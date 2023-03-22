# object to model an event
class Event:

    def __init__(self, title, start, date, location, end = '', genre = ''):
        self.title = title
        self.start = start
        self.end = end
        self.date = date
        self.location = location
        self.genre = genre

    def event_details(self):
        print(self.title)
        if(self.genre != ''):
            print(self.genre)
        print(self.start)
        print(self.date)
        print(self.location)