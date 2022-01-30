import unittest

from gitlab import Gitlab

from gitlab_submodule.objects import Subproject
from gitlab_submodule.gitlab_submodule import (list_submodules,
                                               submodule_to_subproject,
                                               list_subprojects)


class TestSubmoduleCommit(unittest.TestCase):

    def test_read_inkscape_submodule_info(self):

        gl = Gitlab()
        inkscape = gl.projects.get('inkscape/inkscape')
        submodules = list_submodules(
            inkscape,
            ref='e371b2f826adcba316f2e64bbf2f697043373d0b')
        submodule = [sub for sub in submodules if
                     sub.url == 'https://gitlab.com/inkscape/lib2geom.git'][0]
        submodule_info: Subproject = submodule_to_subproject(submodule, gl)
        self.assertEqual(submodule_info.submodule, submodule)

        submodule_project = gl.projects.get('inkscape/lib2geom')
        self.assertEqual(submodule_info.project, submodule_project)

        submodule_commit = submodule_project.commits.get(
            '9d38946b7d7a0486a4a75669008112d306309d9e')
        self.assertEqual(submodule_info.commit, submodule_commit)

    def test_list_all_inkscape_submodule_info(self):
        gl = Gitlab()
        inkscape = gl.projects.get('inkscape/inkscape')
        subprojects = list_subprojects(
            inkscape,
            gl,
            ref='e371b2f826adcba316f2e64bbf2f697043373d0b')
        for subproject in subprojects:
            print('- {} ({}) -> {}'.format(
                subproject.submodule.path,
                subproject.project.ssh_url_to_repo,
                subproject.commit.id))
