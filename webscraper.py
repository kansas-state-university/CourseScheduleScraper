from bs4 import BeautifulSoup
import requests
import regex

import urllib
"""Automating for the sake of debugging, uncomment when production ready
year = input("What year would you like to make a schedule for? (All four digits of year entered.)\n")
semester = raw_input("What semester would you like to make a schedule for? (Spring/Summer/Fall)\n")

schedulePull = semester + str(year) + "/schedule.html"
print (schedulePull)
"""
schedulePull= "spring2017/schedule.html"
data = requests.get("https://courses.ksu.edu/" + schedulePull)


scheduleURLS = data.text

soup = BeautifulSoup(scheduleURLS, "html.parser")

urlList = []
for link in soup.find_all('a'):
    if( len(str(link.get("href"))) < 7 and (str(link.get("href")) != "/" and str(link.get("href")) != "None") ):
        urlList.append(str(link.get("href")))

"""Change this for the full list of URLS once you can do it for one
for url in urlList:
    fullURL = "https://courses.ksu.edu/" + semester + str(year) + "/" + url

    r = urllib.urlopen(fullURL).read()
    urlSoup = BeautifulSoup(r, "html.parser")
    courseHeaders = soup.find_all("tbody", {"class": "course-header"})
    print(urlSoup.getText())
    """


fullURL = "https://courses.ksu.edu/" + "spring" + "2017" + "/AG"
r = urllib.urlopen(fullURL).read()
urlSoup = BeautifulSoup(r, "html.parser")
coursesHeader = urlSoup.find_all('tr', class_='course')
coursesContentOdd = urlSoup.find_all('tbody', class_='section')
coursesContentEven = urlSoup.find_all('tbody', class_='section even')

courseHeadWrite = open('courseNum.txt', 'w')

for c in coursesHeader:
    for cont in c.contents:
        modString = (regex.split('(\d+)', cont.get_text()))
        courseHeadWrite.write(modString[0] + "," + modString[1] + "," + modString[2] + "\n")
courseHeadWrite.close()

for d in coursesContentOdd:
    for cont in d.contents[0]:
        print(cont.get_text())
    print

"""
for d in coursesContentEven:
    for cont in d.contents:
        print(cont.get_text())
    print("\n")
"""