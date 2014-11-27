## INFO ##
## INFO ##

# FIXME: OpenID2.0 will not work with Google from April 20, 2015
#        kibuwiki should use OpenID Connect instead. For more info:
#        https://support.google.com/accounts/answer/6135882

# Import flask modules
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

# Import kibuwiki modules
from kibuwiki.models import User
from kibuwiki.forms import LoginForm
from kibuwiki import app, database, login_manager, open_id

#------------------------------------------------------------------------------#
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


#------------------------------------------------------------------------------#
@app.before_request
def before_request():
    g.user = current_user


#------------------------------------------------------------------------------#
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#------------------------------------------------------------------------------#
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    # Fake data:
    posts = [{'author': {'nickname': 'aliznagy'},
              'body'  : 'this is my first test post'},
             {'author': {'nickname': 'laszlokiss'},
              'body'  : 'aaaand this is the second one!'}]

    return render_template('index.html',
                           title='home',
                           user=user,
                           posts=posts)


#------------------------------------------------------------------------------#
@app.route('/login', methods=['GET', 'POST'])
@open_id.loginhandler
def login():
    # Get local reference
    user = g.user
    # If user is already logged in
    if user is not None and user.is_authenticated():
        return redirect(url_for('index'))
    # If user is not logged in
    form = LoginForm()
    # If user is submitting
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return open_id.try_login(form.openid.data, ask_for=['nickname', 'email'])
    # No submitting and not logged in
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


#------------------------------------------------------------------------------#
@open_id.after_login
def after_login(response):
    # Get local reference
    email = response.email
    # If email is not valid
    # TODO: clean up these conditionals
    #       => email, user and nickname => check for possible values?
    if not email: # email is None or email == '':
        flash('Invalid login. PLease try again.')
        return redirect(url_for('login'))
    # Check if user is in database
    user = User.query.filter_by(email=email).first()
    # If not in database
    if not user: # user is None:
        # Register nickname
        nickname = response.nickname
        if not nickname: # nickname is None or nickname == '':
            nickname, *rest = email.split('@')
        user = User(nickname=nickname, email=email)
        database.session.add(user)
        database.session.commit()

    # Set remember_me option for the user
    try:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    except KeyError:
        remember_me = False

    # Log in and redirect the user to the "next" page (previously required
    # while the user was not logged in) or if there wasn't any request before
    # the user will be redirected to the index page
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


#------------------------------------------------------------------------------#
@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        flash('User {} not found.'.format(nickname))
        return redirect(url_for('index'))
    posts = [{'author': user, 'body': 'Test post #1'},
             {'author': user, 'body': 'Test post #2'},
             {'author': user, 'body': 'Test post #3'}]
    return render_template('user.html',
                           user=user,
                           posts=posts)
