from flask import abort, request, render_template, make_response, redirect, url_for
from ngeprint import app, socket_io, config, job_dao, dao
from ngeprint.utils import new_job, process_job
# from ngeprint.job_dao import retrieve
from random import randrange
from werkzeug.utils import secure_filename
# from pdf2image import convert_from_path
from threading import Thread
from json import dumps

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
	if not status or len(jobs) < 1:
		return redirect(url_for("index"))
	return render_template("cost.html.j2", id=id)

@app.route("/confirm")
@app.route("/confirm/<id>")
def confirm(id=None):
	if not id:
		return redirect(url_for("index"))
	result = job_dao.retrieve(id)
	if not result[0] or len(result[1]) < 1:
		return redirect(url_for("index"))
	return render_template("confirm.html.j2", job=result[1][0])

@app.route("/done")
@app.route("/done/<id>")
def done(id=None):
	if not id:
		return redirect(url_for("index"))
	result = job_dao.retrieve(id)
	if not result[0] or len(result[1]) < 1:
		return redirect(url_for("index"))
	if result[1][0]["status"] != "CONFIRMED":
		return redirect(url_for("index"))
	return render_template("done.html.j2")

@socket_io.on('client_connect')
def client_connect(id):
	session_id = request.sid
	socket_io.emit("server_confirm", id, room=session_id)
	success, jobs, error = job_dao.retrieve(id)
	if not success:
		socket_io.emit("process_failed", str(error), room=session_id)
	else:
		if len(jobs) < 1:
			socket_io.emit("process_failed", {"message": "job not found"}, room=session_id)
		else:
			if jobs[0]["processed"] == 0:
				socket_io.start_background_task(target=process_job, job=jobs[0], session_id=session_id)
			else:
				jobs[0].pop("kode", None)
				socket_io.emit("process_done", jobs[0], room=session_id)

@app.errorhandler(404)
def notFound(error):
	return render_template("notFound.html.j2", error=error), 404
