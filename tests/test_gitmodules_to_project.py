import unittest

from gitlab import Gitlab
from gitlab.v4.objects import Project

from gitlab_submodule.read_gitmodules import list_project_submodules
from gitlab_submodule.gitmodules_to_project import gitmodules_to_project


class TestGitmodulesToProject(unittest.TestCase):

    def test_get_inkscape_submodules_as_projects(self):
        gl = Gitlab()
        inkscape = gl.projects.get('inkscape/inkscape')
        submodules = list_project_submodules(
            inkscape,
            ref='e371b2f826adcba316f2e64bbf2f697043373d0b'
        )
        submodule_projects = [
            gitmodules_to_project(submodule, gl.projects)
            for submodule in submodules
        ]
        self.assertTrue(all(
            isinstance(project, Project)
            for project in submodule_projects
        ))
        self.assertEqual(
            {'extensions', 'lib2geom', 'themes'},
            {project.name for project in submodule_projects}
        )
