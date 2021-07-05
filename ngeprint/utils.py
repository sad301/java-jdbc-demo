from flask import request
from sqlite3 import connect
from os import urandom, makedirs
from os.path import exists, splitext
from datetime import datetime
from werkzeug.utils import secure_filename
from ngeprint import config, job_dao, socket_io
from time import sleep

def new_job(request):
	f = request.files["dokumen"]
	job = {
		"id": "-".join([urandom(5).hex() for i in range(3)]),
		"kode": "-".join([urandom(2).hex().upper() for i in range(3)]),
		"tanggal": datetime.now(),
		"nama": request.form["nama"],
		"handphone": request.form["handphone"],
		"client_file": secure_filename(f.filename)
	}
	path = "{}/{}".format(config["upload_dir"], job["tanggal"].strftime("%Y/%m/%d"))
	if not exists(path):
		makedirs(path)
	_, ext = splitext(job["client_file"])
	job["server_file"] = "{}/{}{}".format(path, job["id"], ext)
	f.save(job["server_file"])
	success, affected_row, error = job_dao.create(job)
	return job, success, affected_row, error

def process_job(job, session_id):
	for i in range(0, 10):
		socket_io.sleep(0.5)
	socket_io.emit("process_done", "job id {} done!".format(job["id"]), room=session_id)
