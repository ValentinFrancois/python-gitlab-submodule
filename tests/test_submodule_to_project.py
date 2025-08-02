from unittest import TestCase
from unittest.mock import MagicMock

from gitlab import Gitlab
from gitlab.v4.objects import ProjectManager

from gitlab_submodule import Submodule
from gitlab_submodule.submodule_to_project import host_url_to_domain
from gitlab_submodule.submodule_to_project import (
    match_submodule_to_client_and_format_project_path)


def test_host_url_to_domain():
    assert host_url_to_domain("https://myhost.com/") == "myhost.com"


class TestSubmoduleToProject(TestCase):

    def mock_submodule(self, url: str) -> MagicMock:
        submodule = MagicMock(Submodule)
        submodule.url = url
        return submodule

    def test__submodule_url_to_path_with_namespace(self):
        # Normal gitlab host
        _, path_with_namespace = \
            match_submodule_to_client_and_format_project_path(
                self.mock_submodule('https://gitlab.com/namespace/repo.git'),
                gls=Gitlab()
            )
        self.assertEqual(path_with_namespace, 'namespace/repo')

        # Self-managed gitlab URL, wrong client
        match = match_submodule_to_client_and_format_project_path(
            self.mock_submodule('https://custom-gitlab/namespace/repo.git'),
            gls=Gitlab())
        self.assertEqual(match, None)

        # Self-managed gitlab URL that includes the URL of the wrong client
        match = \
            match_submodule_to_client_and_format_project_path(
                self.mock_submodule(
                    'https://custom-gitlab.com/namespace/repo.git'),
                gls=Gitlab()
            )
        self.assertEqual(match, None)

        # Self-managed gitlab URL with self_managed_gitlab_host
        self_hosted_client = MagicMock(ProjectManager)
        self_hosted_client.gitlab = MagicMock(Gitlab)
        self_hosted_client.gitlab._base_url = "https://custom-gitlab.com"
        client, path_with_namespace = \
            match_submodule_to_client_and_format_project_path(
                self.mock_submodule(
                    'https://custom-gitlab.com/namespace/repo.git'),
                gls=[Gitlab(), self_hosted_client],
            )
        self.assertEqual(path_with_namespace, 'namespace/repo')
        self.assertEqual(client, self_hosted_client)
