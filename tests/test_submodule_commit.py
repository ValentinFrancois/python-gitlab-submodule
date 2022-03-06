import unittest

from gitlab import Gitlab
from gitlab.v4.objects import ProjectCommit

from gitlab_submodule.read_gitmodules import list_project_submodules
from gitlab_submodule.submodule_to_project import submodule_to_project
from gitlab_submodule.submodule_commit import (get_submodule_commit,
                                               _get_submodule_commit_id)


class TestSubmoduleCommit(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.gl = Gitlab()

    def test__get_submodule_commit_id_with_absolute_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-absolute-urls')
        submodules = list_project_submodules(
            project,
            ref='ce9b1e50b34372d82df098f3ffded58ef4be03ec')
        submodule_commit_ids = [
            _get_submodule_commit_id(
                submodule.parent_project,
                submodule.path,
                submodule.parent_ref,
                get_latest_commit_possible_if_not_found=False
            )
            for submodule in submodules
        ]
        self.assertEqual(
            {'aee2759733857e2d2c021c4f6127f7e8a908a3f2',  # fdroidclient
             'dcf7b47f9d0a194b16d21c567edd028d56d4b967',  # inkscape
             '238d1c01625e2e94e4733f30d5bf46018676a36f'},  # openRGB
            {commit_id for commit_id, _ in submodule_commit_ids})
        self.assertTrue(all(is_exact for _, is_exact in submodule_commit_ids))

    def test_get_submodule_commit_with_absolute_urls(self):
        gl = Gitlab()
        inkscape = gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-absolute-urls')
        submodules = list_project_submodules(
            inkscape,
            ref='ce9b1e50b34372d82df098f3ffded58ef4be03ec')
        submodule_projects = [
            submodule_to_project(submodule, gl.projects)
            for submodule in submodules]
        submodule_commits = [
            get_submodule_commit(
                submodule,
                submodule_project,
                get_latest_commit_possible_if_not_found=False)
            for submodule, submodule_project
            in zip(submodules, submodule_projects)
        ]
        self.assertTrue(all(
            isinstance(commit, ProjectCommit)
            for commit, _ in submodule_commits))
        self.assertEqual(
            {'aee2759733857e2d2c021c4f6127f7e8a908a3f2',  # fdroidclient
             'dcf7b47f9d0a194b16d21c567edd028d56d4b967',  # inkscape
             '238d1c01625e2e94e4733f30d5bf46018676a36f'},  # openRGB
            {commit.id for commit, _ in submodule_commits})
        self.assertTrue(all(is_exact for _, is_exact in submodule_commits))

    def test_get_submodule_commit_with_relative_urls(self):
        gl = Gitlab()
        inkscape = gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-relative-urls')
        submodules = list_project_submodules(inkscape, ref='main')
        submodule_projects = [
            submodule_to_project(submodule, gl.projects)
            for submodule in submodules[:4]]
        submodule_commits = [
            get_submodule_commit(
                submodule,
                submodule_project,
                get_latest_commit_possible_if_not_found=False)
            for submodule, submodule_project
            in zip(submodules, submodule_projects)
        ]
        self.assertTrue(all(
            isinstance(commit, ProjectCommit)
            for commit, _ in submodule_commits))
        self.assertEqual(
            {'e2c321d65e72d40c7a42f4a52117bd6f74c0bec6',  # 1
             '69dedd770bc4e02e2d674e5c9c4f8061bc3003df',  # 2
             '1addd49fad2cd096bd64cca2256b0c0ca92f1b58',  # 3
             '906828a297594114e3b1c48d2191eb31a91284c9'},  # 4
            {commit.id for commit, _ in submodule_commits})
        self.assertTrue(all(is_exact for _, is_exact in submodule_commits))
