import requests
import os
import pandas as pd

class WeatherAPI:
    def __init__(self) -> None:
        key = os.getenv('API_WEATHER_KEY', '')
        self.__url = f'https://api.weatherapi.com/v1/current.json?key={key}'
    
    def getCurrent(self, cities):
        data=[]
        print(cities)
        for city in cities:
            current_weather_url = self.__url + f'&q={city}'
            print(current_weather_url)
            response = requests.get(current_weather_url)
            if response.status_code == 200:
                data.append(response.json())
            else:
                print(f'Error {response.status_code}: {response.text}')

        return data
    
    def get_df(self, data):
        weather_df = pd.json_normalize(data)

        print(weather_df.head())
       
        filtered_df = pd.DataFrame({
            'municipio': weather_df['location.name'],
            'estado': weather_df['location.region'],
            'country': weather_df['location.country'],
            'lat': weather_df['location.lat'],
            'lon': weather_df['location.lon'],
            'tz_id': weather_df['location.tz_id'],
            'temperatura': weather_df['current.temp_c'],
            'humedad': weather_df['current.humidity'],
            'viento_kph': weather_df['current.wind_kph'],
            'localtime_epoch': weather_df['location.localtime_epoch'],
            'local_time': weather_df['location.localtime'],
            'current_last_updated_epoch': weather_df['current.last_updated_epoch'],
            'current_last_updated': weather_df['current.last_updated'],
            'current_condition_text': weather_df['current.condition.text'],
            'current_is_day': weather_df['current.is_day'],
            'current_temp_f': weather_df['current.temp_f'],
            'current_wind_degree': weather_df['current.wind_degree'],
            'current_wind_dir': weather_df['current.wind_dir'],
        })
        return filtered_df