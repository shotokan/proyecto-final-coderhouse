#!/bin/bash

# Inicializa la base de datos
airflow db init

# Crea las conexiones predeterminadas
airflow connections create-default-connections

# Inicia el scheduler y el webserver
airflow scheduler & airflow webserver