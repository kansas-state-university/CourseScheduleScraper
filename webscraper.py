from bs4 import BeautifulSoup
import requests
import regex

import urllib


def __main__():
    year = input("What year would you like to make a schedule for? (All four digits of year entered.)\n")
    semester = raw_input("What semester would you like to make a schedule for? (Spring/Summer/Fall)\n")

    """
        Add if statement for if schedule requested is older than 2016, change web scrape style
    """


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
                if(headerCount >= len(coursesHeader) - 1 and urlCounter >= len(urlList) - 1):
                    modString = (regex.split('(\d+)', cont.get_text()))
                    courseHeadWrite.write("(\"" + modString[0] + "\"" + "," + "\"" + modString[1] + "\"" + "," + "\"" + modString[2].replace("\"", "") + "\")" + "\n")
                elif(headerCount >= len(coursesHeader) - 1 and urlCounter < len(urlList) - 1):
                    modString = (regex.split('(\d+)', cont.get_text()))
                    courseHeadWrite.write("(\"" + modString[0] + "\"" + "," + "\"" + modString[1] + "\"" + "," + "\"" + modString[2].replace("\"", "") + "\")," + "\n")
                else:
                    modString = (regex.split('(\d+)', cont.get_text()))
                    courseHeadWrite.write("(\"" + modString[0] + "\"" + "," + "\"" + modString[1] + "\"" + "," + "\"" + modString[2].replace("\"", "") + "\")," + "\n")
                    headerCount += 1



        coursesContent = urlSoup.find_all('tbody', class_='section')

        contentCount = 0
        for data in coursesContent:
            if(contentCount >= len(coursesContent) - 1 and urlCounter >= len(urlList) - 1):
                for sectionRow in data.find_all('tr', class_='st'):
                    counter = 0
                    courseContentWrite.write("(")
                    for elem in sectionRow.find_all('td'):
                        if(counter != 4 and counter != 8 and counter != 10):
                            if(elem.get_text() == "Appointment"):
                                courseContentWrite.write("\"\", \"\", ")
                                counter += 1
                                counter += 1
                            else:
                                if(counter == 9):
                                    courseContentWrite.write("\"" + elem.get_text().encode("utf-8") + "\"")
                                else:
                                    courseContentWrite.write("\"" + elem.get_text().encode("utf-8") + "\"" + ", ")
                                counter += 1
                        else:
                            counter += 1
                    courseContentWrite.write(")")

            elif(contentCount >= len(coursesContent) - 1 and urlCounter < len(urlList) - 1):
                for sectionRow in data.find_all('tr', class_='st'):
                    counter = 0
                    courseContentWrite.write("(")
                    for elem in sectionRow.find_all('td'):
                        if(counter != 4 and counter != 8 and counter != 10):
                            if(elem.get_text() == "Appointment"):
                                courseContentWrite.write("\"\", \"\", ")
                                counter += 1
                                counter += 1
                            else:
                                if(counter == 9):
                                    courseContentWrite.write("\"" + elem.get_text().encode("utf-8") + "\"")
                                else:
                                    courseContentWrite.write("\"" + elem.get_text().encode("utf-8") + "\"" + ", ")
                                counter += 1
                        else:
                            counter += 1
                    courseContentWrite.write("),\n")

            else:
                for sectionRow in data.find_all('tr', class_='st'):
                    counter = 0
                    courseContentWrite.write("(")
                    for elem in sectionRow.find_all('td'):
                        if(counter != 4 and counter != 8 and counter != 10):
                            if(elem.get_text() == "Appointment"):
                                courseContentWrite.write("\"\", \"\", ")
                                counter += 1
                                counter += 1
                            else:
                                #REMOVE THE ENCODE WHEN YOU FIX THE SANITIZE FUNCTION
                                if(counter == 5):
                                    cleanText = sanitize(elem.get_text(), "day")
                                    courseContentWrite.write("\"" + cleanText.encode("utf-8") + "\"" + ",")

                                elif(counter == 6):
                                    cleanText = sanitize(elem.get_text(), "time")
                                    courseContentWrite.write("\"" + cleanText.encode("utf-8") + "\"" + ",")

                                elif(counter == 7):
                                    cleanText = sanitize(elem.get_text(), "place")
                                    courseContentWrite.write("\"" + cleanText.encode("utf-8") + "\"" + ",")

                                elif(counter == 9):
                                    cleanText = sanitize(elem.get_text(), "instructor")
                                    courseContentWrite.write("\"" + cleanText.encode("utf-8") + "\"")
                                else:
                                    courseContentWrite.write("\"" + elem.get_text().encode("utf-8") + "\"" + ",")

                                counter += 1
                        else:
                            counter += 1
                    courseContentWrite.write(")")
                    courseContentWrite.write(",\n")
            contentCount += 1
        urlCounter += 1

    courseContentWrite.write(";")
    courseHeadWrite.write(";")
    courseHeadWrite.close()
    courseContentWrite.close()


def sanitize(sanText, type):
    if(type == "day"):
        cleanText = []
        for char in sanText:
            if(char == 'M' or char == 'T' or char =='W' or char=='U' or char=='F'):
                cleanText.append(str(char))
        cleanText = ''.join(cleanText)
        return (cleanText)

    elif(type == "time"):
        print
        return sanText

    elif(type == "place"):
        print
        return sanText

    elif(type == "instructor"):
        print
        return sanText
