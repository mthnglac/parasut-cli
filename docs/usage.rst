=====
Usage
=====

Start Command
--------------

This is where the CLI does its magic. It creates two sessions from repos given
using tmux and builds workspaces into them.

.. code-block:: console

    $ parasut-cli start -e <repo-name> -s <repo-name>


* ``-e/--edit`` - a repository name to open in text editor. Choices: server, billing, phoenix, shared-logic, trinity, ui-library, client, e-doc-broker.

* ``-s/--setup`` - a repository name to launch. Choices: server, billing, phoenix, shared-logic, trinity, ui-library, client, e-doc-broker.


Link Command
--------------

This command does the linking work of yarn. It takes the given argument and
writes it to package.json in the current repo for you. It also includes a logic
so that you can undo any changes you have made later ``(-u/--undo)``.

.. code-block:: console

    $ parasut-cli link -b <repo-name> -t <repo-name>


* ``-b/--base`` - a repository name for linking target repository. Use this with ``-t/--target`` option. Choices: phoenix, trinity.

* ``-t/--target`` - a target repository name for linking it to base repository. Choices: ui-library, shared-logic.

* ``-u/--undo`` - a repository name for unlinking. Choices: ui-library, shared-logic.

* ``--list`` - a repository name for unlinking it list linked repos of base repo.

.. note::

    -b/--base argument is necessary. Command will continue to ask until the
    required base repo is given.


Switch Command
--------------

This part can be a little confusing. It represents exactly what it does.
Switch processes run on the ``server``. What the command does is to
automate processes that are executed interactively in the background.

.. code-block:: console

    $ parasut-cli switch <switch-name> -t <switch-choice>


* ``rails`` - a repository name to switch rails frontend repo on server.

    * ``-t/--target`` - target prefix for choosing choices. Choices: phoenix, trinity.

* ``addlings`` - command for switching addlings.

    * ``-t/--target`` - target prefix for choosing choices. Choices: receipt, invoice.


Help Command
--------------

Generally, the CLI will not make you do anything against the rules and will
give you the necessary warnings when the time comes. If you are confused, type
``-h/--help`` at the end of your chain of commands:

.. code-block:: console

    $ parasut-cli -h
    $ parasut-cli start --help
    $ parasut-cli start -b <repo-name> --help
    $ parasut-cli switch --help
