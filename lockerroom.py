"""
Start Here, run app from browser at 127.0.0.1:5000
Created on July 15, 2021
@author: oconn
"""
from application import app, db
from application.models import User


@app.shell_context_processor  # This make it easier to run tests in teh python shell
def make_shell_context():
    return {'db': db, 'User': User}  # this will auto import these into the shell so they can be user directly
# typing 'flask shell' to the terminal will start the Python interpreter IN the context of the app

if __name__ == '__main__':  # Script executed directly?
    app.run(debug=True)  # Launch built-in web server and run this Flask webapp