import pandas as pd
import requests

class DataEnricher:
    def __init__(self, df):
        self.df = df

    def add_rainfall_data(self, api_key):
        base_url = "https://api.openweathermap.org/data/2.5/weather"

        # Get unique dates from the DataFrame
        dates_to_enrich = self.df['Trip Start Time'].dt.date.unique()

        for date in dates_to_enrich:
            date_str = str(date)
            timestamp = pd.Timestamp(date_str).timestamp()  # Convert date to Unix timestamp

            params = {
                "q": "Lagos",
                "appid": api_key,
                "units": "metric",
                "dt": int(timestamp)  # Convert timestamp to integer
            }

            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                weather_data = response.json()
                if 'rain' in weather_data:
                    rainfall = weather_data['rain'].get('1h', 0)  # Rainfall in the last hour (mm)
                    self.df.loc[self.df['Trip Start Time'].dt.date == date, 'Rainfall (mm)'] = rainfall
                else:
                    print("No rainfall data available for", date_str)
            else:
                print("Failed to fetch weather data for", date_str, ". Status code:", response.status_code)

# Instantiate DataEnricher
enricher = DataEnricher(df)

api_key = ''
enricher.add_rainfall_data(api_key)
