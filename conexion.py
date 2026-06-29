from mysql.connector import connect
con = connect(host="localhost", user="root", password="", database="videoclub", autocommit=False)
cur = con.cursor()
