from typing import Optional, Tuple, Union

import re

from gitlab.v4.objects import Project, ProjectCommit
from gitlab.exceptions import GitlabGetError

from gitlab_submodule.objects import Submodule, Commit


def get_submodule_commit(
        submodule: Submodule,
        submodule_project: Optional[Project] = None,
 ) -> Union[ProjectCommit, Commit]:
    commit_id = _get_submodule_commit_id(
        submodule.parent_project,
        submodule.path,
        submodule.parent_ref,
    )
    if submodule_project is not None:
        commit = submodule_project.commits.get(commit_id)
    else:
        commit = Commit(commit_id)
    return commit


def _get_submodule_commit_id(
    project: Project,
    submodule_path: str,
    ref: Optional[str] = None,
) -> str:
    """This uses a trick:
    - The .gitmodules files doesn't contain the actual commit sha that the
      submodules points to.
    - Accessing the `<submodule_path>` dir via the ProjectFileManager
      doesn't bring any useful info, EXCEPT: the id of the last commit that
      modified the file (i.e. that updated the submodule commit sha)

    => We use that info to get the diff of the last commit that updated the
       submodule commit
    => We parse the diff to get the new submodule commit sha
    """
    try:
        submodule_dir = project.files.get(
            submodule_path,
            ref=ref if ref else project.default_branch)
    except GitlabGetError:
        raise FileNotFoundError(
           f'Local submodule path "{submodule_path}" was not found for '
           f'project at url "{project.web_url}" - check if your .gitmodules '
           f'file is up-to-date.')

    last_commit_id = submodule_dir.last_commit_id
    update_submodule_commit = project.commits.get(last_commit_id)

    submodule_commit_regex = r'Subproject commit ([a-zA-Z0-9]+)\n'
    for diff_file in update_submodule_commit.diff(as_list=False):
        if diff_file['new_path'] == submodule_path:
            # either the commit id was added for the first time,
            # or it was updated -> we can find one or two matches
            # (or 0 in these weird cases)
            matches = re.findall(submodule_commit_regex, diff_file['diff'])
            # submodule commit id was updated
            if len(matches) == 2:
                return matches[1]
            # submodule was added
            if len(matches) == 1:
                return matches[0]

    # should never happen
    raise RuntimeError(f'Did not find any commit id for submodule '
                       f'"{submodule_path}" at url "{project.web_url}"')
