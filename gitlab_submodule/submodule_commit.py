from typing import Optional, Tuple

import re

from gitlab.v4.objects import Project, ProjectCommit

from gitlab_submodule.objects import Submodule


def get_submodule_commit(
        submodule: Submodule,
        submodule_project: Project,
        *args,
        **kwargs
 ) -> Tuple[ProjectCommit, bool]:
    commit_id, is_exact = _get_submodule_commit_id(
        submodule.parent_project,
        submodule.path,
        submodule.parent_ref,
        submodule_project,
        *args,
        **kwargs
    )
    commit = submodule_project.commits.get(commit_id)
    return commit, is_exact


def _get_submodule_commit_id(
    project: Project,
    submodule_path: str,
    ref: Optional[str] = None,
    submodule_project: Optional[Project] = None,
    get_latest_commit_possible_if_not_found: bool = False,
    get_latest_commit_possible_ref: Optional[str] = None
) -> Tuple[str, bool]:
    """This uses a trick:
    - The .gitmodules files doesn't contain the actual commit sha that the
      submodules points to.
    - Accessing the `<submodule_path>` dir via the ProjectFileManager
      doesn't bring any useful info, EXCEPT: the id of the last commit that
      modified the file (i.e. that updated the submodule commit sha)

    => We use that info to get the diff of the last commit that updated the
       submodule commit
    => We parse the diff to get the new submodule commit sha

    NOTE: in some weird cases I observed without really understanding,
    a commit which created a .gitmodules file can contain zero submodule
    commit sha in its entire diff.
    In that case, we can only try to guess which was the latest commit in
    the submodule project at the datetime of the commit.
    """
    submodule_dir = project.files.get(
        submodule_path,
        ref=ref if ref else project.default_branch)
    last_commit_id = submodule_dir.last_commit_id
    update_submodule_commit = project.commits.get(last_commit_id)

    submodule_commit_regex = r'Subproject commit ([a-zA-Z0-9]+)\n'
    for diff_file in update_submodule_commit.diff():
        if diff_file['new_path'] == submodule_path:
            # either the commit id was added for the first time,
            # or it was updated -> we can find one or two matches
            # (or 0 in these weird cases)
            matches = re.findall(submodule_commit_regex, diff_file['diff'])
            # submodule commit id was updated
            if len(matches) == 2:
                return matches[1], True
            # submodule was added
            if len(matches) == 1:
                return matches[0], True

    # If the commit diff doesn't contain the submodule commit info, we still
    # know the date of the last commit in the project that updated the
    # submodule, so we can fallback to the last commit in the submodule that
    # was created before this date.
    # This requires a Project object for the submodule so if it wasn't
    # passed we cannot guess anything.
    if not get_latest_commit_possible_if_not_found:
        raise ValueError(
            f'Could not find commit id for submodule {submodule_path} of '
            f'project {project.path_with_namespace}.')
    else:
        last_subproject_commits = submodule_project.commits.list(
            ref_name=(get_latest_commit_possible_ref
                      if get_latest_commit_possible_ref
                      else submodule_project.default_branch),
            until=update_submodule_commit.created_at
        )
    return last_subproject_commits[0].id, False
