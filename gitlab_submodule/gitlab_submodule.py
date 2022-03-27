from typing import Generator, List, Optional, Union

from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectManager

from gitlab_submodule.objects import Submodule, Subproject
from gitlab_submodule.read_gitmodules import \
    iterate_project_submodules as iterate_submodules
from gitlab_submodule.submodule_commit import get_submodule_commit
from gitlab_submodule.submodule_to_project import submodule_to_project


def _get_project_manager(
        gitlab_object: Union[Gitlab, ProjectManager]) -> ProjectManager:
    if isinstance(gitlab_object, ProjectManager):
        return gitlab_object
    elif isinstance(gitlab_object, Gitlab):
        return gitlab_object.projects
    else:
        raise TypeError('Needs a Gitlab instance or its ProjectManager')


def submodule_to_subproject(
        gitmodules_submodule: Submodule,
        gl: Union[Gitlab, ProjectManager],
        self_managed_gitlab_host: Optional[str] = None
) -> Subproject:
    try:
        submodule_project = submodule_to_project(
            gitmodules_submodule,
            _get_project_manager(gl),
            self_managed_gitlab_host
        )
        submodule_commit = get_submodule_commit(
            gitmodules_submodule,
            submodule_project,
        )
        return Subproject(
            gitmodules_submodule,
            submodule_project,
            submodule_commit,
        )
    except FileNotFoundError:
        raise


def iterate_subprojects(
        project: Project,
        gl: Union[Gitlab, ProjectManager],
        ref: Optional[str] = None,
        only_gitlab_subprojects: bool = False,
        self_managed_gitlab_host: Optional[str] = None
) -> Generator[Subproject, None, None]:
    for gitmodules_submodule in iterate_submodules(project, ref):
        try:
            subproject: Subproject = submodule_to_subproject(
                gitmodules_submodule,
                _get_project_manager(gl),
                self_managed_gitlab_host,
            )
            if not (only_gitlab_subprojects and not subproject.project):
                yield subproject
        except FileNotFoundError:
            pass


def list_subprojects(*args, **kwargs) -> List[Subproject]:
    return list(iterate_subprojects(*args, **kwargs))
