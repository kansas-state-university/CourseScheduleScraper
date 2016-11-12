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

    courseHeadWrite = open('courseNum.sql', 'w')
    courseHeadWrite.write("INSERT INTO courseHeader\n")
    courseHeadWrite.write("VALUES \n")

    courseContentWrite = open('courseCont.sql', 'w')
    courseContentWrite.write("INSERT INTO courseContent\n")
    courseContentWrite.write("VALUES \n")


    for url in urlList:
        fullURL = "https://courses.ksu.edu/" + semester + str(year) + "/" + url

        r = urllib.urlopen(fullURL).read()
        urlSoup = BeautifulSoup(r, "html.parser")
        coursesHeader = urlSoup.find_all('tr', class_='course')


        headerCount = 0
        for c in coursesHeader:
            for cont in c.contents:
                if(headerCount >= len(coursesHeader) - 1):
                    modString = (regex.split('(\d+)', cont.get_text()))
                    courseHeadWrite.write("(\"" + modString[0] + "\"" + "," + "\"" + modString[1] + "\"" + "," + "\"" + modString[2] + "\")" + "\n")
                else:
                    modString = (regex.split('(\d+)', cont.get_text()))
                    courseHeadWrite.write("(\"" + modString[0] + "\"" + "," + "\"" + modString[1] + "\"" + "," + "\"" + modString[2] + "\")," + "\n")
                    headerCount += 1



        coursesContent = urlSoup.find_all('tbody', class_='section')

        contentCount = 0
        for data in coursesContent:
            if(contentCount >= len(coursesContent) - 1):
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
                                if(counter == 9):
                                    courseContentWrite.write("\"" + elem.get_text().encode("utf-8") + "\"")
                                else:
                                    courseContentWrite.write("\"" + elem.get_text().encode("utf-8") + "\"" + ", ")
                                counter += 1
                        else:
                            counter += 1
                    courseContentWrite.write(")")
                    courseContentWrite.write(",\n")
            contentCount += 1

    courseContentWrite.write(";")
    courseHeadWrite.write(";")
    courseHeadWrite.close()
    courseContentWrite.close()
