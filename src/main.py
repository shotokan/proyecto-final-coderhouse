

import pandas as pd
from municipios import Municipios
from db import WeatherRepo
from wheater import WeatherAPI


def execute():
    db = WeatherRepo()
    api = WeatherAPI()
    mun = Municipios()
    cities = mun.filter_by_region('Yucatán')['municipio'].tolist()
    municipios_df = mun.get_df()
    print(cities[:3])
    resp = api.getCurrent(cities[:3])
    weather_df = api.get_df(resp)
    print(weather_df)
    merged_df = pd.merge(weather_df, municipios_df, on='municipio', suffixes=('_weather', '_municipio'))
    merged_df = merged_df.drop(columns=['estado_weather'])  # Elimina la que no necesites
    merged_df = merged_df.rename(columns={'estado_municipio': 'estado'})

    print(merged_df.head())
    df_store = db.insert(merged_df)
    df_store.to_csv('/root/airflow/dags/files/resultado.csv', index=False)

    

if __name__ == '__main__':
    execute()