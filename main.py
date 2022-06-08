import requests
from bs4 import BeautifulSoup
from shooting_record import ShootingRecord

wikipedia_api_url = 'https://en.wikipedia.org/w/api.php'
wikipedia_page = 'List_of_mass_shootings_in_the_United_States_in_2022'

def main():
    rawHTML = fetch_wikipedia_page()
    return get_list(rawHTML)


def fetch_wikipedia_page():
    parameters = {
        'action': 'parse',
        'format': 'json',
        'page': wikipedia_page
    }

    response = requests.get(wikipedia_api_url, params=parameters)

    if response.status_code != 200:
        raise Exception('Invalid request')

    if 'error' in response.json():
        raise Exception(response.json()['error']['info'])

    return response.json()['parse']['text']['*']

def get_list(html_input):
    bs = BeautifulSoup(html_input, 'html.parser')
    table = bs.select("table")[0]

    rows = table.select("tr")[1:]
    shooting_records = []

    for row in rows:
        current_record = ShootingRecord.from_html_table_row(row)
        shooting_records.append(current_record)

    return shooting_records

if __name__ == '__main__':
   main()
