from flask import request, render_template
from ngeprint import app
from random import randrange
from werkzeug.utils import secure_filename

import sqlite3

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		id = "-".join(["{:02d}".format( randrange(0, 99) ) for i in range(0, 4)])
		nama = request.form["nama"]
		handphone = request.form["handphone"]
		file = request.files["dokumen"]
		dokumen = secure_filename(file.filename)
		file.save(dokumen)
		job = (id, nama, handphone, dokumen)
		sql = "insert into jobs (id, nama, handphone, dokumen) values (?, ?, ?, ?)"
		with sqlite3.connect("ngeprint.db") as conn:
			cur = conn.cursor()
			cur.execute(sql, job)
			conn.commit();
		conn.close()
		return render_template("index.post.html.j2", id=id, nama=nama, handphone=handphone, dokumen=dokumen)
	return render_template("index.html.j2")
