=======
History
=======


0.3.0 (2021-03-19)
-------------------

* FEATURE: `rich`_ integrated. Plugin used in hidden commands.
* FEATURE: new ``--output`` parameter. ``switch`` and ``link`` command outputs are now hidden. To show their outputs, use ``--output`` prefix at the end of command chain.
* FIX: Yarn error situation was not working properly. Exception was not working. Also, CLI now gets angry for the third time.
* REFACTOR: subprocess structure has been rewritten. Inreractive terminal mode deprecated.

.. _rich: https://github.com/willmcgugan/rich

0.2.0 (2021-03-17)
-------------------

* CREATE: API Reference page added.
* CREATE: ``run`` command added.
* UPDATE: pkg updates.

0.1.16 (2021-03-09)
-------------------

* FIX: tmux exception problem when there is no server.

0.1.15 (2021-03-09)
-------------------

* REFACTOR: ``rails`` subcommand changed as ``frontend``.
* FIX: typos in core.
* FIX: dependencies now installing at installation.
* FIX: state mechanism refactored. There was a FileNotFoundError.
* FIX: ``start`` command now appending new windows existing session if you run start command in detached mode.
* UPDATE: note added to start command.

0.1.14 (2021-03-08)
-------------------

* Docs improvements

0.1.13 (2021-03-08)
-------------------

* Docs improvements


0.1.12 (2021-03-08)
-------------------

* Docs improvements


0.1.11 (2021-03-08)
-------------------

* Docs installation and usage page improvements.
* Sphinx upgrade.


0.1.10 (2021-03-07)
-------------------

* Docs improvements


0.1.9 (2021-03-07)
------------------

* Documents added on installation.
* Some minor fixings.
* Static type checker mypy added to requirements.
* Black code formatter used.


0.1.8 (2021-03-07)
------------------

* Theme changed
* Switch command refactored. added options: addlings, rails.
* Link command base repo argument required now.
* All important environments now coming outside of project.
* Cli now checking env variables; at exception.Keyerror situation, cli logging
  missing argument with warning.
* Start command refactored.
* Link list command shortening removed. at the moment only option is "--list".
* Parser indent fixed.
