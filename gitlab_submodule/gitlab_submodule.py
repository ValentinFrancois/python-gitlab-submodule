from typing import List, Optional, Generator, Union

from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectManager

from gitlab_submodule.objects import Submodule, Subproject
from gitlab_submodule.read_gitmodules import (
    iterate_project_submodules as iterate_submodules)
from gitlab_submodule.submodule_to_project import submodule_to_project
from gitlab_submodule.submodule_commit import get_submodule_commit


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
        get_latest_commit_possible_if_not_found: bool = False,
        get_latest_commit_possible_ref: Optional[str] = None
) -> Subproject:
    submodule_project = submodule_to_project(gitmodules_submodule,
                                             _get_project_manager(gl))
    submodule_commit, commit_is_exact = get_submodule_commit(
        gitmodules_submodule,
        submodule_project,
        get_latest_commit_possible_if_not_found,
        get_latest_commit_possible_ref)
    return Subproject(
        gitmodules_submodule,
        submodule_project,
        submodule_commit,
        commit_is_exact
    )


def iterate_subprojects(
        project: Project,
        gl: Union[Gitlab, ProjectManager],
        ref: Optional[str] = None,
        get_latest_commit_possible_if_not_found: bool = False,
        get_latest_commit_possible_ref: Optional[str] = None
) -> Generator[Subproject, None, None]:
    for gitmodules_submodule in iterate_submodules(project, ref):
        try:
            yield submodule_to_subproject(
                gitmodules_submodule,
                _get_project_manager(gl),
                get_latest_commit_possible_if_not_found,
                get_latest_commit_possible_ref)
        except ValueError:
            continue
        except Exception:
            raise


def list_subprojects(*args, **kwargs) -> List[Subproject]:
    return list(iterate_subprojects(*args, **kwargs))
