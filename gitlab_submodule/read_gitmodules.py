import re
from typing import Iterable, List, Optional, Tuple

from gitlab.v4.objects import Project

from gitlab_submodule.objects import Submodule


def list_project_submodules(
        project: Project,
        ref: Optional[str] = None) -> List[Submodule]:
    return list(iterate_project_submodules(project, ref))


def iterate_project_submodules(
        project: Project,
        ref: Optional[str] = None) -> Iterable[Submodule]:
    gitmodules_file_content = _get_gitmodules_file_content(project, ref)
    if not gitmodules_file_content:
        return []
    for (name, url, path) in _read_gitmodules_file_content(
            gitmodules_file_content):
        yield Submodule(
            parent_project=project,
            parent_ref=ref if ref else project.default_branch,
            name=name,
            url=url,
            path=path)


def _get_gitmodules_file_content(project: Project,
                                 ref: Optional[str] = None) -> Optional[str]:
    try:
        gitmodules = project.files.get(
            '.gitmodules',
            ref=ref if ref else project.default_branch)
        return gitmodules.decode().decode('utf-8')
    except Exception:
        return None


def _read_gitmodules_file_content(
        gitmodules_file_content: str) -> Iterable[Tuple[str, str, str]]:
    """Some basic regex extractions to parse content of .gitmodules file
    """
    name_regex = r'\[submodule "([a-zA-Z0-9\.\-/_]+)"\]'
    path_regex = r'path ?= ?([a-zA-Z0-9\.\-/_]+)'
    url_regex = r'url ?= ?([a-zA-Z0-9\.\-/_:@]+)'
    names = re.findall(name_regex, gitmodules_file_content)
    paths = re.findall(path_regex, gitmodules_file_content)
    urls = re.findall(url_regex, gitmodules_file_content)
    if not (len(names) == len(paths) == len(urls)):
        raise RuntimeError('Failed parsing the .gitmodules content')
    return zip(names, urls, paths)
