

import pandas as pd
from municipios import Municipios
from wheater import WeatherAPI


def execute():
    api = WeatherAPI()
    mun = Municipios()
    cities = mun.filter_by_region('Yucatán')['municipio'].tolist()
    municipios_df = mun.get_df()
    print(cities[:3])
    resp = api.getCurrent(cities[:3])
    weather_df = api.get_df(resp)
    print(weather_df)
    merged_df = pd.merge(weather_df, municipios_df, on='municipio')
    print(merged_df)
    # mun.show_data()

    

if __name__ == '__main__':
    execute()