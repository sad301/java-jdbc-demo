import sqlite3

def __dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def execute_query(sql, data=None):
    temp = []
    try:
        conn = sqlite3.connect("ngeprint.db")
        conn.row_factory = __dict_factory
        curr = conn.cursor()
        if data:
            curr.execute(sql, data)
        else:
            curr.execute(sql)
        for row in curr.fetchall():
            temp.append(row)
        curr.close()
        conn.close()
    except sqlite3.Error as err:
        return False, err
    return True, temp

def execute_update(sql, data):
    try:
        conn = sqlite3.connect("ngeprint.db")
        conn.row_factory = __dict_factory
        curr = conn.cursor()
        curr.execute(sql, data)
        conn.commit()
        curr.close()
        conn.close()
    except sqlite3.Error as err:
        return False, err
    return True, "done!"
