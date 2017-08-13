from __future__ import unicode_literals

import os
import sys

from setuptools import find_packages, setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except (OSError, IOError, ImportError):
    long_description = open('README.md').read()


def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner = ['pytest-runner>=2.9'] if needs_pytest else []

    setup_requires = ["cython", "numpy"] + pytest_runner
    install_requires = [
        'scikit-learn>=0.19.0', 'limix-core>=1.0.1', 'tabulate>=0.7.7',
        'dask[array,bag,dataframe,delayed]>=0.14', 'h5py',
        'pandas-plink>=1.1.7', 'limix-legacy', 'glimix-core>=1.2.20',
        'joblib>=0.11', 'tqdm>=4.10', 'scipy>=0.18', 'distributed',
        'numpy-sugar>=1.0.47', 'ncephes>=1.0.38', 'asciitree>=0.3.3',
        'humanfriendly>=3.6.1', 'statsmodels>=0.8', 'brent-search>=1.0.18',
        'pandas>=0.20', 'feather-format>=0.4'
    ]
    tests_require = ['pytest', 'pytest-console-scripts', 'pytest-pep8']
    recommended = {"numba": ["numba>=0.32"]}

    console_scripts = [
        'limix_runner=limix.scripts.limix_runner:entry_point',
        'mtset_postprocess=limix.scripts.mtset_postprocess:entry_point',
        'mtset_preprocess=limix.scripts.mtset_preprocess:entry_point',
        'mtset_definesets=limix.scripts.mtset_definesets:entry_point',
        'mtset_simpheno=limix.scripts.mtset_simpheno:entry_point',
        'mtset_analyze=limix.scripts.mtset_analyze:entry_point',
        'limix_converter=limix.scripts.limix_converter:entry_point',
        'iset_analyze=limix.scripts.iset_analyze:entry_point',
        'iset_postprocess=limix.scripts.iset_postprocess:entry_point',
        'limix=limix.scripts._limix:entry_point',
        'ilimix=limix.scripts.ilimix:entry_point'
    ]

    metadata = dict(
        name='limix',
        version='1.0.9',
        maintainer="Limix Developers",
        maintainer_email="horta@ebi.ac.uk",
        author=("Christoph Lippert, Danilo Horta, " +
                "Francesco Paolo Casale, Oliver Stegle"),
        author_email="stegle@ebi.ac.uk",
        license="Apache License 2.0'",
        description="A flexible and fast mixed model toolbox.",
        long_description=long_description,
        url='https://github.com/limix/limix',
        packages=find_packages(),
        zip_safe=False,
        install_requires=install_requires,
        setup_requires=setup_requires,
        tests_require=tests_require,
        extras_require=recommended,
        include_package_data=True,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        entry_points={'console_scripts': console_scripts})

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)


if __name__ == '__main__':
    setup_package()
