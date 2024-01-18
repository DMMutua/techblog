from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
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