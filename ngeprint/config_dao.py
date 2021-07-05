from ngeprint.dao import execute_query, execute_update

def retrieve():
	sql = "select * from config"
	return execute_query(sql)
