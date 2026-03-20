import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Cargar las variables de entorno desde el archivo .env
load_dotenv()

# 2. Obtener datos
db_password = os.getenv('DB_PASSWORD')
db_user = os.getenv('DB_USER')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')


# 3. Leer los datos limpios
print("Leyendo dataset limpio...")
df = pd.read_csv('dataset/healthcare_dataset_clean.csv')

# 4. Configurar la conexión a PostgreSQL usando f-strings
cadena_conexion = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(cadena_conexion)

print("Creando modelo en estrella")

# Creación de Dimensiones 

# Dimensión Hospital
dim_hospital = df[['Hospital']].drop_duplicates().reset_index(drop=True)
dim_hospital['hospital_id'] = dim_hospital.index + 1

# Dimensión Doctor
dim_doctor = df[['Doctor']].drop_duplicates().reset_index(drop=True)
dim_doctor['doctor_id'] = dim_doctor.index + 1

# Dimensión Aseguradora
dim_seguro = df[['Insurance Provider']].drop_duplicates().reset_index(drop=True)
dim_seguro['seguro_id'] = dim_seguro.index + 1

# Creación de la tabla de Hechos

# Unimos los IDs creados con la tabla original
df_hechos = df.merge(dim_hospital, on='Hospital')
df_hechos = df_hechos.merge(dim_doctor, on='Doctor')
df_hechos = df_hechos.merge(dim_seguro, on='Insurance Provider')

# Seleccionamos las columnas finales para fact_admissions 
columnas_finales = [
    'Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition',
    'Date of Admission', 'Discharge Date', 'Days Admitted',
    'hospital_id', 'doctor_id', 'seguro_id',
    'Billing Amount', 'Room Number', 'Admission Type',
    'Medication', 'Test Results'
]
fact_admissions = df_hechos[columnas_finales]

# Cargar a la base de Datow
print("Subiendo tablas a PostgreSQL")

# Subimos las dimensiones
dim_hospital.to_sql('dim_hospital', engine, if_exists='replace', index=False)
dim_doctor.to_sql('dim_doctor', engine, if_exists='replace', index=False)
dim_seguro.to_sql('dim_seguro', engine, if_exists='replace', index=False)

# Subimos la tabla de hechos
fact_admissions.to_sql('fact_admissions', engine, if_exists='replace', index=False)

print("Carga exitosa")