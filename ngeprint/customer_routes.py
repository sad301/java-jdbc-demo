from flask import abort, request, render_template, make_response, redirect, url_for
from ngeprint import app, socket_io, config, job_dao
from ngeprint.utils import new_job
# from ngeprint.job_dao import retrieve
from random import randrange
from werkzeug.utils import secure_filename

# --- routes ---

@app.route("/")
def index():
	return render_template("index.html.j2")

@app.route("/cost")
@app.route("/cost/<id>")
def cost(id=None):
	if not id:
		return redirect(url_for("index"))
	status, jobs, err = job_dao.retrieve(id)
	if not status:
		abort(500)
	if len(jobs) < 1:
		abort(404, "Dokumen yang anda cari tidak ditemukan")
	return render_template("cost.html.j2", job=jobs[0])

@app.route("/confirm")
@app.route("/confirm/<id>")
def confirm(id=None):
	if not id:
		return redirect(url_for("index"))
	status, jobs, err = job_dao.retrieve(id)
	if not status:
		abort(500)
	if len(jobs) < 1:
		abort(404, "Dokumen yang anda cari tidak ditemukan")
	return render_template("confirm.html.j2")

@socket_io.on('client_connect')
def client_connect(job):
	session_id = request.sid
	socket_io.emit("server_confirm", "Job id {} confirmed".format(job["id"]), room=session_id)

@app.errorhandler(404)
def notFound(error):
	return render_template("notFound.html.j2", error=error), 404
