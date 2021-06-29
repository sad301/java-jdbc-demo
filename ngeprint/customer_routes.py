from flask import request, render_template
from ngeprint import app
from random import randrange
from werkzeug.utils import secure_filename
import sqlite3

# --- routes ---

@app.route("/")
def index():
	return render_template("index.html.j2")

@app.route("/upload", methods=["POST"])
def upload():
	if not request.form or not request.files:
		return {"message": "invalid request"}, 400
	if not all(key in request.form.keys() for key in ["nama", "handphone"]):
		return {"message": "invalid request"}, 400
	if not "dokumen" in request.files:
		return {"message": "invalid request"}, 400
