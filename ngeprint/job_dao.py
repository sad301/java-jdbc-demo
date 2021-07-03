from ngeprint.dao import execute_query, execute_update

def create(job):
    sql = """
    insert into jobs (id, kode, tanggal, nama, handphone, client_file, server_file)
    values (?, ?, ?, ?, ?, ?, ?)
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
    update jobs set kode=?, tanggal=?, nama=?, handphone=?, client_file=?, server_file=?, page_grayscale=?, page_color=?, page_blank=?, page_total=?, price_grayscale=?, price_color=?, price_blank=?, price_total=?, status=? where id=?
    """
    values = tuple(job.values())
    return execute_update(sql, values)

def delete(job):
    sql = "delete from jobs where id=?"
    values = tuple(job.values())
    return execute_update(sql, values)
