from datetime import datetime, timedelta
from BenefizClient import BenefizClient

def main(days_past, days_future, boat_schedule_name: str, training_schedule_name: str, trainer_schedule_name: str):
    # Create an instance of BenefizClient with the provided schedule names
    client = BenefizClient(boat_schedule_name, training_schedule_name, trainer_schedule_name)

    # Get sorted appointments within the specified date range
    apps = client.get_appointments_sorted(datetime.now() - timedelta(days=days_past), datetime.now() + timedelta(days=days_future))
    
    # Process each appointment
    for app in apps:
        # Remove unnecessary fields
        del app["trainer_id"]
        del app["boat_id"]
        del app["id"]
        
        # Rename fields to match the desired output format
        app["Startzeit"] = app.pop("start")
        app["Endzeit"] = app.pop("finish")
        app["E-Mailadresse Team"] = app.pop("created_by")
        app["Team Ansprechpartner"] = app.pop("full_name")
        app["Handynummer"] = app.pop("mobile")
        app["Boot"] = app.pop("boat_name")
        app["Trainer"] = app.pop("trainer_name")
    
    import csv

    # Write the processed appointments to a CSV file
    with open('trainings.csv', 'w', newline='', encoding='UTF-8') as csvfile:
        fieldnames = apps[0].keys()  # Get the field names from the first appointment
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header row
        for app in apps:
            writer.writerow(app)  # Write each appointment as a row
    print("Finished writing to trainings.csv")

if __name__ == "__main__":
    import os
    # Call the main function with environment variables or default values
    main(
        int(os.getenv("DAYS_PAST", 10)),
        int(os.getenv("DAYS_FUTURE", 7)),
        boat_schedule_name=os.getenv("BOAT_SCHEDULE_NAME", "Test Winter"),
        training_schedule_name=os.getenv("TRAINING_SCHEDULE_NAME", "Benefiz Plan"),
        trainer_schedule_name=os.getenv("TRAINER_SCHEDULE_NAME", "Personen")
    )

