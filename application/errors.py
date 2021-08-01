from flask import render_template
from application import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500) # handle any server errors
def internal_error(error):
    db.session.rollback()  # make sure we don't accidentally commit anything from this broken session
    return render_template('500.html'), 500