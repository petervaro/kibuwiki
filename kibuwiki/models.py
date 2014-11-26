## INFO ##
## INFO ##

# Import kibuwiki modules
from kibuwiki import database

#------------------------------------------------------------------------------#
class User(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    nickname = database.Column(database.String(64), index=True, unique=True)
    email = database.Column(database.String(120), index=True, unique=True)
    posts = database.relationship('Post', backref='author', lazy='dynamic')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        self._active = True
        self._anonymous = False
        self._authenticated = True

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        return '<User {!r}>'.format(self.nickname)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def authenticated(self):
        return self._authenticated
    @authenticated.setter
    def authenticated(self, status):
        self._authenticated = status

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def active(self):
        return self._active
    @active.setter
    def active(self, value):
        self._active = value

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def anonymous(self):
        return self._anonymous
    @anonymous.setter
    def anonymous(self, value):
        self._anonymous = value

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # TODO: Make getter/setters prettier => is it possible, with the static
    #       typed id property of this class?
    def get_id(self):
        return str(self.id)


#------------------------------------------------------------------------------#
class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    body = database.Column(database.String(140))
    timestamp = database.Column(database.DateTime)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        return '<Post {} {!r}>'.format(self.timestamp, self.body)
