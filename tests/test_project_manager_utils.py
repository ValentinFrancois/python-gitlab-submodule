from gitlab import Gitlab

from gitlab_submodule.project_manager_utils import get_host_url
from gitlab_submodule.project_manager_utils import map_domain_to_clients


def test_get_host_url():
    gl = Gitlab()
    assert get_host_url(gl.projects) == "https://gitlab.com"


def test_map_domain_to_clients():
    gl1 = Gitlab()
    gl2 = Gitlab("myhost.com").projects
    mapped = map_domain_to_clients([gl1, gl2])
    assert mapped == {
        "https://gitlab.com": gl1.projects,
        "myhost.com": gl2
    }
