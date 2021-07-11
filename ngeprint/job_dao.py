from ngeprint.dao import execute_query, execute_update
import json

def create(job):
	sql = """
	insert into jobs (id, kode, tanggal, nama, handphone, client_file, server_file)
	values (?, ?, ?, ?, ?, ?, ?)
	"""
	values = (job["id"], job["kode"], job["tanggal"], job["nama"], job["handphone"], job["client_file"], job["server_file"])
	return execute_update(sql, values)

def retrieve(id=None):
	sql = "select * from jobs"
	if id:
		sql += " where id=?"
	sql += " order by tanggal desc"
	return execute_query(sql, (id,) if id else None)

def update(job):
	sql = """
	update jobs set kode=?, tanggal=?, nama=?, handphone=?, client_file=?, server_file=?, page_grayscale=?, page_color=?, page_blank=?, page_total=?, price_grayscale=?, price_color=?, price_blank=?, price_total=?, status=?, processed=? where id=?
	"""
	values = (job["kode"], job["tanggal"], job["nama"], job["handphone"], job["client_file"], job["server_file"], job["page_grayscale"], job["page_color"], job["page_blank"], job["page_total"], job["price_grayscale"], job["price_color"], job["price_blank"], job["price_total"], job["status"], job["processed"], job["id"])
	return execute_update(sql, values)

def delete(id):
	return execute_update("delete from jobs where id=?", (id,))
