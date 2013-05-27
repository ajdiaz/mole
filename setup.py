#!/usr/bin/env python

import re

from setuptools import setup, find_packages
from os import path

MOLE_VERSION="0.1"

def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)
    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))
    return dependency_links


def get_file_contents(filename):
    fd = open(path.join(path.dirname(__file__), filename), "r")
    content = fd.read()
    fd.close()
    return content


def get_file_contents(filename):
    fd = open(path.join(path.dirname(__file__), filename), "r")
    content = fd.read()
    fd.close()
    return content

setup(
    name = "mole",
    version = MOLE_VERSION,
    description = "A flexible log analyzer and operational intelligence tool.",
    long_description=get_file_contents("README.rst"),
    author='Andres J. Diaz',
    author_email='ajdiaz@connectical.com',
    url='http://github.com/ajdiaz/mole',
    install_requires = parse_requirements('requirements.txt'),
    dependency_links = parse_dependency_links('requirements.txt'),
    packages=find_packages(),
    license="GPLv2",
    entry_points={
        'console_scripts': [
            'mole = mole.script.client:main',
            'mole-indexer = mole.script.indexer:main',
            'mole-seeker  = mole.script.seeker:main',
        ]
    },
    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 2.6',
          'Natural Language :: English',
    ],
)
