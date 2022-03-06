import unittest

from gitlab_submodule.objects import Submodule, Subproject


class DictMock(dict):
    def __getattribute__(self, item):
        try:
            return self[item]
        except KeyError:
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        try:
            self[key] = value
        except KeyError:
            super().__setattr__(key, value)

    def __str__(self):
        keys = sorted(self.keys())
        class_part = f"<class '{self.__class__.__name__}'>"

        def to_str(key):
            if isinstance(self[key], str):
                return f"'{self[key]}'"
            else:
                return str(self[key])

        attributes = [f"'{key}': {to_str(key)}" for key in keys]
        return class_part + ' => {' + ', '.join(attributes) + '}'


class TestObjects(unittest.TestCase):

    def test_Submodule_as_dict(self):
        submodule = Submodule(
            parent_project=DictMock(),
            parent_ref='main',
            name='test_submodule',
            url='git@gitlab.com:test/submodule',
            path='include/test_submodule'
        )
        submodule_dict = dict(submodule)
        self.assertEqual(len(submodule_dict.keys()), 5)
        self.assertEqual(submodule_dict['parent_ref'], 'main')
        self.assertEqual(submodule_dict['name'], 'test_submodule')

    def test_Submodule_str(self):
        mock_project = DictMock()
        mock_project.id = 123456789
        submodule = Submodule(
            parent_project=mock_project,
            parent_ref='main',
            name='test_submodule',
            url='git@gitlab.com:test/submodule',
            path='include/test_submodule'
        )
        self.assertEqual(
            "<class 'Submodule'> => {"
            "'name': 'test_submodule', "
            "'parent_project': <class 'DictMock'> => {'id': 123456789}, "
            "'parent_ref': 'main', "
            "'path': 'include/test_submodule', "
            "'url': 'git@gitlab.com:test/submodule'}",
            str(submodule)
        )

    def test_Submodule_repr(self):
        mock_project = DictMock()
        mock_project.id = 123456789
        submodule = Submodule(
            parent_project=mock_project,
            parent_ref='main',
            name='test_submodule',
            url='git@gitlab.com:test/submodule',
            path='include/test_submodule'
        )
        self.assertEqual(
            "Submodule ({'id': 123456789}, 'main', 'test_submodule',"
            " 'include/test_submodule', 'git@gitlab.com:test/submodule')",
            repr(submodule)
        )

    def test_Subproject_get_attr(self):
        mock_parent_project = DictMock()
        mock_parent_project.id = '123456789'
        submodule = Submodule(
            parent_project=mock_parent_project,
            parent_ref='main',
            name='test_submodule',
            url='git@gitlab.com:test/submodule',
            path='include/test_submodule'
        )
        mock_project = DictMock()
        mock_project.name = 'project'
        mock_project.ssh_url = 'git@gitlab.com:test/project'

        mock_commit = DictMock()
        mock_commit.id = '123456789'

        project_submodule = Subproject(submodule, mock_project, mock_commit)

        self.assertEqual(project_submodule.project, mock_project)
        self.assertEqual(project_submodule.project.name, 'project')
        self.assertEqual(project_submodule.project_name, 'project')

        self.assertEqual(project_submodule.submodule, submodule)
        self.assertEqual(project_submodule.submodule.name, 'test_submodule')
        self.assertEqual(project_submodule.submodule_name, 'test_submodule')

        self.assertEqual(project_submodule.commit, mock_commit)
        self.assertEqual(project_submodule.commit.id, '123456789')
        self.assertEqual(project_submodule.commit_id, '123456789')

    def test_Subproject_set_attr(self):
        mock_parent_project = DictMock()
        mock_parent_project.id = '123456789'
        submodule = Submodule(
            parent_project=mock_parent_project,
            parent_ref='main',
            name='test_submodule',
            url='git@gitlab.com:test/submodule',
            path='include/test_submodule'
        )
        mock_project = DictMock()
        mock_project.name = 'project'
        mock_project.ssh_url = 'git@gitlab.com:test/project'

        mock_commit = DictMock()
        mock_commit.id = '123456789'

        project_submodule = Subproject(submodule, mock_project, mock_commit)

        project_submodule.project_name = 'project2'
        self.assertEqual(project_submodule.project_name, 'project2')
        self.assertEqual(project_submodule.project.name, 'project2')

        project_submodule.submodule_name = 'test_submodule2'
        self.assertEqual(project_submodule.submodule_name, 'test_submodule2')
        self.assertEqual(project_submodule.submodule.name, 'test_submodule2')

        project_submodule.commit_id = '0123456789'
        self.assertEqual(project_submodule.commit.id, '0123456789')
        self.assertEqual(project_submodule.commit_id, '0123456789')

        mock_project_3 = DictMock()
        mock_project_3.name = 'project3'
        project_submodule.project = mock_project_3
        self.assertEqual(project_submodule.project_name, 'project3')
        self.assertEqual(project_submodule.project.name, 'project3')

    def test_Subproject_str(self):
        mock_parent_project = DictMock()
        mock_parent_project.id = '123456789'
        submodule = Submodule(
            parent_project=mock_parent_project,
            parent_ref='main',
            name='test_submodule',
            url='git@gitlab.com:test/submodule',
            path='include/test_submodule'
        )
        mock_project = DictMock()
        mock_project.name = 'project'
        mock_project.ssh_url = 'git@gitlab.com:test/project'

        mock_commit = DictMock()
        mock_commit.id = '123456789'

        project_submodule = Subproject(submodule, mock_project, mock_commit)

        str_lines = str(project_submodule).split('\n')
        self.assertEqual(
            "<class 'Subproject'> => {",
            str_lines[0]
        )
        self.assertEqual(
            "    'submodule': <class 'Submodule'> => {"
            "'name': 'test_submodule', "
            "'parent_project': <class 'DictMock'> => {'id': '123456789'}, "
            "'parent_ref': 'main', "
            "'path': 'include/test_submodule', "
            "'url': 'git@gitlab.com:test/submodule'},",
            str_lines[1]
        )
        self.assertEqual(
            "    'project': <class 'DictMock'> => {'name': 'project', "
            "'ssh_url': 'git@gitlab.com:test/project'},",
            str_lines[2]
        )
        self.assertEqual(
            "    'commit': <class 'DictMock'> => {'id': '123456789'}",
            str_lines[3]
        )
        self.assertEqual('}', str_lines[4])

    def test_Subproject_repr(self):
        mock_parent_project = DictMock()
        mock_parent_project.id = '123456789'
        submodule = Submodule(
            parent_project=mock_parent_project,
            parent_ref='main',
            name='test_submodule',
            url='git@gitlab.com:test/submodule',
            path='include/test_submodule'
        )
        mock_project = DictMock()
        mock_project.name = 'project'
        mock_project.ssh_url = 'git@gitlab.com:test/project'

        mock_commit = DictMock()
        mock_commit.id = '123456789'

        project_submodule = Subproject(submodule, mock_project, mock_commit)

        str_lines = repr(project_submodule).split('\n')
        self.assertEqual(
            "Subproject (",
            str_lines[0]
        )
        self.assertEqual(
            "    Submodule ({'id': '123456789'}, 'main', "
            "'test_submodule', 'include/test_submodule', "
            "'git@gitlab.com:test/submodule'),",
            str_lines[1]
        )
        self.assertEqual(
            "    {'name': 'project', "
            "'ssh_url': 'git@gitlab.com:test/project'},",
            str_lines[2]
        )
        self.assertEqual(
            "    {'id': '123456789'}",
            str_lines[3]
        )
        self.assertEqual(')', str_lines[4])
