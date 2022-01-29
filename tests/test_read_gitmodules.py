import unittest

from gitlab import Gitlab

from gitlab_submodule.read_gitmodules import list_project_submodules


class TestReadGitmodules(unittest.TestCase):

    def test_get_inkscape_submodules(self):

        gl = Gitlab()
        inkscape = gl.projects.get('inkscape/inkscape')
        submodules = list_project_submodules(
            inkscape,
            ref='e371b2f826adcba316f2e64bbf2f697043373d0b')
        self.assertEqual(
            {'https://gitlab.com/inkscape/extensions.git',
             'https://gitlab.com/inkscape/lib2geom.git',
             'https://gitlab.com/inkscape/themes.git'},
            {submodule.url for submodule in submodules}
        )
