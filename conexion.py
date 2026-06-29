# CONEXION A LA BASE DE DATOS
# Este archivo crea la conexion con MySQL.
# Todos los modulos importan con y cur desde aca para ejecutar consultas.
# autocommit=False permite usar commit() y rollback() manualmente.

from mysql.connector import connect

# Se conecta a MySQL (base "videoclub" en localhost, usuario root sin contraseña)
con = connect(host="localhost", user="root", password="", database="videoclub", autocommit=False)

# Crea un cursor para ejecutar consultas SQL
cur = con.cursor()
