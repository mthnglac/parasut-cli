=======
History
=======


0.1.15 (2021-08-27)
-------------------

* REFACTOR: ``rails`` subcommand changed as ``frontend``.
* FIX: typos in core.
* FIX: dependencies now installing at installation.
* FIX: state mechanism refactored. There was a FileNotFoundError.
* FIX: ``start`` command now appending new windows existing session if you run start command in detached mode.
* UPDATE: note added to start command.

0.1.14 (2021-08-27)
-------------------

* Docs improvements

0.1.13 (2021-08-27)
-------------------

* Docs improvements


0.1.12 (2021-08-27)
-------------------

* Docs improvements


0.1.11 (2021-08-27)
-------------------

* Docs installation and usage page improvements.
* Sphinx upgrade.


0.1.10 (2021-07-27)
-------------------

* Docs improvements


0.1.9 (2021-07-27)
------------------

* Documents added on installation.
* Some minor fixings.
* Static type checker mypy added to requirements.
* Black code formatter used.


0.1.8 (2021-07-27)
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
