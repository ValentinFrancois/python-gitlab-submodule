try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='python-gitlab-submodule',
    description='python-gitlab-submodule : '
                'List project submodules and get the commits they point to '
                'with python-gitlab.',
    license='Apache License 2.0',
    version='0.1.0',
    author='Valentin François',
    maintainer='Valentin François',
    url='https://github.com/ValentinFrancois/python-gitlab-submodule',
    packages=['gitlab_submodule'],
    install_requires=[
       'python-gitlab>=3.1.0',
       'giturlparse>=0.10.0'
    ]
)