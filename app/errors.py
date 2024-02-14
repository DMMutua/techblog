from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    """Handles Errors for 404 Not Found Error"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handles Errors for 500 Internal Server Error"""
    db.session.rollback()
    return render_template('500.html'), 500