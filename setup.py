import sys

sys.path[0:0] = ['gitlab_submodule']

from __version__ import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md', 'r') as readme:
    readme_text = readme.read()
    readme_text = readme_text.split('## Contributing')[0]


setup(
    name='python-gitlab-submodule',
    description='python-gitlab-submodule : '
                'List project submodules and get the commits they point to '
                'with python-gitlab.',
    license='Apache License 2.0',
    version=__version__,
    author='Valentin François',
    maintainer='Valentin François',
    url='https://github.com/ValentinFrancois/python-gitlab-submodule',
    packages=['gitlab_submodule'],
    install_requires=[
       'python-gitlab>=3.0.0',
       'giturlparse>=0.10.0'
    ],
    long_description=readme_text,
    long_description_content_type='text/markdown',
    platforms=['any']
)
