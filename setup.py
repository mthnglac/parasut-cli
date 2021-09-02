#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'python-dotenv',
    'libtmux',
    'rich',
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Metehan Gulac",
    author_email=' metehanglc@protonmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="CLI for Parasut workspace management",
    entry_points={
        'console_scripts': [
            'parasut-cli=parasut_cli.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='parasut-cli',
    name='parasut-cli',
    packages=find_packages(include=['parasut_cli', 'parasut_cli.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mthnglac/parasut-cli',
    version='0.4.7',
    zip_safe=False,
)
