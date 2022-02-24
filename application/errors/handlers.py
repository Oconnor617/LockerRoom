from flask import render_template
from application import db #app removed
from application.errors import bp # The bp named "errors" in this case

@bp.app_errorhandler(404)
#@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
#@app.errorhandler(500) # handle any server errors
def internal_error(error):
    db.session.rollback()  # make sure we don't accidentally commit anything from this broken session
    return render_template('errors/500.html'), 500