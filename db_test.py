import pandas as pd
import mysql.connector as ms
import psycopg2

x = pd.read_csv('test.csv', header=None)
x.to_excel('test.xlsx', index=None, header=None)
cnx = psycopg2.connect(user='postgres', password='123', host='localhost', database='dbname', port=5432)
# cnx = ms.connect(user='postgres', password='postgres', host='172.168.2.164', database='postgres', port=5432)
cursor = cnx.cursor()
cursor.execute("SELECT * FROM bike LIMIT 100")
result = cursor.fetchall()
print(result)
