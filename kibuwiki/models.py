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

    ##- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    #def __init__(self):
    #    self._is_active = True
    #    self._is_anonymous = False
    #    self._is_authenticated = True

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        return '<User {!r}>'.format(self.nickname)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    ##- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    #@property
    #def is_authenticated(self):
    #    return self._is_authenticated
    #@is_authenticated.setter
    #def is_authenticated(self, status):
    #    self._is_authenticated = status

    ##- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    #@property
    #def is_active(self):
    #    return self._is_active
    #@is_active.setter
    #def is_active(self, value):
    #    self._is_active = value

    ##- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    #@property
    #def is_anonymous(self):
    #    return self._is_anonymous
    #@is_anonymous.setter
    #def is_anonymous(self, value):
    #    self._is_anonymous = value

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
