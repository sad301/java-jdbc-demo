from flask import render_template, make_response
from ngeprint import app, job_dao

# --- admin routes ---

@app.route("/admin")
def admin():
    return render_template("admin/index.html.j2")

@app.route("/admin/home")
def admin_home():
    return render_template("admin/home.html.j2")

@app.route("/admin/jobs")
def admin_jobs():
    return render_template("admin/jobs.html.j2")

@app.route("/admin/jobs/<id>")
def admin_jobs_job(id):
    success, jobs, error = job_dao.retrieve(id)
    if not success:
        return {"message": str(error)}, 500
    if len(jobs) < 1:
        return {"message": "not found"}, 404
    return render_template("admin/job.html.j2", id=id)
