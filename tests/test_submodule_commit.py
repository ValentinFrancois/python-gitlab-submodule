import unittest

from gitlab import Gitlab
from gitlab.v4.objects import ProjectCommit

from gitlab_submodule.read_gitmodules import list_project_submodules
from gitlab_submodule.gitmodules_to_project import gitmodules_to_project
from gitlab_submodule.submodule_commit import (get_submodule_commit,
                                               _get_submodule_commit_id)


class TestSubmoduleCommit(unittest.TestCase):

    def test_get_inkscape_submodules_commit_ids(self):
        gl = Gitlab()
        inkscape = gl.projects.get('inkscape/inkscape')
        submodules = list_project_submodules(
            inkscape,
            ref='e371b2f826adcba316f2e64bbf2f697043373d0b'
        )
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
            {'9d38946b7d7a0486a4a75669008112d306309d9e',
             '6c9b68507be427bffba23507bbaacf3f8a0f3752',
             '2fc6ece138323f905c9b475c3bcdef0d007eb233'},
            {commit_id for commit_id, _ in submodule_commit_ids}
        )
        self.assertTrue(all(is_exact for _, is_exact in submodule_commit_ids))

    def test_get_inkscape_submodules_commits(self):
        gl = Gitlab()
        inkscape = gl.projects.get('inkscape/inkscape')
        submodules = list_project_submodules(
            inkscape,
            ref='e371b2f826adcba316f2e64bbf2f697043373d0b'
        )
        submodule_projects = [
            gitmodules_to_project(submodule) for submodule in submodules
        ]
        submodule_commits = [
            get_submodule_commit(
                submodule,
                submodule_project,
                get_latest_commit_possible_if_not_found=False
            )
            for submodule, submodule_project
            in zip(submodules, submodule_projects)
        ]
        self.assertTrue(all(
            isinstance(commit, ProjectCommit)
            for commit, _ in submodule_commits
        ))
        self.assertEqual(
            {'9d38946b7d7a0486a4a75669008112d306309d9e',
             '6c9b68507be427bffba23507bbaacf3f8a0f3752',
             '2fc6ece138323f905c9b475c3bcdef0d007eb233'},
            {commit.id for commit, _ in submodule_commits}
        )
        self.assertTrue(all(is_exact for _, is_exact in submodule_commits))
