import psycopg2
import os
import pandas as pd
import sqlalchemy as sa

TABLE_NAME = 'weather_data_final'
DB_SCHEMA = 'isabido86_coderhouse'

class WeatherRepo:
    def __init__(self):
        db_name = os.getenv('DB_NAME', '')
        db_user = os.getenv('DB_USER', '')
        db_password = os.getenv('DB_PASSWORD', '')
        db_host = os.getenv('DB_HOST', '')
        db_port = os.getenv('DB_PORT', '')
        # self.conn = redshift_connector.connect(
        #                 host = db_host,
        #                 port = db_port,
        #                 user = db_user,
        #                 password = db_password,
        #                 database = db_name
        #               )
        self.engine = sa.create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')


    
    def insert(self, df_new):
        print('inserting... ')
        try: 
            query = f'SELECT * FROM {DB_SCHEMA}.{TABLE_NAME}'
            print(query)
            df_existing = pd.read_sql(query, self.engine)
            df_existing = df_existing.drop(columns=['id'])
            df_existing['is_existing'] = True
            df_new['is_existing'] = False
            print(df_existing)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.drop_duplicates(subset=['municipio', 'estado', 'current_last_updated_epoch'], keep='first', inplace=True)
            df_filtered_new = df_combined[df_combined['is_existing'] == False].drop(columns=['is_existing'])
            print('-----', df_filtered_new)
            df_filtered_new.to_sql(TABLE_NAME, con=self.engine, if_exists='append', index=False, schema=DB_SCHEMA)
            return df_filtered_new
        except sa.exc.SQLAlchemyError as e:
            print(f"Error occurred while dropping the table: {e}")
        except Exception as e:
            print(e)
       
        print('done...')
