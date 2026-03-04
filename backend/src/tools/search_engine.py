import pandas as pd
from src.utils.config import DATA_PATH


class DoctorSearchEngine:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)

    def search(self, specialty, city, urgency):
        df = self.df.copy()

        # Normalize text comparison
        df["specialty"] = df["specialty"].str.lower()
        df["city"] = df["city"].str.lower()
        df["availability"] = df["availability"].str.lower()

        specialty = specialty.lower()
        city = city.lower()
        urgency = urgency.lower()

        # Filter by specialty and city
        filtered = df[
            (df["specialty"] == specialty) &
            (df["city"] == city)
        ]

        # Emergency logic
        if urgency == "emergency":
            filtered = filtered[
                filtered["availability"].isin(["on-call", "immediate"])
            ]

        if filtered.empty:
            return []

        # Sort by rating + experience
        filtered = filtered.sort_values(
            by=["rating", "experience_years"],
            ascending=[False, False]
        )

        # Return top 3 doctors
        return filtered.head(3).to_dict(orient="records")