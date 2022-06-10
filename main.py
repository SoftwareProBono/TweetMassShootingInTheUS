import requests
from bs4 import BeautifulSoup
from csv_storage import CSVStorage
from shooting_record import ShootingRecord
from dotenv import load_dotenv

wikipedia_api_url = 'https://en.wikipedia.org/w/api.php'
wikipedia_page = 'List_of_mass_shootings_in_the_United_States_in_2022'

def main():
    load_dotenv()
    updated_records = get_list(fetch_wikipedia_page())
    stored_records = CSVStorage.get_saved_recods_from_csv()

    old_new_pairing = []
    for single_stored in stored_records:
        equal = False
        for single_updated in updated_records:
            if(single_stored.same_shooting(single_updated)):
                old_new_pairing.append((single_stored, single_updated))


    changed = []

    for (old, new) in old_new_pairing:
        if(not old.__eq__(new)):
            changed.append((old, new))
    
    # overwritten records in a list
    overwritten = [
        ShootingRecord(new.date, new.city, new.occurrence,  new.state, new.dead, new.injured, new.description, old.tweet_id)
        for (old, new) in old_new_pairing
    ]

    new_records = set(updated_records) - set(stored_records)

    new_end_state = []
    paired_olds = [old for (old) in old_new_pairing]

    for single_record in stored_records:
        if(single_record in paired_olds):
            new_end_state.append(single_record)
            continue
    
    for single_record in overwritten:
        new_end_state.append(single_record)

    for single_record in new_records:
        new_end_state.append(single_record)

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

def handle_changed_records(records):
    for record in records:
        if record.tweet_id != None:
            #update tweet
            pass
        else:
            #tweet
            pass

    return records

if __name__ == '__main__':
   main()
