import sys

from .._display import session_line
from .._data import conform_dataset
from .._display import session_block
from .._data import assert_likelihood
from ..qc._lik import normalise_extreme_values
from ._result import ScanResultFactory


def st_scan(G, y, lik, K=None, M=None, verbose=True):
    """
    Single-variant association testing via generalised linear mixed models.

    It supports Normal (linear mixed model), Bernoulli, Probit, Binomial, and Poisson
    residual errors, defined by ``lik``.
    The columns of ``G`` define the candidates to be tested for association
    with the phenotype ``y``.
    The covariance matrix is set by ``K``.
    If not provided, or set to ``None``, the generalised linear model
    without random effects is assumed.
    The covariates can be set via the parameter ``M``.
    We recommend to always provide a column of ones when covariates are actually
    provided.

    Parameters
    ----------
    G : array_like
        :math:`N` individuals by :math:`S` candidate markers.
    y : array_like
        An outcome array of :math:`N` individuals.
    lik : tuple, "normal", "bernoulli", "probit", binomial", "poisson"
        Sample likelihood describing the residual distribution.
        Either a tuple or a string specifiying the likelihood is required. The Normal,
        Bernoulli, Probit, and Poisson likelihoods can be selected by providing a
        string. Binomial likelihood on the other hand requires a tuple because of the
        number of trials: ``("binomial", array_like)``.
    K : array_like, optional
        :math:`N`-by-:math:`N` covariance matrix (e.g., kinship coefficients).
        Set to ``None`` for a generalised linear model without random effects.
        Defaults to ``None``.
    M : array_like, optional
        `N` individuals by `S` covariates.
        It will create a :math:`N`-by-:math:`1` matrix ``M`` of ones representing the
        offset covariate if ``None`` is passed. If an array is passed, it will used as
        is. Defaults to ``None``.
    verbose : bool, optional
        ``True`` to display progress and summary; ``False`` otherwise.

    Returns
    -------
    :class:`limix.qtl.QTLModel`
        QTL representation.

    Examples
    --------
    .. doctest::

        >>> from numpy import dot, exp, sqrt, ones
        >>> from numpy.random import RandomState
        >>> from pandas import DataFrame
        >>> import pandas as pd
        >>> from limix.qtl import st_scan
        >>>
        >>> random = RandomState(1)
        >>> pd.options.display.float_format = "{:9.6f}".format
        >>>
        >>> n = 30
        >>> p = 3
        >>> samples_index = range(n)
        >>>
        >>> M = DataFrame(dict(offset=ones(n), age=random.randint(10, 60, n)))
        >>> M.index = samples_index
        >>>
        >>> X = random.randn(n, 100)
        >>> K = dot(X, X.T)
        >>>
        >>> candidates = random.randn(n, p)
        >>> candidates = DataFrame(candidates, index=samples_index,
        ...                                    columns=['rs0', 'rs1', 'rs2'])
        >>>
        >>> y = random.poisson(exp(random.randn(n)))
        >>>
        >>> result = st_scan(candidates, y, 'poisson', K, M=M, verbose=False)
        >>>
        >>> result.stats  # doctest: +FLOAT_CMP
               null lml    alt lml    pvalue  dof
        test
        0    -48.736563 -48.561855  0.554443    1
        1    -48.736563 -47.981093  0.218996    1
        2    -48.736563 -48.559868  0.552200    1
        >>> result.alt_effsizes  # doctest: +FLOAT_CMP
           test candidate   effsize  effsize se
        0     0       rs0 -0.130867    0.221390
        1     1       rs1 -0.315079    0.256327
        2     2       rs2 -0.143869    0.242014
        >>> print(result)  # doctest: +FLOAT_CMP
        Null model
        ----------
        <BLANKLINE>
          𝐳 ~ 𝓝(M𝜶, 0.79*K + 0.00*I)
          yᵢ ~ Poisson(λᵢ=g(zᵢ)), where g(x)=eˣ
          M = ['offset' 'age']
          𝜶 = [ 0.39528617 -0.00556789]
          Log marg. lik.: -48.736563230140376
          Number of models: 1
        <BLANKLINE>
        Alt model
        ---------
        <BLANKLINE>
          𝐳 ~ 𝓝(M𝜶 + Gᵢ, 0.79*K + 0.00*I)
          yᵢ ~ Poisson(λᵢ=g(zᵢ)), where g(x)=eˣ
          Min. p-value: 0.21899561824721903
          First perc. p-value: 0.22565970374303942
          Max. log marg. lik.: -47.981092939974765
          99th perc. log marg. lik.: -47.9926684371547
          Number of models: 3

        >>> from numpy import zeros
        >>>
        >>> nsamples = 50
        >>>
        >>> X = random.randn(nsamples, 2)
        >>> G = random.randn(nsamples, 100)
        >>> K = dot(G, G.T)
        >>> ntrials = random.randint(1, 100, nsamples)
        >>> z = dot(G, random.randn(100)) / sqrt(100)
        >>>
        >>> successes = zeros(len(ntrials), int)
        >>> for i, nt in enumerate(ntrials):
        ...     for _ in range(nt):
        ...         successes[i] += int(z[i] + 0.5 * random.randn() > 0)
        >>>
        >>> result = st_scan(X, successes, ("binomial", ntrials), K, verbose=False)
        >>> print(result)  # doctest: +FLOAT_CMP
        Null model
        ----------
        <BLANKLINE>
          𝐳 ~ 𝓝(M𝜶, 1.74*K + 0.15*I)
          yᵢ ~ Binom(μᵢ=g(zᵢ), nᵢ), where g(x)=1/(1+e⁻ˣ)
          M = ['offset']
          𝜶 = [0.40956947]
          Log marg. lik.: -142.9436437096321
          Number of models: 1
        <BLANKLINE>
        Alt model
        ---------
        <BLANKLINE>
          𝐳 ~ 𝓝(M𝜶 + Gᵢ, 1.74*K + 0.15*I)
          yᵢ ~ Binom(μᵢ=g(zᵢ), nᵢ), where g(x)=1/(1+e⁻ˣ)
          Min. p-value: 0.23699422686919802
          First perc. p-value: 0.241827874774993
          Max. log marg. lik.: -142.24445140459548
          99th perc. log marg. lik.: -142.25080258276773
          Number of models: 2

    Notes
    -----
    It will raise a ``ValueError`` exception if non-finite values are passed. Please,
    refer to the :func:`limix.qc.mean_impute` function for missing value imputation.
    """
    from numpy_sugar import is_all_finite
    from numpy_sugar.linalg import economic_qs

    if not isinstance(lik, (tuple, list)):
        lik = (lik,)

    lik_name = lik[0].lower()
    lik = (lik_name,) + lik[1:]
    assert_likelihood(lik_name)

    with session_block("qtl analysis", disable=not verbose):

        with session_line("Normalising input... ", disable=not verbose):
            data = conform_dataset(y, M, G=G, K=K)

        y = data["y"]
        M = data["M"]
        G = data["G"]
        K = data["K"]

        if not is_all_finite(y):
            raise ValueError("Outcome must have finite values only.")

        if not is_all_finite(M):
            raise ValueError("Covariates must have finite values only.")

        if K is not None:
            if not is_all_finite(K):
                raise ValueError("Covariate matrix must have finite values only.")
            QS = economic_qs(K)
        else:
            QS = None

        y = normalise_extreme_values(data["y"], lik)

        r = ST_ScanResultFactory(lik, M.covariate, G.candidate)

        if lik_name == "normal":
            r = _perform_lmm(r, y.values, M, QS, G, verbose)
        else:
            r = _perform_glmm(r, y.values, lik, M, K, QS, G, verbose)

        if verbose:
            print(r)

        return r


def _perform_lmm(r, y, M, QS, G, verbose):
    from glimix_core.lmm import LMM

    lmm = LMM(y, M.values, QS)

    lmm.fit(verbose=verbose)
    sys.stdout.flush()

    null_lml = lmm.lml()

    beta = lmm.beta

    r.set_null(null_lml, beta, lmm.v1, lmm.v0)

    flmm = lmm.get_fast_scanner()
    alt_lmls, effsizes = flmm.fast_scan(G.data, verbose=verbose)

    for i, data in enumerate(zip(alt_lmls, effsizes)):
        r.add_test(i, data[1], data[0])

    return r.create()


def _perform_glmm(r, y, lik, M, K, QS, G, verbose):
    from glimix_core.glmm import GLMMExpFam, GLMMNormal

    glmm = GLMMExpFam(y.ravel(), lik, M.values, QS)

    glmm.fit(verbose=verbose)
    sys.stdout.flush()

    eta = glmm.site.eta
    tau = glmm.site.tau

    gnormal = GLMMNormal(eta, tau, M.values, QS)
    gnormal.fit(verbose=verbose)

    beta = gnormal.beta

    flmm = gnormal.get_fast_scanner()
    flmm.set_scale(1.0)
    null_lml = flmm.null_lml()

    r.set_null(null_lml, beta, gnormal.v1, gnormal.v0)

    alt_lmls, effsizes = flmm.fast_scan(G.values, verbose=verbose)

    for i, data in enumerate(zip(alt_lmls, effsizes)):
        r.add_test(i, data[1], data[0])

    return r.create()