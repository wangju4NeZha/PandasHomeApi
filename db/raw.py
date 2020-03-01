from . import db_conn

def query(sql, *args, **kwargs):
    with db_conn as cursor:
        cursor.execute(sql, args=(args if args else kwargs))
        if cursor.rowcount > 0:
            return cursor.fetchall()

if __name__ == '__main__':
    pass
