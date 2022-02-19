# python-gitlab-submodule
List project submodules and get the commits they point to with python-gitlab.


The [Gitlab REST API V4](https://docs.gitlab.com/ee/api/api_resources.html) 
doesn't implement anything for submodule inspection yet. The only thing we can 
currently do is [updating a submodule to a new commit id](https://docs.gitlab.com/ee/api/repository_submodules.html),
but how can we trigger such an update if we don't know the current commit id 
of our submodule?

If you're using `python-gitlab` and you're distributing shared code among 
your projects with submodules, you've probably run into this issue already.

This package provides minimal utils to list the submodules present in a 
Gitlab project, and more importantly to get the commits they're pointing to 
(when the submodules are Gitlab projects themselves, otherwise we cannot 
access the project via their URLs using `python-gitlab` only).

Internally, it reads and parses the `.gitmodules` file at the root of the 
Project. To get the commit id of a submodule, it finds the last commit that 
updated the submodule and parses its diff.

## Requirements
- Python >= __3.7__ (required by `python-gitlab` since version `3.0.0`)

## Dependencies
- [python-gitlab](https://github.com/python-gitlab/python-gitlab)
- [giturlparse](https://github.com/nephila/giturlparse)

## Install
```
pip install python-gitlab-gitmodule
```
or directly from Github:
```
pip install git+git://github.com/ValentinFrancois/python-gitlab-submodule#egg=python-gitlab-submodule
```

## Usage example
### 1)
- Iterate over the submodules of the Gitlab [Inkscape](https://gitlab.com/inkscape/inkscape) project
- For each submodule, print:
  - its path in the project
  - its own Gitlab project SSH URL
  - the current commit sha that the Inkscape project is pointing to
```python
from gitlab import Gitlab
from gitlab_submodule import iterate_subprojects

gl = Gitlab()
inkscape = gl.projects.get('inkscape/inkscape')
subprojects = iterate_subprojects(
    inkscape,
    gl,
    # current HEAD of master as I'm writing this
    ref='e371b2f826adcba316f2e64bbf2f697043373d0b')
for subproject in subprojects:
    print('- {} ({}) -> {}'.format(
        subproject.submodule.path, 
        subproject.project.web_url, 
        subproject.commit.id))
```
Output:
```
- share/extensions (git@gitlab.com:inkscape/extensions.git) -> 6c9b68507be427bffba23507bbaacf3f8a0f3752
- src/3rdparty/2geom (git@gitlab.com:inkscape/lib2geom.git) -> 9d38946b7d7a0486a4a75669008112d306309d9e
- share/themes (git@gitlab.com:inkscape/themes.git) -> 2fc6ece138323f905c9b475c3bcdef0d007eb233
```

### 2)
- Iterate over the submodules of the Gitlab [Inkscape](https://gitlab.com/inkscape/inkscape) project
- For each submodule, print:
  - its path in the project
  - if its commit is up-to-date with the HEAD of the main branch of the 
    subproject
```diff
for subproject in subprojects:
-    print('- {} ({}) -> {}'.format(
-        subproject.submodule.path, 
-        subproject.project.web_url, 
-        subproject.commit.id))
+    head_subproject_commit = subproject.project.commits.list(
+        ref=subproject.project.default_branch)[0]
+    up_to_date = subproject.commit.id == head_subproject_commit.id
+    print('- {}: {}'.format(
+        subproject.submodule.path,
+        'ok' if up_to_date else '/!\\ must update'))

```
Output:
```
- share/extensions: /!\ must update
- src/3rdparty/2geom: ok
- share/themes: ok
```

## Available functions and objects

### `iterate_subprojects(...)`
What you'll probably use most of the time.<br/>
- Yields [`Subproject`](#class-subproject) objects that describe the submodules.
- Ignores submodules that are not hosted on Gitlab. If you want to list all 
  modules present in the `.gitmodules` file but without mapping them to 
  `gitlab.v4.objects.Project` objects, use [`list_submodules(...)`](#list_submodules) instead.
```python
iterate_subprojects(
    project: Project,
    gl: Union[Gitlab, ProjectManager],
    ref: Optional[str] = None,
    get_latest_commit_possible_if_not_found: bool = False,
    get_latest_commit_possible_ref: Optional[str] = None
) -> Generator[Subproject, None, None]
```
Parameters:
- `project`: a `gitlab.v4.objects.Project` object
- `gitlab`: the `gitlab.Gitlab` instance that you used to authenticate, or its 
  `projects: gitlab.v4.objects.ProjectManager` attribute
- `ref`: (optional) a ref to a branch, commit, tag etc. Defaults to the 
  HEAD of the project default branch.
- `get_latest_commit_possible_if_not_found`: in some rare cases, there 
  won't be any `Subproject commit ...` info in the diff of the last commit 
  that updated the submodules. Set this option to `True` if you want to get 
  instead the most recent commit in the subproject that is anterior to the 
  commit that updated the submodules of the project. If your goal is to 
  check that your submodules are up-to-date, you might want to use this.
- `get_latest_commit_possible_ref`: in case you set 
  `get_latest_commit_possible_if_not_found` to `True`, you can specify a ref for the 
  subproject (for instance your submodule could point to a different branch 
  than the main one). By default, the main branch of the subproject will be 
  used.

Returns: Generator of `Subproject` objects

### `list_subprojects(...)`
Same parameters as [`iterate_subprojects(...)`](#iterate_subprojects) but 
returns a `list` of [`Subproject`](#class-subproject) objects.

### class `Subproject`
Basic objects that contain the info about a Gitlab subproject.

Attributes:
- `project: gitlab.v4.objects.Project`: the Gitlab project that the submodule links to
- `submodule: `[`Submodule`](#class-submodule): a basic object that contains 
  the info found in the `.gitmodules` file (name, path, url).
- `commit: gitlab.v4.objects.ProjectCommit`: the commit that the submodule points to
- `commit_is_exact: bool`: `True` most of the time, `False` only if the commit 
  had to be guessed via the `get_latest_commit_possible_if_not_found` option

Example `str()` output:
```
<class 'Subproject'> => {
    'submodule': <class 'Submodule'> => {'name': 'share/extensions', 'parent_project': <class 'gitlab.v4.objects.projects.Project'> => {'id': 3472737, 'description': 'Inkscape vector image editor', 'name': 'inkscape', 'name_with_namespace': 'Inkscape / inkscape', 'path': 'inkscape', 'path_with_namespace': 'inkscape/inkscape', 'created_at': '2017-06-09T14:16:35.615Z', 'default_branch': 'master', 'tag_list': [], 'topics': [], 'ssh_url_to_repo': 'git@gitlab.com:inkscape/inkscape.git', 'http_url_to_repo': 'https://gitlab.com/inkscape/inkscape.git', 'web_url': 'https://gitlab.com/inkscape/inkscape', 'readme_url': 'https://gitlab.com/inkscape/inkscape/-/blob/master/README.md', 'avatar_url': 'https://gitlab.com/uploads/-/system/project/avatar/3472737/inkscape.png', 'forks_count': 900, 'star_count': 2512, 'last_activity_at': '2022-01-29T23:45:49.894Z', 'namespace': {'id': 470642, 'name': 'Inkscape', 'path': 'inkscape', 'kind': 'group', 'full_path': 'inkscape', 'parent_id': None, 'avatar_url': '/uploads/-/system/group/avatar/470642/inkscape.png', 'web_url': 'https://gitlab.com/groups/inkscape'}}, 'parent_ref': 'e371b2f826adcba316f2e64bbf2f697043373d0b', 'path': 'share/extensions', 'url': 'https://gitlab.com/inkscape/extensions.git'},
    'project': <class 'gitlab.v4.objects.projects.Project'> => {'id': 5833962, 'description': 'Python extensions for Inkscape core, separated out from main repository.', 'name': 'extensions', 'name_with_namespace': 'Inkscape / extensions', 'path': 'extensions', 'path_with_namespace': 'inkscape/extensions', 'created_at': '2018-03-22T00:29:09.053Z', 'default_branch': 'master', 'tag_list': ['addin', 'additional', 'addon', 'core', 'extension', 'inkscape', 'python'], 'topics': ['addin', 'additional', 'addon', 'core', 'extension', 'inkscape', 'python'], 'ssh_url_to_repo': 'git@gitlab.com:inkscape/extensions.git', 'http_url_to_repo': 'https://gitlab.com/inkscape/extensions.git', 'web_url': 'https://gitlab.com/inkscape/extensions', 'readme_url': 'https://gitlab.com/inkscape/extensions/-/blob/master/README.md', 'avatar_url': 'https://gitlab.com/uploads/-/system/project/avatar/5833962/addons.png', 'forks_count': 89, 'star_count': 41, 'last_activity_at': '2022-01-29T19:10:13.502Z', 'namespace': {'id': 470642, 'name': 'Inkscape', 'path': 'inkscape', 'kind': 'group', 'full_path': 'inkscape', 'parent_id': None, 'avatar_url': '/uploads/-/system/group/avatar/470642/inkscape.png', 'web_url': 'https://gitlab.com/groups/inkscape'}},
    'commit': <class 'gitlab.v4.objects.commits.ProjectCommit'> => {'id': '6c9b68507be427bffba23507bbaacf3f8a0f3752', 'short_id': '6c9b6850', 'created_at': '2021-11-28T22:23:47.000+00:00', 'parent_ids': ['fdda3f18b3ddda61a19f5046ce21a6e2147791f5', '8769b39a55f94d42ac0d9b24757540a88f2865cc'], 'title': "Merge branch 'add-issue-template-bug-report' into 'master'", 'message': "Merge branch 'add-issue-template-bug-report' into 'master'\n\nadd issue template for GitLab for bug reports\n\nSee merge request inkscape/extensions!377", 'author_name': 'Martin Owens', 'author_email': 'doctormo@geek-2.com', 'authored_date': '2021-11-28T22:23:47.000+00:00', 'committer_name': 'Martin Owens', 'committer_email': 'doctormo@geek-2.com', 'committed_date': '2021-11-28T22:23:47.000+00:00', 'trailers': {}, 'web_url': 'https://gitlab.com/inkscape/extensions/-/commit/6c9b68507be427bffba23507bbaacf3f8a0f3752', 'stats': {'additions': 25, 'deletions': 0, 'total': 25}, 'status': 'success', 'project_id': 5833962, 'last_pipeline': {'id': 417958828, 'iid': 924, 'project_id': 5833962, 'sha': '6c9b68507be427bffba23507bbaacf3f8a0f3752', 'ref': 'master', 'status': 'success', 'source': 'push', 'created_at': '2021-11-28T22:23:48.313Z', 'updated_at': '2021-11-28T22:31:49.083Z', 'web_url': 'https://gitlab.com/inkscape/extensions/-/pipelines/417958828'}, 'is_exact': True}
}
```

### `list_submodules(...)`
Lists the info about the project submodules found in the `.gitmodules` file.
```python
list_project_submodules(
    project: Project,
    ref: Optional[str] = None) -> List[Submodule]
```
Parameters:
- `project`: a `gitlab.v4.objects.Project` object
- `ref`: (optional) a ref to a branch, commit, tag etc. Defaults to the 
  HEAD of the project default branch.

Returns: list of `Submodule` objects

### class `Submodule`
Represents the `.gitmodules` config of a submodule + adds info about the 
parent project

Attributes:
- `parent_project: gitlab.v4.objects.Project`: project that uses the submodule
- `parent_ref: str`: ref where the `.gitmodules` file was read
- `name: str`: local name used by git for the submodule
- `path: str`: local path pointing to the submodule directory in the project
- `url: str`: URL linking to the location of the repo of the submodule (not 
  necessarily Gitlab)

Example `str()` output:
```
<class 'Submodule'> => {'name': 'share/extensions', 'parent_project': <class 'gitlab.v4.objects.projects.Project'> => {'id': 3472737, 'description': 'Inkscape vector image editor', 'name': 'inkscape', 'name_with_namespace': 'Inkscape / inkscape', 'path': 'inkscape', 'path_with_namespace': 'inkscape/inkscape', 'created_at': '2017-06-09T14:16:35.615Z', 'default_branch': 'master', 'tag_list': [], 'topics': [], 'ssh_url_to_repo': 'git@gitlab.com:inkscape/inkscape.git', 'http_url_to_repo': 'https://gitlab.com/inkscape/inkscape.git', 'web_url': 'https://gitlab.com/inkscape/inkscape', 'readme_url': 'https://gitlab.com/inkscape/inkscape/-/blob/master/README.md', 'avatar_url': 'https://gitlab.com/uploads/-/system/project/avatar/3472737/inkscape.png', 'forks_count': 900, 'star_count': 2512, 'last_activity_at': '2022-01-29T23:45:49.894Z', 'namespace': {'id': 470642, 'name': 'Inkscape', 'path': 'inkscape', 'kind': 'group', 'full_path': 'inkscape', 'parent_id': None, 'avatar_url': '/uploads/-/system/group/avatar/470642/inkscape.png', 'web_url': 'https://gitlab.com/groups/inkscape'}}, 'parent_ref': 'e371b2f826adcba316f2e64bbf2f697043373d0b', 'path': 'share/extensions', 'url': 'https://gitlab.com/inkscape/extensions.git'}
```

### `submodule_to_subproject(...)`
Converts a `Submodule` object to a [`Subproject`](#class-subproject) object, assuming it's 
hosted on Gitlab.

```python
submodule_to_subproject(
    gitmodules_submodule: Submodule,
    gl: Union[Gitlab, ProjectManager],
    get_latest_commit_possible_if_not_found: bool = False,
    get_latest_commit_possible_ref: Optional[str] = None
) -> Subproject
```
Parameters: See [`iterate_subprojects(...)`](#iterate_subprojects)
