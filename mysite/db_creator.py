from mysql import connector as con

dbase = con.connect(
#    database = 'MySQLnow',
    host = 'localhost',
    user = 'root',
    password = '(Puxy1989)',
    )

my_cursor = dbase.cursor()

my_cursor.execute("CREATE DATABASE MySQLdb CHARACTER SET utf8;")
