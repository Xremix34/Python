import mysql.connector

#Conecta à base de dados do MySQL
conectar = mysql.connector.connect(
  host='localhost',
  user='root',
  password="CQghi816",
  port = 3306, #for Mamp users
  database='stock',
  auth_plugin = 'mysql_native_password',
)

#print(conectar)