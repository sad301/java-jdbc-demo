from flask import jsonify, request
from ngeprint import config, app, job_dao
from ngeprint.utils import new_job
from os import remove
from shutil import rmtree

@app.route("/api")
def api_index():
    return {"message": "/api index"}

@app.route("/api/jobs", methods=["GET", "POST"])
def api_jobs():
	# post method
	if request.method == "POST":
		if not request.form or not request.files:
			return {"message": "invalid request"}, 400
		if not all(key in request.form.keys() for key in ["nama", "handphone"]):
			return {"message": "invalid request"}, 400
		if not "dokumen" in request.files:
			return {"message": "invalid request"}, 400
		job, success, affected_row, error = new_job(request)
		if not success:
			return {"message": str(error)}, 500
		return {"message": "success!", "id": job["id"]}
	# get method
	status, data, error = job_dao.retrieve()
	if not status:
		return {"message": str(error)}, 500
	return jsonify(data)

@app.route("/api/jobs/<id>", methods=["GET", "DELETE", "PUT"])
def api_jobs_job(id):
	if request.method == "PUT":
		return {"message": "put method"}
	# --- delete method ---
	if request.method == "DELETE":
		success, jobs, error = job_dao.retrieve(id)
		if not success:
			return {"message", str(error)}, 500
		if len(jobs) < 1:
			return {"message": "not found"}, 404
		remove(jobs[0]["server_file"])
		rmtree("{}/{}".format( config["temp_dir"], jobs[0]["id"] ))
		success, affected_row, error = job_dao.delete(id)
		if not success:
			return {"message": str(error)}, 500
		return {"message": "done!"}
	# --- get method ---
	status, data, error = job_dao.retrieve(id)
	if not status:
		return {"message": str(error)}, 500
	if len(data) < 1:
		return {"message": "not found"}, 404
	return jsonify(data[0])

@app.route("/api/jobs/<id>/confirm", methods=["POST"])
def api_jobs_job_confirm(id):
    return {"message": "job {} confirmed".format(id)}
