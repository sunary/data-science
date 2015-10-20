__author__ = 'sunary'


import os
from setuptools import setup, find_packages


def __path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

build = 0
if os.path.exists(__path('build.info')):
    build = open(__path('build.info')).read().strip()

version = '1.0.{}'.format(build)

setup(
    name='data-science',
    version=version,
    description='Data science',
    author='Sunary',
    author_email='v2nhat@gmail.com',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
    ]
)