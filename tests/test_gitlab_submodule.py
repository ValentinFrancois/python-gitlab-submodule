import unittest

from gitlab import Gitlab

from gitlab_submodule.objects import ProjectSubmodule
from gitlab_submodule.gitlab_submodule import (list_all_project_submodules,
                                               read_gitlab_submodule,
                                               list_gitlab_project_submodules)


class TestSubmoduleCommit(unittest.TestCase):

    def test_read_inkscape_submodule_info(self):

        gl = Gitlab()
        inkscape = gl.projects.get('inkscape/inkscape')
        submodules = list_all_project_submodules(
            inkscape,
            ref='e371b2f826adcba316f2e64bbf2f697043373d0b')
        submodule = [sub for sub in submodules if
                     sub.url == 'https://gitlab.com/inkscape/lib2geom.git'][0]
        submodule_info: ProjectSubmodule = read_gitlab_submodule(submodule)
        self.assertEqual(submodule_info.submodule, submodule)

        submodule_project = gl.projects.get('inkscape/lib2geom')
        self.assertEqual(submodule_info.project, submodule_project)

        submodule_commit = submodule_project.commits.get(
            '9d38946b7d7a0486a4a75669008112d306309d9e')
        self.assertEqual(submodule_info.commit, submodule_commit)

    def test_list_all_inkscape_submodule_info(self):
        gl = Gitlab()
        inkscape = gl.projects.get('inkscape/inkscape')
        submodule_info_list = list_gitlab_project_submodules(
            inkscape,
            ref='e371b2f826adcba316f2e64bbf2f697043373d0b')
        for submodule_info in submodule_info_list:
            print('- {} -> {}'.format(
                submodule_info.submodule.path, submodule_info.commit.id))
