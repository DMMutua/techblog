import os

class Config:
    """Hosts all the Configuration Settings for the TechBlog App
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_pretty_strong_password'