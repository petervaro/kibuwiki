## INFO ##
## INFO ##

from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname':  'petervaro'}
    posts = [        {
            'author': {'nickname': 'aliznagy'},
            'body': 'this is my first test post'
        },
        {
            'author': {'nickname': 'laszlokiss'},
            'body': 'aaaand this is the second one!'
        }
    ]
    return render_template('index.html',
                           title='home',
                           user=user,
                           posts=posts)


FLASH = 'Login requested for OpenID={}, remember_me={}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(FLASH.format(form.openid.data,
                           str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
