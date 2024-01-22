import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Hosts all the Configuration Settings for the TechBlog App
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_pretty_strong_password'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')