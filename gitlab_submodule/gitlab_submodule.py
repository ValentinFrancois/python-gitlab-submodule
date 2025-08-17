from typing import Generator, List, Optional

from gitlab.v4.objects import Project

from gitlab_submodule.objects import Submodule, Subproject
from gitlab_submodule.project_manager_utils import OneOrManyClients
from gitlab_submodule.read_gitmodules import \
    iterate_project_submodules as iterate_submodules
from gitlab_submodule.submodule_commit import get_submodule_commit
from gitlab_submodule.submodule_to_project import submodule_to_project


def submodule_to_subproject(
        gitmodules_submodule: Submodule,
        gls: OneOrManyClients,
) -> Subproject:
    try:
        submodule_project = submodule_to_project(
            gitmodules_submodule,
            gls,
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
        gls: OneOrManyClients,
        ref: Optional[str] = None,
        only_gitlab_subprojects: bool = False,
) -> Generator[Subproject, None, None]:
    for gitmodules_submodule in iterate_submodules(project, ref):
        try:
            subproject: Subproject = submodule_to_subproject(
                gitmodules_submodule,
                gls,
            )
            if not (only_gitlab_subprojects and not subproject.project):
                yield subproject
        except FileNotFoundError:
            pass


def list_subprojects(*args, **kwargs) -> List[Subproject]:
    return list(iterate_subprojects(*args, **kwargs))
