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

* ``start`` command for preparing workspace with all necessary options.
* ``link`` command for yarn linking operations. Also --undo action.
* ``switch`` command for rails console actions.
* ``run`` command for executing repo command chains manually.
* ``release`` command for releasing version on related repo.
* ``pre-release`` flag for ``release`` command.
* `rich`_ integrated.

.. _rich: https://github.com/willmcgugan/rich

TODO
----

* ``clone`` command for cloning repos in base directory.
* unit tests.
* mypy & black connection to tox.
* linking state mechanism refactor.
