#!/usr/bin/env python
## INFO ##
## INFO ##

# Import python modules
# TODO: should use importlib instead of imp
import imp
import os.path

# Import SQLAlchemy-migrate modules
from migrate.versioning import api

# Import kibuwiki modules
from app import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO

# Modules level constants
_MESSAGE = 'New migration saved as {!r}\nCurrent database version is: {!r}'

#------------------------------------------------------------------------------#
def main():
    # Get current version and generate migration file name and location
    version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    migration = os.path.join(SQLALCHEMY_MIGRATE_REPO,
                             'versions',
                             '{:0>4}_migration.py'.format(version + 1))
    # Create the new migration script
    temp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI,
                                 SQLALCHEMY_MIGRATE_REPO)
    exec(old_model, temp_module.__dict__)
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                              SQLALCHEMY_MIGRATE_REPO,
                                              temp_module.meta,
                                              db.metadata)
    # Write migration script to a file
    with open(migration, 'w') as file:
        file.write(script)
    # Upgrade it, and get new version number
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    # Report back to user
    print(_MESSAGE.format(migration, version))


#------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
