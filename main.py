from shutil import unpack_archive
import requests
from bs4 import BeautifulSoup
from csv_storage import CSVStorage
from shooting_record import ShootingRecord
from dotenv import load_dotenv

from twitter import Twitter

wikipedia_api_url = 'https://en.wikipedia.org/w/api.php'
wikipedia_page = 'List_of_mass_shootings_in_the_United_States_in_2022'

def main():
    load_dotenv()
    updated_records = get_list(fetch_wikipedia_page())
    stored_records = CSVStorage.get_saved_recods_from_csv()

    old_new_pairing = []
    for single_stored in stored_records:
        for single_updated in updated_records:
            if(single_stored.same_shooting(single_updated)):
                old_new_pairing.append((single_stored, single_updated))


    paired_olds = [old for (old) in old_new_pairing]

    # overwritten records in a list
    overwritten = [
        ShootingRecord(new.date, new.city, new.occurrence,  new.state, new.dead, new.injured, new.description, old.tweet_id)
        for (old, new) in old_new_pairing
    ]
    new_records = set(updated_records) - set(stored_records)
    unchanged_records = (list(set(stored_records) & (set(paired_olds))))

    new_end_state = []
    new_end_state.extend(unchanged_records)
    new_end_state.extend(overwritten)
    new_end_state.extend(new_records)

    handle_changed_records(new_records)
    CSVStorage.write_records_to_csv(new_end_state)

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

def ordinal_suffix(number):
    modulus = number % 10
    if modulus == 1:
        return 'st'
    elif modulus == 2:
        return 'nd'
    elif modulus == 3:
        return 'rd'
    else:
        return 'th'


def handle_changed_records(records):
    if(len(records) == 0):
        return records

    client = Twitter()
    client.refresh_tokens()

    for record in records:
        if record.tweet_id != None:
            #update tweet
            pass
        else:
            client.tweet(f'Another sad day in America. Mass Shooting in {record.city} in {record.state} on {record.date} 2022. {str(record.dead)} dead. {str(record.injured)} injured. This is the {str(record.occurrence) + ordinal_suffix(record.occurrence)} shooting this year in this city.')

    return records

if __name__ == '__main__':
   main()
