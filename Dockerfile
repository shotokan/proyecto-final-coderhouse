# Usa una imagen base ligera de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en /root/airflow
WORKDIR /root/airflow

# Copia el archivo requirements.txt y luego instala las dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Instala Apache Airflow
RUN pip install apache-airflow

# Crea un directorio para los archivos del DAG
RUN mkdir -p /root/airflow/dags/src
RUN mkdir -p /root/airflow/dags/files

# Copia todos los archivos de src al directorio de trabajo en el contenedor
COPY src /root/airflow/dags/src
COPY files /root/airflow/dags/files

# Copia el archivo del DAG al directorio de DAGs
COPY dags/ /root/airflow/dags/

# Copia el script de inicialización
COPY init.sh /root/airflow/

# Dale permisos de ejecución al script
RUN chmod +x /root/airflow/init.sh

# Añade /root/airflow/dags al PYTHONPATH
ENV PYTHONPATH="/root/airflow/dags/src:${PYTHONPATH}"

# Exponer el puerto de Airflow WebServer (opcional)
EXPOSE 8080

# Inicia el contenedor con el script de inicialización
CMD ["/root/airflow/init.sh"]