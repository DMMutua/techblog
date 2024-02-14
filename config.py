import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Hosts all the Configuration Settings for the TechBlog App
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_pretty_strong_password'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['some-email@example.com']