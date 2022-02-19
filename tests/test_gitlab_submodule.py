import unittest

from gitlab import Gitlab

from gitlab_submodule.objects import Subproject
from gitlab_submodule.gitlab_submodule import (list_submodules,
                                               submodule_to_subproject,
                                               list_subprojects)


class TestGitlabSubmodule(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.gl = Gitlab()

    def test_read_subproject_details_with_absolute_url(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-absolute-urls')
        submodules = list_submodules(
            project,
            ref='ce9b1e50b34372d82df098f3ffded58ef4be03ec')
        submodule = [sub for sub in submodules if
                     sub.name == 'git@gitlab.com:fdroid/fdroidclient.git'][0]
        submodule_info: Subproject = submodule_to_subproject(
            submodule, self.gl)
        self.assertEqual(submodule_info.submodule, submodule)

        submodule_project = self.gl.projects.get('fdroid/fdroidclient')
        self.assertEqual(submodule_info.project, submodule_project)

        submodule_commit = submodule_project.commits.get(
            'aee2759733857e2d2c021c4f6127f7e8a908a3f2')
        self.assertEqual(submodule_info.commit, submodule_commit)

    def test_read_subproject_details_with_relative_url(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-relative-urls')
        submodules = list_submodules(project, ref='main')
        submodule = [sub for sub in submodules if sub.name == '1'][0]
        submodule_info: Subproject = submodule_to_subproject(
            submodule, self.gl)
        self.assertEqual(submodule_info.submodule, submodule)

        submodule_project = self.gl.projects.get(
            'python-gitlab-submodule-test/dummy-projects/1')
        self.assertEqual(submodule_info.project, submodule_project)

        submodule_commit = submodule_project.commits.get(
            'e5a7153ae32515d9cdba12557345e627f7231fe2')
        self.assertEqual(submodule_info.commit, submodule_commit)

    def test_list_subprojects_with_absolute_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-absolute-urls')
        subprojects = list_subprojects(project, self.gl)
        self.assertEqual(3, len(subprojects))
        for subproject in subprojects:
            print('- {} ({}) -> {}'.format(
                subproject.submodule.path,
                subproject.project.ssh_url_to_repo,
                subproject.commit.id))

    def test_list_subprojects_with_relative_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-relative-urls')
        subprojects = list_subprojects(project, self.gl)
        self.assertEqual(4, len(subprojects))
        for subproject in subprojects:
            print('- {} ({}) -> {}'.format(
                subproject.submodule.path,
                subproject.project.ssh_url_to_repo,
                subproject.commit.id))

    def test_list_subprojects_with_external_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/external-urls')
        subprojects = list_subprojects(project, self.gl)
        self.assertEqual([], subprojects)

    def test_compare_subprojects_commits_to_head_with_absolute_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-absolute-urls')
        subprojects = list_subprojects(
            project,
            self.gl,
            ref='ce9b1e50b34372d82df098f3ffded58ef4be03ec')
        for subproject in subprojects:
            head_subproject_commit = subproject.project.commits.list(
                ref=subproject.project.default_branch)[0]
            submodule_commit = subproject.commit.id
            up_to_date = submodule_commit == head_subproject_commit.id
            print('- {}: {}'.format(
                subproject.submodule.path,
                'ok' if up_to_date else '/!\\ must update'))

    def test_compare_subprojects_commits_to_head_with_relative_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-relative-urls')
        subprojects = list_subprojects(project, self.gl)
        for subproject in subprojects:
            head_subproject_commit = subproject.project.commits.list(
                ref=subproject.project.default_branch)[0]
            submodule_commit = subproject.commit.id
            up_to_date = submodule_commit == head_subproject_commit.id
            if subproject.name in {'1', '2'}:
                self.assertTrue(up_to_date)
            else:
                self.assertFalse(up_to_date)
            print('- {}: {}'.format(
                subproject.submodule.path,
                'ok' if up_to_date else '/!\\ must update'))
