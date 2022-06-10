import csv
from shooting_record import ShootingRecord
import os

class CSVStorage:

    @staticmethod
    def get_saved_recods_from_csv():
        shooting_records = []

        with open(os.getenv('DATA_FILE_PATH'), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                if row==ShootingRecord.attributes:
                    continue
                shooting_records.append(ShootingRecord(*row))

        return shooting_records

    @staticmethod
    def write_records_to_csv(shooting_records):

        with open(os.getenv('DATA_FILE_PATH'), 'w+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(ShootingRecord.attributes)

            for record in shooting_records:
                writer.writerow([record[attribute] for attribute in ShootingRecord.attributes])
