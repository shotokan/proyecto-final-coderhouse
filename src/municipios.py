

import os

import pandas as pd


class Municipios:
    def __init__(self):
        # Obtener la ruta absoluta del directorio raíz
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construir la ruta del archivo CSV
        csv_file_path = os.path.join(root_dir, 'files', 'municipios.csv')
        
        # Cargar el archivo CSV en un DataFrame de Pandas
        self.data = pd.read_csv(csv_file_path)
    
    def get_df(self):
        # Mostrar las primeras filas del archivo CSV
        return self.data
    
    def show_data(self):
        # Mostrar las primeras filas del archivo CSV
        print(self.data.head())
    
    def filter_by_region(self, region):
        print(self.data['estado'])
        return self.data[self.data['estado'] == region]
