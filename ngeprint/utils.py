from flask import request
from sqlite3 import connect
from os import urandom, makedirs
from os.path import exists
from datetime import datetime
from werkzeug.utils import secure_filename
from ngeprint import config

def new_job(request):
    f = request.files["dokumen"]
    job = {
        "id": "-".join([urandom(5).hex() for i in range(3)]),
        "kode": "-".join([urandom(2).hex().upper() for i in range(3)]),
        "tanggal": datetime.now(),
        "nama": request.form["nama"],
        "handphone": request.form["handphone"],
        "dokumen": secure_filename(f.filename)
    }
    path = "{}/{}/{}".format(
        config["upload_dir"],
        job["tanggal"].strftime("%Y/%m/%d"),
        job["id"]
    )
    if not exists(path):
        makedirs(path)
    f.save("{}/{}".format(path, job["dokumen"]))
    return job
