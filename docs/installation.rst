.. highlight:: shell

============
Installation
============


Dependency Setup
--------------

There are some dependencies we need to handle before running the cli.

It is necessary to install and configure the 3rd tools below:

* `Ember.js`_
* `Ruby on Rails`_
* `nvm`_ - node version manager
* `yvm`_ - yarn version manager
* `rvm`_ - ruby version manager
* `tmux`_ (if you will use start command)

.. _Ember.js: https://emberjs.com/
.. _Ruby on Rails: https://rubyonrails.org/
.. _nvm: https://github.com/nvm-sh/nvm
.. _yvm: https://yvm.js.org/
.. _rvm: https://rvm.io/


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
