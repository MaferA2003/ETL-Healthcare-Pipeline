import pandas as pd
import os

print("\nIniciando Fase 2: Limpieza y Transformación")

# 1. Ajuste de rutas
ruta_entrada = 'dataset/healthcare_dataset.csv'
ruta_salida = 'dataset/healthcare_dataset_clean.csv'

# Verificamos que el archivo original exista antes de empezar
if not os.path.exists(ruta_entrada):
    print(f"Error: No se encontró el archivo {ruta_entrada}")
    exit(1)

# Leemos el archivo CSV
print(f"Archivo crudo: {ruta_entrada}")
df = pd.read_csv(ruta_entrada)

# Limpieza de Datos

# 1. Eliminamos filas donde todo es igual.
antes_dup = len(df)
df = df.drop_duplicates()
print(f"Se eliminaron {antes_dup - len(df)} duplicados exactos.")

# 2. Normalización de Textos
# a) Pacientes: Regex a prueba de fallos para quitar títulos (Mr, Mrs, Ms, Miss, Dr)
df['Name'] = df['Name'].str.replace(r'(?i)^\s*(mr|mrs|ms|miss|dr)\.?\s+', '', regex=True)
df['Name'] = df['Name'].str.title().str.strip()

# b) Hospitales: Quitamos "and/&" sueltos en los extremos y comas
df['Hospital'] = df['Hospital'].str.replace(r'(?i)^\s*(and|&)\s+|\s+(and|&)\s*$', '', regex=True)
df['Hospital'] = df['Hospital'].str.strip(', ').str.title()

# c) Doctores: Quitamos "Dr." y ponemos Formato Título
df['Doctor'] = df['Doctor'].str.replace(r'(?i)^\s*dr\.?\s+', '', regex=True)
df['Doctor'] = df['Doctor'].str.title().str.strip()

# 3. Manejo de Inconsistencias
columnas_ancla = ['Name', 'Date of Admission', 'Hospital', 'Medical Condition']
antes_inc = len(df)
df = df.drop_duplicates(subset=columnas_ancla, keep='last')
print(f"Se corrigieron {antes_inc - len(df)} registros con inconsistencias.")

# 4. Limpieza de Facturación: Pasamos a valor absoluto y redondeamos
df['Billing Amount'] = df['Billing Amount'].abs().round(2)

# 5. Conversión de Fechas y Cálculo de Estancia
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])

# Calculamos los días y nos aseguramos que existan valores negativos
df['Days Admitted'] = (df['Discharge Date'] - df['Date of Admission']).dt.days
df = df[df['Days Admitted'] >= 0]

# 6. Comprobación Final
print(f"Existen {len(df)} Registros listos para BD.")

# Guardar el archivo

# Verificamos si el archivo ya existe
if os.path.exists(ruta_salida):
    os.remove(ruta_salida) 
    print("Archivo limpio anterior detectado y eliminado.")
else:
    print("No se encontró un archivo previo. Se creará uno nuevo.")

# Guardamos el nuevo dataset limpio
df.to_csv(ruta_salida, index=False)
print(f"Se guardo correctamente el dataset en: {ruta_salida}\n")