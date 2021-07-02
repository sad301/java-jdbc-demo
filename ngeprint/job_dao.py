from ngeprint.dao import execute_update

def create(job):
    sql = "insert into jobs (id, kode, tanggal, nama, handphone, client_file, server_file) values (?, ?, ?, ?, ?, ?, ?)"
    values = tuple(job.values())
    return execute_update(sql, values)
