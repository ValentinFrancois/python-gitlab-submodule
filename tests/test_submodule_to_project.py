from unittest import TestCase
from unittest.mock import Mock

from gitlab_submodule.submodule_to_project import \
    _submodule_url_to_path_with_namespace


class TestSubmoduleToProject(TestCase):
    def test__submodule_url_to_path_with_namespace(self):
        # Normal gitlab host
        path_with_namespace = _submodule_url_to_path_with_namespace(
            'https://gitlab.com/namespace/repo.git',
            Mock())
        self.assertEqual(path_with_namespace, 'namespace/repo')

        # Self-managed gitlab URL without self_managed_gitlab_host
        path_with_namespace = _submodule_url_to_path_with_namespace(
            'https://custom-gitlab/namespace/repo.git',
            Mock())
        self.assertEqual(path_with_namespace, None)

        # Self-managed gitlab URL with self_managed_gitlab_host
        path_with_namespace = _submodule_url_to_path_with_namespace(
            'https://custom-gitlab/namespace/repo.git',
            Mock(),
            self_managed_gitlab_host='custom-gitlab')
        self.assertEqual(path_with_namespace, 'namespace/repo')
