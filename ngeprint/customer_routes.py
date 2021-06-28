from flask import render_template
from ngeprint import app

@app.route("/")
def index():
	return render_template("index.html.j2")
