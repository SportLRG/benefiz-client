from datetime import datetime, timedelta
from BenefizClient import BenefizClient


def main(days_past, days_future, boat_schedule_name: str, training_schedule_name: str, trainer_schedule_name: str):

    client = BenefizClient(boat_schedule_name, training_schedule_name, trainer_schedule_name)

    apps = client.get_appointments_sorted(datetime.now() - timedelta(days=days_past), datetime.now() + timedelta(days=days_future))
    import csv

    with open('trainings.csv', 'w', newline='') as csvfile:
        fieldnames = apps[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for app in apps:
            writer.writerow(app)

if __name__ == "__main__":
    import os
    main(
            int(os.getenv("DAYS_PAST", 10)),
            int(os.getenv("DAYS_FUTURE", 7)),
            boat_schedule_name=os.getenv("BOAT_SCHEDULE_NAME", "Test Winter"),
            training_schedule_name=os.getenv("TRAINING_SCHEDULE_NAME", "Benefiz Plan"),
            trainer_schedule_name=os.getenv("TRAINER_SCHEDULE_NAME", "Personen")
        )

