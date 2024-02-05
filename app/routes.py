from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app import db
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    """Renders the Index/Home Template to the 
    Homepage API endpoint of the app"""
    user = {'username':'Davy'}
    posts = [
        {
            'author': {'username': 'ThyFather'},
            'body': 'Beautiful day in Nairobii!'
        },
        {
            'author': {'username': 'Florian'},
            'body': 'James Cameron`s Avatar is the Ishh'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """logs In a User by Verification"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """Logs out an Active User"""
    logout_user()
    return redirect(url_for('index'))
