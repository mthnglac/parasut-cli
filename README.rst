===========
Parasut CLI
===========


.. image:: https://img.shields.io/pypi/v/parasut-cli.svg
        :target: https://pypi.python.org/pypi/parasut-cli

.. image:: https://travis-ci.com/mthnglac/parasut-cli.svg?branch=master
    :target: https://travis-ci.com/mthnglac/parasut-cli

.. image:: https://readthedocs.org/projects/parasut-cli/badge/?version=latest
        :target: https://parasut-cli.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Parasut development environment consists of microservices and different
applications depending on them. **parasut-cli** is a CLI that facilitates you to
manage your workspaces and the applications you will run during development.


* Free software: MIT license
* Documentation: https://parasut-cli.readthedocs.io.


Features
--------

* Start command for preparing workspace with all necessary options.
* Link command for yarn linking operations. Also --undo action.
* Switch command for rails console actions.
* Run command for executing repo command chains manually.
* `rich`_ integrated.

.. _rich: https://github.com/willmcgugan/rich

TODO
----

* ``clone`` command for cloning repos in base directory.
* ``release`` & ``pre-release`` command.
* ``version`` command.
* unit tests.
* mypy & black connection to tox.
* linking state mechanism refactor.
* docs refactor.
