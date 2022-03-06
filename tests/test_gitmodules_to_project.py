import unittest

from gitlab import Gitlab
from gitlab.v4.objects import Project

from gitlab_submodule.read_gitmodules import list_project_submodules
from gitlab_submodule.submodule_to_project import submodule_to_project


class TestGitmodulesToProject(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.gl = Gitlab()

    def test_get_submodules_as_projects_with_gitlab_absolute_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-absolute-urls')
        submodules = list_project_submodules(
            project,
            ref='ce9b1e50b34372d82df098f3ffded58ef4be03ec')
        submodule_projects = [
            submodule_to_project(submodule, self.gl.projects)
            for submodule in submodules]
        self.assertTrue(all(
            isinstance(project, Project)
            for project in submodule_projects))
        self.assertEqual(
            {'Client', 'OpenRGB', 'inkscape'},
            {project.name for project in submodule_projects})

    def test_get_submodules_as_projects_with_gitlab_relative_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/gitlab-relative-urls')
        submodules = list_project_submodules(project, ref='main')

        existing_submodule_projects = [
            submodule_to_project(submodule, self.gl.projects)
            for submodule in submodules[:4]]
        self.assertTrue(all(
            isinstance(project, Project)
            for project in existing_submodule_projects))
        self.assertEqual(
            {'1', '2', '3', '4'},
            {project.name for project in existing_submodule_projects})

        for submodule in submodules[4:]:
            with self.assertRaises(FileNotFoundError):
                submodule_to_project(submodule, self.gl.projects)

    def test_get_submodules_as_projects_with_external_urls(self):
        project = self.gl.projects.get(
            'python-gitlab-submodule-test/test-projects/external-urls')
        submodules = list_project_submodules(project)
        self.assertEqual(3, len(submodules))
        for submodule in submodules:
            self.assertIsNone(
                submodule_to_project(submodule, self.gl.projects))
