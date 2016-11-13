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
fixedTable2 = "INSERT INTO courseContent VALUES "

quoteCount = 0
for line in table2.splitlines():
    quoteCount = line.count('\"')
    if(quoteCount >= 16):
        fixedTable2 += line + " "


print(fixedTable2)


cursor.execute(table1)
cursor.execute(fixedTable2)
cnx.commit()
cnx.close()