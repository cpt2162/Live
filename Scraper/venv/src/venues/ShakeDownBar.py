import sys
sys.path.append(r"C:\Users\Cameron\Live\Scraper\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Cameron\Live\Scraper\venv\src")
import requests
import Event
from Event import Event
from bs4 import BeautifulSoup

URL = "https://shakedownbarvail.com/events/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

def createEvent(sets, location, date):
    events=[]
    for set in sets:
        times = []
        times.append(set.find_all("time"))
        start = times[0][0].text.strip()
        end = times[0][1].text.strip()
        links = set.find_all("a")
        title = links[1].text.strip()
        evnt = Event(title, start, end, date, location)
        events.append(evnt)

    return events


def readCalendar(venue):
    events = []
    weeks = soup.find_all("div", class_="tribe-events-calendar-month__week")
    for week in weeks:
        days = week.find_all("div", class_="tribe-events-calendar-month__day")
        for day in days:
            event = day.find_all("article")
            info = day.find_all("div")
            clas = info[0]['id']
            date = slice(len(clas)-10, len(clas))
            sets = createEvent(event, venue, clas[date])
            for set in sets:
                events.append(set)
    for event in events:
        print("#####")
        print(event.title)
        print(event.start)
        print(event.end)
        print(event.date)
        print(event.location)


def main():
    readCalendar("Shakedown Bar")


if __name__=="__main__":
    main()