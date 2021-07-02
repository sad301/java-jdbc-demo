from flask import render_template
from ngeprint import app

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
