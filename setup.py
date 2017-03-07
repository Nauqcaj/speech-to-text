import os
import ast

from setuptools import setup
from setuptools.command.test import test as TestCommand

VALUES = {
    '__version__': None,
    '__title__': None,
    '__description__': None
}

with open('speech_to_text/__init__.py', 'r') as f:
    tree = ast.parse(f.read())
    for node in tree.body:
        if node.__class__ != ast.Assign:
            continue
        target = node.targets[0]
        if target.id in VALUES:
            VALUES[target.id] = node.value.s

if not all(VALUES.values()):
    raise RuntimeError("Can't locate values to init setuptools hook.")


version = VALUES['__version__']
project_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
package_name = 'speech_to_text'


def extract_requirements_from_file(req_file_name):
    with open(req_file_name, 'r') as fp:
        return [line.strip() for line in fp
                if line.strip() and not line.startswith('-r')]

requirements = extract_requirements_from_file('requirements.txt')
dev_requirements = (requirements +
                    extract_requirements_from_file('dev-requirements.txt'))

project_url = 'http://github.com/rmotr/{project_name}'.format(
    project_name=project_name)
# assert False, requirements

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["-s", "tests.py"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import sys
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name=VALUES['__title__'],
    version=version,
    description=VALUES['__description__'],
    url=project_url,
    download_url="{url}/tarball/{version}".format(
        url=project_url, version=version),
    author='Santiago Basulto',
    author_email='santiago@rmotr.com',
    license='MIT',
    scripts=['main.py'],
    packages=[package_name],
    maintainer='Santiago Basulto',
    install_requires=requirements,
    tests_require=dev_requirements,
    entry_points={
        'console_scripts': [
            'speech_to_text = main:speech_to_text'
        ]
    },
    zip_safe=True,
    cmdclass={'test': PyTest},
)
