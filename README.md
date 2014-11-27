kibuwiki
========

Logging, tracking, documenting, collaborating and communicationg -- are some of
the tasks `kibuwiki` (the wiki-based project management and documentation tool
developed by Peter Varo at [Kitchen Budapest](http://www.kibu.hu)) can help you
and your team to manage.

Get python:
-----------

> **NOTE:** On a Mac you need to install [homebrew](http://brew.sh) first.

On Mac OS X:

    $ brew install python3

On Arch Linux:

    # sudo pacman -S python tk python-pip python-setuptools

Install tools:
--------------

> **NOTE:** On a Mac it is `pip3`, on Arch Linux it is `pip` by default.

    $ pip3 install flask flask-login flask-openid flask-mail flask-sqlalchemy
      sqlalchemy-migrate flask-whooshalchemy flask-wtf flask-babel
      guess_language flipflop coverage

On Mac OS X:

    $ brew install pygit2

On Arch Linux:

    # sudo pacman -S python-pygit2

Run the server:
---------------

> **NOTE:** On a Mac you can run the script just as on a GNU/Linux distribution,
however to do that you have to create/change aliases: `python => python2` and
`python3 => python`. This is necessary, because `run.py`'s shebang is looking
for `python` without the version number suffix.

On Mac OS X:

    $ cd kibuwiki
    $ python3 run.py

On Arch Linux:

    # cd kibuwiki
    # chmod a+x run.py
    # ./run.py

Development Guide:
------------------

**Import Statements:** should always be ordered by importing core python modules
first, which should be followed by all the third-party modules and then user
modules should be the last to import.

*Example:*

    # Import python modules
    from itertools import zip_longest

    # Import flask modules
    from flask import flash

    # Import kibuwiki modules
    from app import db
