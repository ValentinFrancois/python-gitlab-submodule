"""List project submodules and get the commits they point to with python-gitlab
"""

from gitlab_submodule.__version__ import __version__ as hardcoded_version

__version__ = hardcoded_version

__all__ = [
    'Submodule', 'Subproject',
    'list_submodules', 'iterate_submodules',
    'submodule_to_subproject',
    'iterate_subprojects', 'list_subprojects'
]

from gitlab_submodule.objects import Submodule, Subproject
from gitlab_submodule.read_gitmodules import (
    list_project_submodules as list_submodules)
from gitlab_submodule.gitlab_submodule import (
    iterate_submodules,
    submodule_to_subproject,
    iterate_subprojects,
    list_subprojects,
)
