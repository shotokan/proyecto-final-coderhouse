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
        weather_df = weather_df.rename(columns={
            'location.name': 'municipio',
            'location.region': 'estado',
            'location.country': 'country',
            'current.temp_c': 'temperatura',
            'current.humidity': 'humedad',
            'current.wind_kph': 'viento_kph'
        })
        return weather_df