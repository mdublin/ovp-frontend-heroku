from flask import render_template
from . import main

@app.errorhandler(404)
def page_not_found(e):
    print("THIS IS BEING CALLED!!!")
    return render_template('404.html'), 404

