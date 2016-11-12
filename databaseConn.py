import webscraper
import mysql.connector

webscraper.__main__()


cnx = mysql.connector.connect(user='root', password='hackpass', host='127.0.0.1', database='Hackathon')
cursor = cnx.cursor()
cursor.execute("DELETE FROM contentHeader")
cursor.execute("DELETE FROM courseContent")


file1 = open('courseNum.txt', 'r')
file2 = open('courseCont.txt', 'r')

table1 = file1.read()
table2 = file2.read()

cursor.execute(table1)
cursor.execute(table2)
cnx.commit()
cnx.close()