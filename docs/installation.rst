.. highlight:: shell

============
Installation
============


Dependency Setup
----------------

There are some dependencies we need to handle before running the cli.

It is necessary to install and configure the 3rd tools below:

* `Ember.js`_
* `Ruby on Rails`_
* `nvm`_ - node version manager
* `yvm`_ - yarn version manager
* `rvm`_ - ruby version manager
* tmux - terminal multiplexer

.. _Ember.js: https://emberjs.com/
.. _Ruby on Rails: https://rubyonrails.org/
.. _nvm: https://github.com/nvm-sh/nvm
.. _yvm: https://yvm.js.org/
.. _rvm: https://rvm.io/


Workspace Structure
-------------------

Clone all repos into a folder that you will use as base. You get the idea.::

    parasutcom/          # Parasut Base Directory
        server/          # Server repo
        billing/         # Billing repo
        e-doc-broker/    # broker repo
        phoenix/         # phoenix repo
        shared-logic/    # shared repo
        trinity/         # trinity repo
        ui-library/      # ui repo


Environment Variables
---------------------

CLI only need these certain ``environment variables`` while working. You need
to define them in your local shell configuration. As long as you pay attention
here, everything goes well on CLI. Briefly define the following variables:

.. code-block:: console

    # parasut-cli text editor
    export PARASUT_CLI_TEXT_EDITOR="vim"
    # company id
    export PARASUT_COMPANY_ID="..."
    # switch rails names
    export PARASUT_PHOENIX_SWITCH_NAME="..."
    export PARASUT_TRINITY_SWITCH_NAME="..."
    # version & ports
    export PARASUT_SERVER_RUBY_V="..."
    export PARASUT_BILLING_RUBY_V="..."
    export PARASUT_BILLING_RAILS_PORT="..."
    export PARASUT_E_DOC_BROKER_RUBY_V="..."
    export PARASUT_E_DOC_BROKER_RAILS_PORT="..."
    export PARASUT_PHOENIX_NODE_V="..."
    export PARASUT_PHOENIX_YARN_V="..."
    export PARASUT_CLIENT_NODE_V="..."
    export PARASUT_CLIENT_YARN_V="..."
    export PARASUT_CLIENT_EMBER_PORT="..."
    export PARASUT_TRINITY_NODE_V="..."
    export PARASUT_TRINITY_YARN_V="..."
    export PARASUT_TRINITY_EMBER_PORT="..."
    export PARASUT_UI_LIBRARY_NODE_V="..."
    export PARASUT_UI_LIBRARY_YARN_V="..."
    export PARASUT_UI_LIBRARY_EMBER_PORT="..."
    export PARASUT_SHARED_LOGIC_NODE_V="..."
    export PARASUT_SHARED_LOGIC_YARN_V="..."
    export PARASUT_SHARED_LOGIC_EMBER_PORT="..."
    # structure variables
    export PARASUT_BASE_DIR="~/Code/development/parasutcom"
    export PARASUT_SERVER_DIR="server"
    export PARASUT_BILLING_DIR="billing"
    export PARASUT_E_DOC_BROKER_DIR="e-doc-broker"
    export PARASUT_PHOENIX_DIR="phoenix"
    export PARASUT_SHARED_LOGIC_DIR="shared-logic"
    export PARASUT_CLIENT_DIR="client"
    export PARASUT_TRINITY_DIR="trinity"
    export PARASUT_UI_LIBRARY_DIR="ui-library"

.. warning::

    CLI using text editor like ``vim, nvim, emacs, nano`` while executing
    ``start`` command for launching tmux server. It will try to open editor in
    tmux window. Don't use anything else. If you're using IDE or something else
    that work outside of terminal, just skip ``-e/--edit`` partition of
    ``start`` command.


Stable release
--------------

To install Parasut CLI, run this command in your terminal:

.. code-block:: console

    $ pip install parasut-cli

This is the preferred method to install Parasut CLI, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for Parasut CLI can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/mthnglac/parasut-cli

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/mthnglac/parasut-cli/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/mthnglac/parasut-cli
.. _tarball: https://github.com/mthnglac/parasut-cli/tarball/master
