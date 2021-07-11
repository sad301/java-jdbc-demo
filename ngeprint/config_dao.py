from ngeprint.dao import execute_query, execute_update

def create(config):
	sql = "insert into config values (?, ?)"
	return execute_update(sql, tuple(config.values()))

def retrieve():
	sql = "select * from config"
	return execute_query(sql)

# return: success, config, error
def retrieve_as_dict():
	success, rows, error = retrieve()
	if not success:
		return False, None, error
	return True, { row["_key"]: row["_value"] for row in rows }, None
