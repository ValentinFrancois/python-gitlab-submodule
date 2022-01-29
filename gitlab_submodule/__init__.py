"""List project submodules and get the commits they point to with python-gitlab
"""

__version__ = '0.1.0'
__all__ = [
    'GitmodulesSubmodule', 'ProjectSubmodule',
    'list_all_project_submodules',
    'read_gitlab_submodule',
    'iterate_gitlab_project_submodules', 'list_gitlab_project_submodules'
]

from gitlab_submodule.objects import GitmodulesSubmodule, ProjectSubmodule
from gitlab_submodule.gitlab_submodule import (
    list_all_project_submodules,
    read_gitlab_submodule,
    iterate_gitlab_project_submodules,
    list_gitlab_project_submodules
)
