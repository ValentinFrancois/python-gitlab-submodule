from typing import Optional, Union

from gitlab.v4.objects import Project, ProjectCommit

from gitlab_submodule.string_utils import lstrip


class Submodule:

    def __init__(self,
                 parent_project: Project,
                 parent_ref: str,
                 name: str,
                 path: str,
                 url: str,
                 branch: Optional[str] = None,
                 ignore: Optional[str] = None,
                 update: Optional[str] = None,
                 recurse: bool = False,
                 shallow: bool = False):

        self.parent_project = parent_project
        self.parent_ref = parent_ref
        self.name = name
        self.path = path
        self.url = url
        self.branch = branch
        self.ignore = ignore
        self.update = update
        self.recurse = recurse
        self.shallow = shallow

    def keys(self):
        return {
            'parent_project', 'parent_ref', 'name', 'path', 'url',
            'update', 'branch', 'ignore', 'shallow', 'recurse'
        }

    def __getitem__(self, key):
        if key in self.keys():
            return getattr(self, key)
        else:
            raise KeyError(key)

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

    def __repr__(self):
        return '{} ({})'.format(
            self.__class__.__name__,
            ", ".join((
                repr(self.parent_project),
                repr(self.parent_ref),
                repr(self.name),
                repr(self.path),
                repr(self.url),
                repr(self.branch),
                repr(self.ignore),
                repr(self.update),
                repr(self.recurse),
                repr(self.shallow),
            ))
        )


class Commit:
    def __init__(self, _id) -> None:
        self.id = id


class Subproject:
    def __init__(self,
                 submodule: Submodule,
                 project: Optional[Project],
                 commit: Optional[Union[ProjectCommit, Commit]]):
        self.submodule = submodule
        self.project = project
        self.commit = commit

    def __getattribute__(self, item: str):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            for attribute in {'submodule', 'project', 'commit'}:
                if item.startswith(f'{attribute}_'):
                    return getattr(super().__getattribute__(attribute),
                                   lstrip(item, f'{attribute}_'))

        raise AttributeError("'{} object has no attribute '{}'".format(
            self.__class__.__name__, item))

    def __setattr__(self, key, value):
        for attribute in {'submodule', 'project', 'commit'}:
            if key == attribute:
                return super().__setattr__(key, value)
            if key.startswith(f'{attribute}_'):
                return setattr(getattr(self, attribute),
                               lstrip(key, f'{attribute}_'),
                               value)

        try:
            super().__setattr__(key, value)
        except AttributeError:
            raise AttributeError("'{} object has no attribute '{}'".format(
                self.__class__.__name__, key))

    def __str__(self):
        class_part = f"<class '{self.__class__.__name__}'>"
        attributes = [f"\n    '{key}': {getattr(self, key)}"
                      for key in ['submodule', 'project', 'commit']]
        return class_part + ' => {' + ','.join(attributes) + '\n}'

    def __repr__(self):
        return '{} (\n    {},\n    {},\n    {}\n)'.format(
            self.__class__.__name__,
            repr(self.submodule),
            repr(self.project),
            repr(self.commit),
        )
