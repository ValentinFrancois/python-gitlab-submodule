import unittest

from gitlab import Gitlab

from gitlab_submodule.read_gitmodules import list_project_submodules
from gitlab_submodule.gitmodules_to_project import gitmodules_to_project


class SubmoduleAsGitlabProject(unittest.TestCase):

    def test_get_inkscape_submodules_as_projects(self):

        gl = Gitlab()
        inkscape = gl.projects.get('inkscape/inkscape')
        submodules = list_project_submodules(inkscape)
        submodule_projects = [
            gitmodules_to_project(submodule)
            for submodule in submodules
        ]
        self.assertEqual(
            {'extensions', 'lib2geom', 'themes'},
            {project.name for project in submodule_projects}
        )
