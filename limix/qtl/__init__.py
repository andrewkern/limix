r"""
**********************
Single-variant testing
**********************

- :func:`.qtl_test_lm`
- :func:`.qtl_test_lmm`
- :func:`.qtl_test_lmm_kronecker`
- :func:`.qtl_test_interaction_lmm_kronecker`
- :class:`.LMM`

Public interface
^^^^^^^^^^^^^^^^
"""

from .qtl import qtl_test_lm
from .qtl import qtl_test_lmm
from .qtl import qtl_test_lmm_kronecker
from .qtl import qtl_test_interaction_lmm_kronecker
from .lmm import LMM

__all__ = ['qtl_test_lm', 'qtl_test_lmm', 'qtl_test_lmm_kronecker',
           'qtl_test_interaction_lmm_kronecker', 'LMM']

