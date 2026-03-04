import pandas as pd
import difflib
import os


class DoctorAgent:

    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        csv_path = os.path.join(base_path, "data", "raw", "master_doctors_india.csv")

        self.df = pd.read_csv(csv_path)

    def recommend(self, specialty, city):

        specialty = specialty.strip().lower()
        city = city.strip().lower()

        # Normalize dataframe columns
        self.df["specialty"] = self.df["specialty"].str.lower()
        self.df["city"] = self.df["city"].str.lower()

        # Fuzzy match city
        all_cities = self.df["city"].unique().tolist()
        closest_city = difflib.get_close_matches(city, all_cities, n=1, cutoff=0.6)
        normalized_city = closest_city[0] if closest_city else city

        # Partial specialty match
        filtered = self.df[
            (self.df["specialty"].str.contains(specialty)) &
            (self.df["city"] == normalized_city)
        ]

        return filtered.head(3).to_dict(orient="records")