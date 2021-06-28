from flask import request, render_template
from ngeprint import app

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		return "this is post method"
	return render_template("index.html.j2")
