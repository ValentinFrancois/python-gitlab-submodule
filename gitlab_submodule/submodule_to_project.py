import logging
import re
from posixpath import join, normpath
from typing import Optional, Tuple

from gitlab.exceptions import GitlabGetError, GitlabHttpError
from gitlab.v4.objects import Project, ProjectManager
from giturlparse import GitUrlParsed, parse

from gitlab_submodule.objects import Submodule
from gitlab_submodule.project_manager_utils import (OneOrManyClients,
                                                    map_domain_to_clients)
from gitlab_submodule.string_utils import lstrip, rstrip

logger = logging.getLogger(__name__)


def host_url_to_domain(url: str) -> str:
    return url.split("//")[1].rstrip("/")


def match_submodule_to_client_and_format_project_path(
        submodule: Submodule,
        gls: OneOrManyClients
) -> Optional[Tuple[ProjectManager, str]]:
    url = submodule.url

    # check if the submodule url is a relative path to the project path
    if url.startswith('./') or url.startswith('../'):
        # we build the path of the submodule project using the path of
        # the current project
        url = rstrip(url, '.git')
        path_with_namespace = normpath(join(
            submodule.parent_project.path_with_namespace,
            url
        ))
        client: ProjectManager = submodule.parent_project.manager
        return client, path_with_namespace

    # If URL is not relative: try parsing it
    parsed: GitUrlParsed = parse(url)
    if not parsed.valid:
        logger.warning(f'submodule git url does not seem to be valid: {url}')
        return None

    url_to_client = map_domain_to_clients(gls)
    domain_to_client = {
        host_url_to_domain(_url): client
        for _url, client in url_to_client.items()
    }

    matched_domain = [
        domain for domain in domain_to_client
        if re.search("(^|[/@])" + domain, url)
    ]
    if len(matched_domain) == 0:
        logger.warning(f'submodule git url is not hosted on gitlab: {url}')
        return None
    elif len(matched_domain) > 1:
        raise ValueError(f"More than one of the provided Gitlab host domains "
                         f"matches submodule url {url}")
    else:
        matched_domain = matched_domain[0]
    client = domain_to_client[matched_domain]

    # Format to python-gitlab path_with_namespace:
    # rewrite to https format then split by host and keep & cut the right part.
    # I find it more robust than trying to rebuild the path from the different
    # attributes of giturlparse.GitUrlParsed objects
    https_url = parsed.url2https
    path_with_namespace = https_url.split(matched_domain)[1]
    path_with_namespace = lstrip(path_with_namespace, '/')
    path_with_namespace = rstrip(path_with_namespace, '.git')
    return client, path_with_namespace


def submodule_to_project(
        submodule: Submodule,
        gls: OneOrManyClients,
) -> Optional[Project]:
    match = match_submodule_to_client_and_format_project_path(
        submodule=submodule,
        gls=gls
    )
    if not match:
        return None
    try:
        client, submodule_project_path_with_namespace = match
        submodule_project = client.get(submodule_project_path_with_namespace)
    except (GitlabGetError, GitlabHttpError):
        # Repo doesn't actually exist (possible because you can modify
        # .gitmodules without using `git submodule add`)
        raise FileNotFoundError(
            'No repo found at url "{}" for submodule at path "{}" - Check if '
            'the repo was deleted.'.format(submodule.url, submodule.path))
    return submodule_project
