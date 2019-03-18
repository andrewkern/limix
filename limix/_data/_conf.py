CONF = {
    "likelihoods": set(["normal", "bernoulli", "probit", "binomial", "poisson"]),
    "targets": set(
        [
            "trait",
            "covariate",
            "covariance",
            "genotype",
            "covariate",
            "inter0",
            "inter1",
        ]
    ),
    "filetypes": set(["csv", "bed"]),
    "dim_axis": {
        "sample": 0,
        "trait": 1,
        "candidate": 1,
        "covariate": 1,
        "sample_0": 0,
        "sample_1": 1,
    },
    "dim_names": {"sample", "candidate", "covariate", "trait"},
    "data_synonym": {
        "y": "trait",
        "trait": "y",
        "G": "genotype",
        "genotype": "G",
        "M": "covariate",
        "covariate": "M",
        "K": "covariance",
        "covariance": "K",
    },
    "data_dims": {
        "trait": ["sample", "trait"],
        "genotype": ["sample", "candidate"],
        "covariate": ["sample", "covariate"],
        "covariance": ["sample_0", "sample_1"],
        "inter0": ["sample", "inter"],
        "inter1": ["sample", "inter"],
    },
    "varname_to_target": {
        "y": "trait",
        "M": "covariate",
        "G": "genotype",
        "K": "covariance",
    },
    "target_to_varname": {
        "trait": "y",
        "covariate": "M",
        "genotype": "G",
        "covariance": "K",
    },
}
