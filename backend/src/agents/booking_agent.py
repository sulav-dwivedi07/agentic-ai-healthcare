import csv
import os
from datetime import datetime


class BookingAgent:

    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.file_path = os.path.join(base_path, "data", "processed", "bookings.csv")

    def book(self, patient_name, doctor):

        appointment_date = datetime.now().strftime("%Y-%m-%d")
        appointment_time = "Tomorrow 10:00 AM"

        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                patient_name,
                doctor["name"],
                doctor["hospital"],
                doctor["city"],
                appointment_date,
                appointment_time,
                "confirmed"
            ])

        return {
            "status": "confirmed",
            "doctor": doctor["name"],
            "hospital": doctor["hospital"],
            "date": appointment_date,
            "time": appointment_time
        }