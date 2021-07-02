from flask import request, render_template, make_response
from ngeprint import app, config
from ngeprint.utils import new_job
from random import randrange
from werkzeug.utils import secure_filename

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
	# nama = request.form["nama"]
	# handphone = request.form["handphone"]
	# dokumen = request.files["dokumen"]
	job = new_job(request)
	# res = make_response(job)
	# res.headers["Content-Type"] = "application/json"
	return render_template("upload.html.j2")
