import requests
from bs4 import BeautifulSoup
import json

wikipedia_api_url = 'https://en.wikipedia.org/w/api.php'
wikipedia_page = 'List_of_mass_shootings_in_the_United_States_in_2022'


def main():
    rawHTML = fetch_wikipedia_page()
    return parse_html(rawHTML)


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

def parse_html(html_input):
    bs = BeautifulSoup(html_input, 'html.parser')
    return bs


if __name__ == '__main__':
    print(fetch_wikipedia_page())
