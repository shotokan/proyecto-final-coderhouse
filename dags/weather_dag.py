from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import os
import pandas as pd
import subprocess

# Definir argumentos predeterminados
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Función para verificar si el archivo existe
def check_municipios_file():
    file_path = '/root/airflow/dags/files/municipios.csv'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe")

# Función para ejecutar el script main.py
def run_main_script():
    subprocess.run(['python', '/root/airflow/dags/src/main.py'], check=True)

# Función para verificar si hay alguna fila con 'cloudy' en el campo 'current_condition_text'
def check_cloudy_condition():
    df = pd.read_csv('/root/airflow/dags/files/resultado.csv')
    print(df)
    if 'cloudy' in df['current_condition_text'].values:
        raise ValueError("Se encontró 'cloudy' en la columna current_condition_text")

# Definir el DAG
dag = DAG(
    'weather_dag',
    default_args=default_args,
    description='DAG para procesar datos de clima',
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2024, 1, 1),
    catchup=False
)

# Tarea para verificar si el archivo municipios existe
check_municipios = PythonOperator(
    task_id='check_municipios_file',
    python_callable=check_municipios_file,
    dag=dag,
)

# Tarea para ejecutar el script main.py
execute_main_script = PythonOperator(
    task_id='run_main_script',
    python_callable=run_main_script,
    dag=dag,
)

# Tarea para verificar si hay 'cloudy' en la columna 'current_condition_text'
check_for_cloudy = PythonOperator(
    task_id='check_cloudy_condition',
    python_callable=check_cloudy_condition,
    dag=dag,
)

# Tarea para enviar correo si no se encuentra el archivo municipios.csv
send_email_no_file = EmailOperator(
    task_id='send_email_no_file',
    to='shotokan.isc@gmail.com',
    subject='Error: No se encontró el archivo municipios.csv',
    html_content='El archivo municipios.csv no fue encontrado en el directorio /files.',
    dag=dag,
    trigger_rule='one_failed'
)

# Tarea para enviar correo si se encuentra 'cloudy'
send_email_cloudy = EmailOperator(
    task_id='send_email_cloudy',
    to='shotokan.isc@gmail.com',
    subject='Alerta: Condición "Cloudy" encontrada',
    html_content='Se encontró el texto "cloudy" en la columna current_condition_text.',
    dag=dag,
    trigger_rule='one_failed'
)

# Definir el flujo de tareas
check_municipios >> [execute_main_script, send_email_no_file]
execute_main_script >> check_for_cloudy >> send_email_cloudy