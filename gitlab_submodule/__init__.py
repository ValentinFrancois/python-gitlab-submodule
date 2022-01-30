"""List project submodules and get the commits they point to with python-gitlab
"""

__version__ = '0.1.0'
__all__ = [
    'Submodule', 'Subproject',
    'list_submodules',
    'submodule_to_subproject',
    'iterate_subprojects', 'list_subprojects'
]

from gitlab_submodule.objects import Submodule, Subproject
from gitlab_submodule.gitlab_submodule import (
    list_submodules,
    submodule_to_subproject,
    iterate_subprojects,
    list_subprojects,
)
