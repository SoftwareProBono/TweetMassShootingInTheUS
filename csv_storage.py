import csv
from shooting_record import ShootingRecord

class CSVStorage:

    attributes = ['date', 'city', 'state', 'dead', 'injured', 'description']

    @staticmethod
    def get_saved_recods_from_csv():
        shooting_records = []

        with open('data.csv', 'r') as file:
            reader = csv.reader(file)

            for row in reader[1:]:
                shooting_records.append(ShootingRecord(*row))

        return shooting_records

    @staticmethod
    def write_records_to_csv(shooting_records):

        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSVStorage.attributes)

            for record in shooting_records:
                writer.writerow([record[attribute] for attribute in CSVStorage.attributes])
