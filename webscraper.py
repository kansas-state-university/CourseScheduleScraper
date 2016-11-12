from bs4 import BeautifulSoup
import requests

import urllib

year = input("What year would you like to make a schedule for? (All four digits of year entered.)\n")
semester = raw_input("What semester would you like to make a schedule for? (Spring/Summer/Fall)\n")

fullURL = semester + str(year) + "/schedule.html"
print (fullURL)

data = requests.get("https://courses.ksu.edu/" + fullURL)


scheduleURLS = data.text

soup = BeautifulSoup(scheduleURLS, "html.parser")

urlList = []
for link in soup.find_all('a'):
    if (len(str(link.get("href"))) < 7 and (str(link.get("href"))) != "/" and (str(link.get("href"))) != "None"):
        urlList.append(link.get("href"))

for url in urlList:
    print(str(url))

r = urllib.urlopen('https://courses.k-state.edu/spring2017/EN/').read()

soup = BeautifulSoup(r, "html.parser")


courseHeaders = soup.find_all("tbody", {"class": "course-header"})


print ()