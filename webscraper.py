from bs4 import BeautifulSoup
import requests
import regex

import urllib


def __main__():
    year = 2017 #input("What year would you like to make a schedule for? (All four digits of year entered.)\n")
    semester = "spring" #raw_input("What semester would you like to make a schedule for? (Spring/Summer/Fall)\n")



    schedulePull = semester + str(year) + "/schedule.html"
    print (schedulePull)

    data = requests.get("https://courses.ksu.edu/" + schedulePull)

    scheduleURLS = data.text

    soup = BeautifulSoup(scheduleURLS, "html.parser")

    urlList = []
    for link in soup.find_all('a'):
        if( len(str(link.get("href"))) < 7 and (str(link.get("href")) != "/" and str(link.get("href")) != "None") ):
            urlList.append(str(link.get("href")))

    courseHeadWrite = open('courseNum.txt', 'w')
    courseHeadWrite.write("INSERT INTO contentHeader\n")
    courseHeadWrite.write("VALUES \n")

    courseContentWrite = open('courseCont.txt', 'w')
    courseContentWrite.write("INSERT INTO courseContent\n")
    courseContentWrite.write("VALUES \n")

    urlCounter = 0
    for url in urlList:
        fullURL = "https://courses.ksu.edu/" + semester + str(year) + "/" + url

        r = urllib.urlopen(fullURL).read()
        urlSoup = BeautifulSoup(r, "html.parser")
        coursesHeader = urlSoup.find_all('tr', class_='course')

        headerCount = 0
        for c in coursesHeader:
            for cont in c.contents:
                if (headerCount >= len(coursesHeader) - 1 and urlCounter >= len(urlList) - 1):
                    modString = (regex.split('(\d+)', cont.get_text()))
                    courseHeadWrite.write(
                        "(\"" + modString[0] + "\"" + "," + "\"" + modString[1] + "\"" + "," + "\"" + modString[
                            2].replace("\"", "") + "\");" + "\n")
                elif (headerCount >= len(coursesHeader) - 1 and urlCounter < len(urlList) - 1):
                    modString = (regex.split('(\d+)', cont.get_text()))
                    courseHeadWrite.write(
                        "(\"" + modString[0] + "\"" + "," + "\"" + modString[1] + "\"" + "," + "\"" + modString[
                            2].replace("\"", "") + "\")," + "\n")
                else:
                    modString = (regex.split('(\d+)', cont.get_text()))
                    courseHeadWrite.write(
                        "(\"" + modString[0] + "\"" + "," + "\"" + modString[1] + "\"" + "," + "\"" + modString[
                            2].replace("\"", "") + "\")," + "\n")
                headerCount += 1


        coursesContent = urlSoup.find_all('tbody', class_='section')

        lineCounter = 0
        for data in coursesContent:
            for sectionRow in data.find_all('tr', class_='st'):
                counter = 0
                courseContentWrite.write("(")
                for rowData in sectionRow.find_all('td', {'class': lambda x : x != "session-label"}):
                    if (counter != 4 and counter != 8 and counter != 10):
                        if (rowData.get_text() == "Appointment"):
                            courseContentWrite.write("\"\", \"\", ")
                            counter += 1
                            counter += 1
                        else:
                            if (counter == 5):
                                cleanText = sanitize(rowData.get_text(), "day")
                                courseContentWrite.write("\"" + cleanText.encode("utf-8") + "\"" + ",")

                            elif (counter == 6):
                                cleanText = sanitize(rowData.get_text(), "time")
                                courseContentWrite.write("\"" + cleanText.encode("utf-8") + "\"" + ",")

                            elif (counter == 7):
                                cleanText = sanitize(rowData.get_text(), "place")
                                courseContentWrite.write("\"" + cleanText.encode("utf-8") + "\"" + ",")

                            elif (counter == 9):
                                cleanText = sanitize(rowData.get_text(), "instructor")
                                courseContentWrite.write("\"" + cleanText.encode("utf-8") + "\"")
                            else:
                                courseContentWrite.write("\"" + rowData.get_text().encode("utf-8") + "\"" + ",")

                            counter += 1
                    else:
                        counter += 1
                if(lineCounter >= len(coursesContent) - 1 and urlCounter >= len(urlList) - 1):
                    courseContentWrite.write(");")
                else:
                    courseContentWrite.write("),\n")
            lineCounter += 1
        urlCounter+=1


def sanitize(sanText, type):
    if(type == "day"):
        cleanText = []
        for char in sanText:
            if(char == 'M' or char == 'T' or char =='W' or char=='U' or char=='F'):
                cleanText.append(str(char))
        cleanText = ''.join(cleanText)
        return (cleanText)

    elif(type == "time"):
        return sanText

    elif(type == "place"):
        return sanText

    elif(type == "instructor"):
        return sanText
