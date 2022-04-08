=======
History
=======


0.6.1 (2022-01-05)
-------------------

* switch option for Asist.

0.6.0 (2022-01-05)
-------------------

* FIX: ``--pre-release`` flag was broken. Also now flow was tested.

0.5.0 (2022-01-04)
-------------------

* FEATURE: ``--pre-release`` flag added to release command.
* UPDATE: docs improvements.

0.4.9 (2021-11-17)
-------------------

* UPDATE: add logic circle to switching frontend.
* ``PARASUT_PHOENIX_SWITCH_NAME`` environment variable changed as ``PARASUT_PHOENIX_SWITCH_APP_NAME``
* ``PARASUT_PHOENIX_SWITCH_OWNER_TYPE_NAME`` environment variable added.
* UPDATE: minor changes on linking

0.4.8 (2021-10-12)
-------------------

* DELETE: ``git push --tags`` command removed from release process; it is already done in "ember release" command.
* FEATURE: ``printX`` repo & its related logic & environments added.
* UPDATE: docs improvements

0.4.7 (2021-09-02)
-------------------

* UPDATE: "git push .." after release.

0.4.6 (2021-08-26)
-------------------

* FEATURE: new switch subcommand added: ``pricing_list``.
* UPDATE: docs improvements.
* UPDATE: minor bugs.

0.4.5 (2021-08-13)
-------------------

* FEATURE: ``--yes`` flag added for ember release auto login.

0.4.4 (2021-08-13)
-------------------

* BUG: auto release was working as manuel.
* UPDATE: docs improvements

0.4.3 (2021-08-13)
-------------------

* REFACTOR: release command logic
* UPDATE: ``--auto-login`` and ``--output`` options for release command
* UPDATE: docs improvements

0.4.2 (2021-08-12)
-------------------

* UPDATE: new core commands for releasing

0.4.1 (2021-05-06)
-------------------

* ``version`` command added.
* bug fixings.
* docs improvements.

0.4.0 (2021-05-04)
-------------------

* ``post-office`` repo added.
* ``ubl-validator`` repo added.
* ``release`` command added (beta).
* tox python3.5 deprecated
* dependency upgrades.
* editor workspace choosing node,ruby versions now in favor of editor actions.
* all version managers (rvm, yvm, nvm) deprecated in favor of `asdf`_ .
* docs improvements.

.. _asdf: https://asdf-vm.com

0.3.5 (2021-03-23)
-------------------

* UPDATE: rich integrated install script.
* UPDATE: docs improvements.

0.3.4 (2021-03-23)
-------------------

* FIX: run_process output fix.

0.3.3 (2021-03-19)
-------------------

* FIX: flake8 warnings.
* FIX: black warnings.

0.3.2 (2021-03-19)
-------------------

* UPDATE: Docs improvements

0.3.1 (2021-03-19)
-------------------

* UPDATE: Docs improvements
* DELETE: forgotten paremeters.

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
