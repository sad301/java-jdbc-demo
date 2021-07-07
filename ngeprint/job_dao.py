from ngeprint.dao import execute_query, execute_update

def create(job):
	sql = """
	insert into jobs (id, kode, tanggal, nama, handphone, client_file, server_file, max_page)
	values (?, ?, ?, ?, ?, ?, ?, ?)
	"""
	values = tuple(job.values())
	return execute_update(sql, values)

def retrieve(id=None):
	sql = "select * from jobs"
	if id:
		sql += " where id=?"
	return execute_query(sql, (id,) if id else None)

def update(job):
	sql = """
	update	jobs
	set		kode=?, tanggal=?, nama=?, handphone=?, client_file=?, server_file=?, max_page=?, page_grayscale=?, page_color=?, page_blank=?, page_total=?, price_grayscale=?, price_color=?, price_blank=?, price_total=?, status=?, processed=?
	where	id=?
	"""
	# values = tuple(job.values())
	values_list = list(tuple(job.values()))
	id = values_list.pop(0)
	values_list.append(id)
	# values = tuple(values_list)
	return execute_update(sql, tuple(values_list))

def delete(id):
	return execute_update("delete from jobs where id=?", (id,))
