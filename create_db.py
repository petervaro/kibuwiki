#!/usr/bin/env python
## INFO ##
## INFO ##

# Import python modules
import os.path

# Import SQLAlchemy-migrate modules
from migrate.versioning import api

# Import kibuwiki modules
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from kibuwiki import database

#------------------------------------------------------------------------------#
def main():
    database.create_all()
    # If repo already exists
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    # If create from scratch
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI,
                            SQLALCHEMY_MIGRATE_REPO,
                            api.version(SQLALCHEMY_MIGRATE_REPO))


#------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
