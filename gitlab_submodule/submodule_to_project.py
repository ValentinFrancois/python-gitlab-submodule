from typing import List, Optional, Union

import logging
import re
from posixpath import join, normpath

from gitlab.exceptions import GitlabGetError
from gitlab.v4.objects import Project, ProjectManager
from giturlparse import GitUrlParsed, parse

from gitlab_submodule.objects import Submodule
from gitlab_submodule.string_utils import lstrip, rstrip

logger = logging.getLogger(__name__)


def submodule_to_project(
        submodule: Submodule,
        project_manager: ProjectManager,
        self_managed_gitlab_host: Optional[Union[str, List[str]]] = None
) -> Optional[Project]:
    submodule_project_path_with_namespace = \
        _submodule_url_to_path_with_namespace(submodule.url,
                                              submodule.parent_project,
                                              self_managed_gitlab_host)
    if not submodule_project_path_with_namespace:
        return None
    try:
        submodule_project = project_manager.get(
            submodule_project_path_with_namespace)
    except GitlabGetError:
        # Repo doesn't actually exist (possible because you can modify
        # .gitmodules without using `git submodule add`)
        raise FileNotFoundError(
            'No repo found at url "{}" for submodule at path "{}" - Check if '
            'the repo was deleted.'.format(submodule.url, submodule.path))
    return submodule_project


def _submodule_url_to_path_with_namespace(
        url: str,
        parent_project: Project,
        self_managed_gitlab_host: Optional[Union[str, List[str]]] = None
) -> Optional[str]:
    """Returns a path pointing to a Gitlab project, or None if the submodule
    is hosted elsewhere
    """
    # check if the submodule url is a relative path to the project path
    if url.startswith('./') or url.startswith('../'):
        # we build the path of the submodule project using the path of
        # the current project
        url = rstrip(url, '.git')
        path_with_namespace = normpath(
            join(parent_project.path_with_namespace, url))
        return path_with_namespace

    parsed: GitUrlParsed = parse(url)
    if not parsed.valid:
        logger.warning(f'submodule git url does not seem to be valid: {url}')
        return None

    # even if the parent project is hosted on a self-managed gitlab host,
    # it can still use submodules hosted on gitlab.com
    gitlab_hosts = ['gitlab']
    if self_managed_gitlab_host:
        if isinstance(self_managed_gitlab_host, str):
            gitlab_hosts.append(self_managed_gitlab_host)
        else:
            gitlab_hosts.extend(self_managed_gitlab_host)

    # giturlparse.GitUrlParsed.platform is too permissive and will be set to
    # 'gitlab' for some non-gitlab urls, for instance:
    # https://opensource.ncsa.illinois.edu/bitbucket/scm/u3d/3dutilities.git
    if (parsed.platform not in ('gitlab', 'base')
            or not any([re.match(fr'^{host}(\.\w+)?$', parsed.host)
                        for host in gitlab_hosts])):
        logger.warning(f'submodule git url is not hosted on gitlab: {url}')
        return None

    # Format to python-gitlab path_with_namespace:
    # rewrite to https format then split by host and keep & cut the right part.
    # I find it more robust than trying to rebuild the path from the different
    # attributes of giturlparse.GitUrlParsed objects
    https_url = parsed.url2https
    path_with_namespace = https_url.split(parsed.host)[1]
    path_with_namespace = lstrip(path_with_namespace, '/')
    path_with_namespace = rstrip(path_with_namespace, '.git')
    return path_with_namespace
