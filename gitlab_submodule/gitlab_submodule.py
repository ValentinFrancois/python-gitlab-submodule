from typing import List, Optional, Iterable

from gitlab.v4.objects import Project

from gitlab_submodule.objects import GitmodulesSubmodule, ProjectSubmodule
from gitlab_submodule.read_gitmodules import list_project_submodules
from gitlab_submodule.gitmodules_to_project import gitmodules_to_project
from gitlab_submodule.submodule_commit import get_submodule_commit


def list_all_project_submodules(
        project: Project,
        ref: Optional[str] = None) -> List[GitmodulesSubmodule]:
    return list_project_submodules(project, ref)


def read_gitlab_submodule(
        gitmodules_submodule: GitmodulesSubmodule,
        get_latest_commit_possible_if_not_found: bool = True,
        get_latest_commit_possible_ref: Optional[str] = None
) -> ProjectSubmodule:
    submodule_project = gitmodules_to_project(gitmodules_submodule)
    submodule_commit, commit_is_exact = get_submodule_commit(
        gitmodules_submodule,
        submodule_project,
        get_latest_commit_possible_if_not_found,
        get_latest_commit_possible_ref)
    return ProjectSubmodule(
        gitmodules_submodule,
        submodule_project,
        submodule_commit,
        commit_is_exact
    )


def iterate_gitlab_project_submodules(
        project: Project,
        ref: Optional[str] = None,
        get_latest_commit_possible_if_not_found: bool = True,
        get_latest_commit_possible_ref: Optional[str] = None
) -> Iterable[ProjectSubmodule]:
    for gitmodules_submodule in list_all_project_submodules(project, ref):
        try:
            yield read_gitlab_submodule(
                gitmodules_submodule,
                get_latest_commit_possible_if_not_found,
                get_latest_commit_possible_ref)
        except ValueError:
            continue
        except Exception:
            raise


def list_gitlab_project_submodules(**kwargs) -> List[ProjectSubmodule]:
    return list(iterate_gitlab_project_submodules(**kwargs))
