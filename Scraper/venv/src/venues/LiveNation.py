import sys
sys.path.append(r"C:\Users\Cameron\Live\Scraper\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Cameron\Live\Scraper\venv\src")
import requests
import Event
from bs4 import BeautifulSoup
from Event import Event
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

SearchUrlBase = "https://livenation.com"

# soup = BeautifulSoup(page.content, "html.parser")

###
# Extracts events from the event list and creates an event onject for each one
###
def extractEvents(events, driver, venue):
    import time
    concerts = []
    eventLinks = driver.find_elements(By.CLASS_NAME, 'css-qvkmuq')
    index = -1
    if(len(events) > len(eventLinks)):
        max = len(eventLinks)
    else: 
        max = len(events)
    for i in range(max):
        time.sleep(1)
        eventLinks = driver.find_elements(By.CLASS_NAME, 'css-qvkmuq')
        eventCovers = driver.find_elements(By.CLASS_NAME, 'css-1lxwves')
        index += 1
        details = eventCovers[i].text.split("\n")
        name = details[1]
        genre = details[2]
        date = details[0]
        clicked = False
        while not clicked:
            try:
                eventLinks[index].click()
                time.sleep(1)
                clicked = True
            except:
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, 1080)") 
        start = extractTime(driver, venue)
        event = Event(name, start, date, venue)
        concerts.append(event)
        driver.back()
    return concerts


####
# Extract date spans. Custom for each venue.. for now
###
def extractTime(driver, venue):
    if(venue == "Red Rocks Amphitheatre"):
        times = driver.find_elements(By.CLASS_NAME, 'date-wrapper')
        start = times[1].text[19:len(times[1].text)]
        return start
    elif(venue == "Dillon Amphitheater"):
        times = driver.find_elements(By.CLASS_NAME, 'date')
        start = times[0].text.split(' ')
        print(start[3])


###
# prints events legibly
###
def prettyPrint(events, venue):
    print(f'{venue} Events')
    for event in events:
        print("##########")
        event.event_details()

###
# retrieve event list from venue site, extracts and creates events with the extractEvents function, prints the events
###
def findVenueEvents(venue, driver):
    import time
    driver.get(f'{SearchUrlBase}')
    time.sleep(2)
    searchBar = driver.find_element(By.CLASS_NAME,'react-autosuggest__input')
    searchBar.send_keys(venue)
    searchBar.send_keys(Keys.RETURN)
    driver.implicitly_wait(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all('a', class_='chakra-linkbox__overlay css-10rafrq')
    results = soup.find_all('div', class_= 'css-1lxwves')
    index = 0
    for result in results:
        if(result.header.h3.text == venue):
            query = links[index].attrs['href']
            driver.get((f"{SearchUrlBase}{query}"))
        else:
            index += 1
    events = driver.find_elements(By.CLASS_NAME, 'css-1lxwves')
    prettyPrint(extractEvents(events, driver, venue), venue)


def main(venue):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(service=ChromService(ChromeDriverManager().install()), chrome_options=options)
    findVenueEvents(venue, driver)

 
if __name__=="__main__":
    main(sys.argv[1])