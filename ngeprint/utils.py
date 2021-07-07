# from flask import request
# from sqlite3 import connect
from os import urandom, makedirs
from os.path import exists, splitext
from datetime import datetime
from json import dumps
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
from ngeprint import config, dao, job_dao, config_dao, socket_io
# from time import sleep

# jumlah maximal halaman yang bisa diprint
def max_page(handphone):
	paid_jobs = 0;
	res = dao.execute_query("select paid_jobs from count_jobs where handphone=?", (handphone,))
	if len(res[1]) == 1:
		paid_jobs = res[1][0]["paid_jobs"]
	return (paid_jobs + 1) * 5

def new_job(request):
	f = request.files["dokumen"]
	handphone = request.form["handphone"]
	# paid_jobs = 0
	# success, data, error = dao.execute_query("select paid_jobs from count_jobs where handphone=?", (handphone,))
	# if not success:
	# 	return None, success, -1, error
	# if len(data) == 1:
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
	job["max_page"] = max_page(job["handphone"])
	f.save(job["server_file"])
	success, affected_row, error = job_dao.create(job)
	return job, success, affected_row, error

def __analyze_image(image):
	pixel_total = image.width * image.height
	pixel_white = 0
	pixel_grayscale = 0
	pixel_color = 0
	for x in range(image.width):
		for y in range(image.height):
			pixel = image.getpixel((x, y))
			if pixel[0] == pixel[1] == pixel[2]:
				if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
					pixel_white += 1
				else:
					pixel_grayscale += 1
			else:
				c = [pixel[0], pixel[1], pixel[2]]
				c.sort()
				div = 0
				try:
					div = (c[2] - c[0]) / c[1]
				except ZeroDivisionError as error:
					pass
				finally:
					if div >= 0.25:
						pixel_color += 1
					else:
						pixel_grayscale += 1
	return pixel_total, pixel_white, pixel_grayscale, pixel_color

def process_job(job, session_id):
	print("processing ... ")
	temp = "{}/{}".format("temp", job["id"])
	if not exists(temp):
		makedirs(temp)
	images = convert_from_path(job["server_file"], size=(200, None), output_folder=temp, output_file="img", fmt="png")
	job["page_total"] = len(images)
	for idx, image in enumerate(images):
		pixel_total, pixel_white, pixel_grayscale, pixel_color = __analyze_image(image)
		color_percentage = 0
		if pixel_color > 0:
			color_percentage = ((pixel_color / pixel_total) * 100)
			if color_percentage > 0.1:
				job["page_color"] += 1
		if pixel_white > 0:
			if ((pixel_white / pixel_total) * 100) >= 100.0:
				job["page_blank"] += 1
	job["page_grayscale"] = job["page_total"] - (job["page_color"] + job["page_blank"])
	success, rows, error = config_dao.retrieve()
	if not success:
		print(str(error))
		socket_io.emit("process_failed", str(error), room=session_id)
	else:
		config = {row["_key"]: row["_value"] for row in rows}
		job["price_grayscale"] = int(job["page_grayscale"]) * int(config["price.grayscale"])
		job["price_color"] = int(job["page_color"]) * int(config["price.color"])
		job["price_blank"] = int(job["page_blank"]) * int(config["price.blank"])
		job["price_total"] = job["price_grayscale"] + job["price_color"] + job["price_blank"]
		job["processed"] = 1
		success, row_num, error = job_dao.update(job)
		if not success:
			print(str(error))
			socket_io.emit("process_failed", str(error), room=session_id)
		else:
			job.pop("kode", None)
			socket_io.emit("process_done", job, room=session_id)
			print("done!")
