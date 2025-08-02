import configparser
import re
from typing import Iterable, List, Optional, Union

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
    for kwargs in _read_gitmodules_file_content(
            gitmodules_file_content):
        yield Submodule(
            parent_project=project,
            parent_ref=ref if ref else project.default_branch,
            **kwargs)


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
    gitmodules_file_content: str
) -> Iterable[dict[str, Union[None, bool, str]]]:
    """Parses contents of .gitmodule file using configparser"""
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read_string(gitmodules_file_content)
    stropts = ('branch', 'ignore', 'update')
    boolopts = ('recurse', 'shallow')
    name_regex = r'submodule "([a-zA-Z0-9\.\-/_]+)"'
    for section in config.sections():
        try:
            kwargs = {
                'name': re.match(name_regex, section).group(1),
                'path': config.get(section, 'path'),
                'url': config.get(section, 'url')
            }
        except (AttributeError, KeyError):
            raise RuntimeError('Failed parsing the .gitmodules contnet')
        kwargs.update(
            (opt, config.get(section, opt, fallback=None))
            for opt in stropts
        )
        kwargs.update(
            (opt, config.getboolean(section, opt, fallback=False))
            for opt in boolopts
        )
        yield kwargs
