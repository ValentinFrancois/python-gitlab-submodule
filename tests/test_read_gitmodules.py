import unittest

from gitlab import Gitlab

from gitlab_submodule.read_gitmodules import list_project_submodules


class TestReadGitmodules(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.gl = Gitlab()

    def test_gitmodules_with_gitlab_absolute_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-absolute-urls')
        submodules = list_project_submodules(
            project,
            ref='ce9b1e50b34372d82df098f3ffded58ef4be03ec')
        self.assertEqual(
            {'git@gitlab.com:fdroid/fdroidclient.git',
             'ssh://git@gitlab.com:/CalcProgrammer1/OpenRGB.git',
             'https://gitlab.com/inkscape/inkscape.git'},
            {submodule.url for submodule in submodules})

    def test_gitmodules_with_gitlab_relative_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-relative-urls')
        submodules = list_project_submodules(project, ref='main')
        self.assertEqual(
            {'../../dummy-projects/1.git',
             '../../../python-gitlab-submodule-test/dummy-projects/2.git',
             './../../../python-gitlab-submodule-test/dummy-projects/3.git',
             './../../dummy-projects/4.git',
             './../../missing-repos/5.git'},
            {submodule.url for submodule in submodules})

    def test_gitmodules_with_external_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/external-urls')
        submodules = list_project_submodules(project)
        self.assertEqual(
            {('https://opensource.ncsa.illinois.edu/bitbucket/scm/u3d/'
              '3dutilities.git'),
             'git://git.code.sf.net/p/scribus/code',
             'ssh://git@github.com:/opencv/opencv.git'},
            {submodule.url for submodule in submodules})
