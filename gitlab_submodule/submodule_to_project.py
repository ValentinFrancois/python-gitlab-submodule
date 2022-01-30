from typing import Optional

from posixpath import join, normpath
from giturlparse import parse

from gitlab.v4.objects import Project, ProjectManager

from gitlab_submodule.objects import Submodule


def submodule_to_project(submodule: Submodule,
                         project_manager: ProjectManager) -> Project:
    submodule_project_path_with_namespace = \
        _submodule_url_to_path_with_namespace(submodule.url,
                                              submodule.parent_project)
    if not submodule_project_path_with_namespace:
        raise ValueError(
            f'submodule at {submodule.url} is not hosted on Gitlab')
    submodule_project = project_manager.get(
        submodule_project_path_with_namespace)
    return submodule_project


def _submodule_url_to_path_with_namespace(
        url: str,
        parent_project: Project
) -> Optional[str]:
    """Returns a path pointing to a Gitlab project, or None if the submodule
    is hosted elsewhere
    """
    try:
        parsed = parse(url)
        if parsed.platform != 'gitlab':
            return None
        if parsed.groups:
            to_join = [parsed.owner, join(*parsed.groups), parsed.repo]
        else:
            to_join = [parsed.owner, parsed.repo]
        path_with_namespace = join(*to_join)
        return path_with_namespace
    except Exception:
        # check if the submodule url is a relative path to the project path
        if url.startswith('./') or url.startswith('../'):
            # we build the path of the submodule project using the path of
            # the current project
            path_with_namespace = normpath(
                join(parent_project.path_with_namespace, url))
            return path_with_namespace
    return None
