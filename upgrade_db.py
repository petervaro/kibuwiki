#!/usr/bin/env python
## INFO ##
## INFO ##

# Import SQLAlchemy modules
from migrate.versioning import api

# Import kibuwiki modules
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO

# Module level contstant
_MESSAGE = 'Current database version: {!r}'

# Upgrade and report back to user
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print(_MESSAGE.format(api.db_version(SQLALCHEMY_DATABASE_URI,
                                     SQLALCHEMY_MIGRATE_REPO)))
