from inspect import getargs
import re

class ShootingRecord:

    def __init__(self, date, city, occurrence, state, dead, injured, description):
        self.date = date
        self.city = city
        self.occurrence = occurrence
        self.state = state
        self.dead = dead
        self.injured = injured
        self.description = description

    @staticmethod
    def from_html_table_row(html):
        arguments = []
        arguments.append(html.select('td:nth-child(1)')[0].get_text().replace(u'\xa0', ' ').strip())
        arguments.append(*ShootingRecord.extract_data_from_city_entry(html.select('td:nth-child(2)')[0].get_text().replace(u'\xa0', ' ').strip()))
        arguments.append(html.select('td:nth-child(3)')[0].get_text().replace(u'\xa0', ' ').strip())
        arguments.append(html.select('td:nth-child(4)')[0].get_text().replace(u'\xa0', ' ').strip())
        arguments.append(html.select('td:nth-child(5)')[0].get_text().replace(u'\xa0', ' ').strip())
        arguments.append(html.select('td:nth-child(7)')[0].get_text().replace(u'\xa0', ' ').strip())
        
        return ShootingRecord(*arguments)

    @staticmethod
    def extract_data_from_city_entry(entry):
        regex = r'(?P<cityName>.*)(?: \((?P<occurence>\d+)\))?'
        match = re.search(regex, entry)
        city_name = match.group('cityName')
        occurrence = match.group('occurrence')

        return [city_name, occurrence if occurrence else 1]

    def __eq__(self, other):
        if not isinstance(other, ShootingRecord):
            return False
        
        return all([
            self.date==other.date, 
            self.city==other.city, 
            self.state==other.state,
            self.dead==other.dead,
            self.injured==other.injured,
        ])

    def __getitem__(self, key):
        return getattr(self, key, None)