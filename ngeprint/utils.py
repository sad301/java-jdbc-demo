from flask import request
from sqlite3 import connect
from os import urandom, makedirs
from os.path import exists, splitext
from datetime import datetime
from werkzeug.utils import secure_filename
from ngeprint import config, job_dao

def new_job(request):
    f = request.files["dokumen"]
    job = {
        "id": "-".join([urandom(5).hex() for i in range(3)]),
        "kode": "-".join([urandom(2).hex().upper() for i in range(3)]),
        "tanggal": datetime.now(),
        "nama": request.form["nama"],
        "handphone": request.form["handphone"]
    }
    path = "{}/{}".format(config["upload_dir"], job["tanggal"].strftime("%Y/%m/%d"))
    if not exists(path):
        makedirs(path)
    _, ext = splitext(secure_filename(f.filename))
    job["dokumen"] = "{}/{}{}".format(path, job["id"], ext)
    f.save(job["dokumen"])
    stat, msg = job_dao.create(job)
    if not stat:
        print(msg)
    return job
