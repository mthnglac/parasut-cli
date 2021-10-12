.. highlight:: shell

============
Installation
============


Dependency Setup
----------------

There are some dependencies we need to handle before running the cli.

It is necessary to install and configure these third party tools below:

* `Ember.js`_
* `Ruby on Rails`_
* `asdf`_ - version manager
* tmux - terminal multiplexer
* `npm-cli-login`_ - npm auto login package (optional)

.. _Ember.js: https://emberjs.com/
.. _Ruby on Rails: https://rubyonrails.org/
.. _asdf: https://github.com/asdf-vm/asdf
.. _npm-cli-login: https://github.com/postmanlabs/npm-cli-login

.. warning::

    Before using the asdf version manager, you need to install the interpreters
    and their valid versions you will use (maven, nodejs, ruby, yarn):

    .. code-block:: console

        $ asdf plugin-add maven
        $ asdf install maven <version>
        $ asdf plugin-add nodejs
        $ asdf install nodejs <version>
        $ asdf plugin-add ruby
        $ asdf install ruby <version>
        $ asdf plugin-add yarn
        $ asdf install yarn <version>

.. note::

    **asdf** will create a file named ``.tool-versions`` in all your
    repositories while CLI is running. To have Git ignore these files, you can
    create a global ``.gitignore`` file and define this information in git.

    .. code-block:: console

        $ echo .tool-versions > ~/.gitignore
        $ git config --global core.excludesFile '~/.gitignore'


Workspace Structure
-------------------

Clone all repos into a folder that you will use as base. You get the idea.::

    parasutcom/          # Parasut Base Directory
        server/          # Server repo
        billing/         # Billing repo
        e-doc-broker/    # broker repo
        post-office/     # post-office repo
        printX/          # printX repo
        ubl-validator/   # ubl-validator repo
        phoenix/         # phoenix repo
        shared-logic/    # shared repo
        trinity/         # trinity repo
        ui-library/      # ui-library repo


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
    # npm registry
    export PARASUT_REGISTRY="..."
    export PARASUT_NPM_USERNAME="..."
    export PARASUT_NPM_PASSWORD="..."
    export PARASUT_NPM_EMAIL="..."
    # switch rails names
    export PARASUT_PHOENIX_SWITCH_NAME="..."
    export PARASUT_PHOENIX_SWITCH_PRICING_LIST_NAME="..."
    export PARASUT_TRINITY_SWITCH_NAME="..."
    export PARASUT_TRINITY_SWITCH_PRICING_LIST_NAME="..."
    # version & ports
    export PARASUT_SERVER_RUBY_V="..."
    export PARASUT_BILLING_RUBY_V="..."
    export PARASUT_BILLING_RAILS_PORT="..."
    export PARASUT_E_DOC_BROKER_RUBY_V="..."
    export PARASUT_E_DOC_BROKER_RAILS_PORT="..."
    export PARASUT_POST_OFFICE_RUBY_V="..."
    export PARASUT_POST_OFFICE_RAILS_PORT="..."
    export PARASUT_UBL_VALIDATOR_MAVEN_V="..."
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
    export PARASUT_PRINTX_NODE_V="..."
    export PARASUT_PRINTX_YARN_V="..."
    export PARASUT_PRINTX_EMBER_PORT="..."
    # structure variables
    export PARASUT_BASE_DIR="~/Code/development/parasutcom"
    export PARASUT_SERVER_DIR="server"
    export PARASUT_BILLING_DIR="billing"
    export PARASUT_E_DOC_BROKER_DIR="e-doc-broker"
    export PARASUT_POST_OFFICE_DIR="post-office"
    export PARASUT_UBL_VALIDATOR_DIR="ubl-validator"
    export PARASUT_PHOENIX_DIR="phoenix"
    export PARASUT_SHARED_LOGIC_DIR="shared-logic"
    export PARASUT_PRINTX_DIR="printX"
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
