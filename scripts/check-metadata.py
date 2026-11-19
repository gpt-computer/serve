#!/usr/bin/env python3
"""Validate that packaging metadata agrees across the repository."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding='utf-8')


def require(condition, message):
    if not condition:
        errors.append(message)


init_py = read('gptc/__init__.py')
pyproject = read('pyproject.toml')
setup_py = read('setup.py')
conda_recipe = read('conda/meta.yaml')
extras = read('extra-requirements.txt')
workflows = '\n'.join(
    p.read_text(encoding='utf-8')
    for p in (ROOT / '.github' / 'workflows').glob('*.yml')
)

version = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)", init_py, re.M).group(1)
conda_version = re.search(r'\{%\s*set version = "([^"]+)"', conda_recipe).group(1)
require(
    version == conda_version,
    f'conda version {conda_version} != package version {version}',
)
project_version = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M).group(1)
require(
    project_version == version,
    f'pyproject.toml version {project_version} != package version {version}',
)

requires_python = re.search(r'^requires-python\s*=\s*"([^"]+)"', pyproject, re.M).group(
    1
)
require('>=3.10' in requires_python, f'unexpected requires-python: {requires_python}')
require('python >=3.8' in conda_recipe, 'conda recipe must require python >=3.8')
require('Python :: 3.7' not in setup_py, 'setup.py still advertises Python 3.7')
require(
    '"Programming Language :: Python :: 3.12"' in pyproject,
    'pyproject.toml must advertise Python 3.12',
)

require(
    "gptc = \"gptc_cli:main\"" in pyproject, 'pyproject.toml console script must be gptc_cli:main'
)
require(
    'gptc = gptc_cli:main' in conda_recipe, 'conda entry point must be gptc_cli:main'
)

tags = set()
for line in extras.splitlines():
    if line.strip() and not line.startswith('#') and ':' in line:
        tags.update(tag.strip() for tag in line.split(':', 1)[1].split(','))
require(
    'standrad' not in tags,
    'extra-requirements.txt contains the misspelled tag "standrad"',
)
require('standard' in tags, 'extra-requirements.txt has no "standard" tag')
require('common' not in workflows, 'workflows reference the undefined "common" extra')

if errors:
    print('Metadata consistency check failed:')
    for error in errors:
        print(f'  - {error}')
    sys.exit(1)

print(f'Metadata consistent (version {version}, Python {requires_python}).')
