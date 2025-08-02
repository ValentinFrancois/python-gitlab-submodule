from typing import Dict, List, Union

from gitlab import Gitlab
from gitlab.v4.objects import ProjectManager

# Some typing
Client = Union[Gitlab, ProjectManager]
OneOrManyClients = Union[Client, List[Client]]
ProjectManagerDicts = Dict[str, ProjectManager]


def as_project_manager(gl: Client) -> ProjectManager:
    if isinstance(gl, ProjectManager):
        return gl
    elif isinstance(gl, Gitlab):
        return gl.projects
    else:
        raise TypeError('Needs a Gitlab instance or its ProjectManager')


def get_host_url(gl: Client) -> str:
    if isinstance(gl, Gitlab):
        return gl._base_url
    elif isinstance(gl, ProjectManager):
        return gl.gitlab._base_url
    else:
        raise TypeError(gl)


def map_domain_to_clients(gls: OneOrManyClients) -> ProjectManagerDicts:
    if not isinstance(gls, list):
        gls = [gls]
    return {get_host_url(gl): as_project_manager(gl) for gl in gls}
