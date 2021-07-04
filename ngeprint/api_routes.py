from flask import jsonify, request
from ngeprint import app, job_dao
from ngeprint.utils import new_job

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
        job, res, err = new_job(request)
        if not res:
            return {"message": str(err)}, 500
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
    # delete method
    if request.method == "DELETE":
        return {"message": "delete method"}
    # get method
    status, data, error = job_dao.retrieve(id)
    if not status:
        return {"message": str(error)}, 500
    if len(data) < 1:
        return {"message": "not found"}, 404
    return jsonify(data[0])
