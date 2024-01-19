from flask import render_template
from app import app
from app.forms import LoginForm

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


@app.route('/login')
def login():
    """Renders the Login Template to the `/login` url"""
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)