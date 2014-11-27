## INFO ##
## INFO ##

# Import python modules
import os.path


# Module level constants
KIBUWIKI_BASEDIR = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'zHaFVRMT'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(KIBUWIKI_BASEDIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(KIBUWIKI_BASEDIR, 'db_repository')

OPENID_PROVIDERS = [{'name': 'Google',
                     'url' : 'https://www.google.com/accounts/o8/id'},
                    {'name': 'Yahoo',
                     'url' : 'https://me.yahoo.com'},
                    {'name': 'AOL',
                     'url' : 'http://openid.aol.com/<username>'},
                    {'name': 'Flickr',
                     'url' : 'http://www.flickr.com/<username>'},
                    {'name': 'MyOpenID',
                     'url' : 'https://www.myopenid.com'}]
