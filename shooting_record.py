from inspect import getargs
import re
from turtle import update

def sanitize_html_text(input):
    return re.sub(f'\[.*?\]', '', input.replace(u'\xa0', ' ')).strip()

class ShootingRecord:

    attributes = ['date', 'city', 'occurrence', 'state', 'dead', 'injured', 'description', 'tweet_id']

    def __init__(self, date, city, occurrence, state, dead, injured, description, tweet_id = None):
        self.date = date
        self.city = city
        self.occurrence = int(occurrence)
        self.state = state
        self.dead = int(dead)
        self.injured = int(injured)
        self.description = description
        self.tweet_id = tweet_id

    @staticmethod
    def from_html_table_row(html):
        arguments = []
        arguments.append(sanitize_html_text((html.select('td:nth-child(1)')[0].get_text())))
        [city_name, occurrence] = ShootingRecord.extract_data_from_city_entry(html.select('td:nth-child(2)')[0].get_text().replace(u'\xa0', ' ').strip())
        arguments.append(city_name)
        arguments.append(occurrence)
        arguments.append(sanitize_html_text(html.select('td:nth-child(3)')[0].get_text()))
        arguments.append(sanitize_html_text(html.select('td:nth-child(4)')[0].get_text()))
        arguments.append(sanitize_html_text(html.select('td:nth-child(5)')[0].get_text()))
        arguments.append(sanitize_html_text(html.select('td:nth-child(7)')[0].get_text()))
        
        return ShootingRecord(*arguments)

    @staticmethod
    def extract_data_from_city_entry(entry):
        regex = r'(?P<cityName>[a-zA-Z \-_\.]*)(?:\((?P<occurrence>\d+)\))?'
        match = re.search(regex, entry)
        city_name = match.group('cityName').strip()

        occurrence = match.group('occurrence')

        return [city_name, occurrence if occurrence != None else 1]

    def same_shooting(self, other):
        if not isinstance(other, ShootingRecord):
            return False

        return self.occurrence==other.occurrence and self.city==other.city and self.state==other.state

    def __eq__(self, other):
        if not isinstance(other, ShootingRecord):
            return False

        return all([
            self.date==other.date, 
            self.city==other.city, 
            self.state==other.state,
            self.dead==other.dead,
            self.injured==other.injured,
            self.description==other.description,
            self.occurrence==other.occurrence,
        ])

    def __hash__(self):
        hash = 0
        for attribute in ShootingRecord.attributes:
            if(attribute=='tweet_id'):
                continue
            hash = hash+self[attribute].__hash__()

        return hash

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get_updated_counterpart(self, updated_records):
        filtered_list = filter(lambda single_record: self.same_shooting(single_record), updated_records)
        return next((filtered_list), None)

    def __str__(self) -> str:
        return f'''
            city: "{self.city}"
            occurrence: {self.occurrence}
            state: "{self.state}"
            date: "{self.date}"
            dead: {self.dead}
            injured: {self.injured}
            description: "{self.description}"
            tweet_id: "{self.tweet_id}"
        '''