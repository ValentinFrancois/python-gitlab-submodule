from typing import List, Optional, Iterable, Union

from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectManager

from gitlab_submodule.objects import Submodule, Subproject
from gitlab_submodule.read_gitmodules import list_project_submodules
from gitlab_submodule.gitmodules_to_project import gitmodules_to_project
from gitlab_submodule.submodule_commit import get_submodule_commit


list_submodules = list_project_submodules


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
        gitlab: Union[Gitlab, ProjectManager],
        get_latest_commit_possible_if_not_found: bool = True,
        get_latest_commit_possible_ref: Optional[str] = None
) -> Subproject:
    submodule_project = gitmodules_to_project(gitmodules_submodule,
                                              _get_project_manager(gitlab))
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
        gitlab: Union[Gitlab, ProjectManager],
        ref: Optional[str] = None,
        get_latest_commit_possible_if_not_found: bool = True,
        get_latest_commit_possible_ref: Optional[str] = None
) -> Iterable[Subproject]:
    for gitmodules_submodule in list_project_submodules(project, ref):
        try:
            yield submodule_to_subproject(
                gitmodules_submodule,
                _get_project_manager(gitlab),
                get_latest_commit_possible_if_not_found,
                get_latest_commit_possible_ref)
        except ValueError:
            continue
        except Exception:
            raise


def list_subprojects(*args, **kwargs) -> List[Subproject]:
    return list(iterate_subprojects(*args, **kwargs))
