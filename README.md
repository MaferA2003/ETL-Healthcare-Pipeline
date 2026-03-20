# Pipeline de Datos Hospitalarios (ETL) & Dashboard Analítico

## Descripción del Proyecto
Este proyecto es una solución de Ingeniería de Datos y Business Intelligence para el sector salud. Extrae datos crudos de ingresos hospitalarios, realiza una limpieza profunda, modela los datos en un Esquema de Estrella y los carga automáticamente a una base de datos PostgreSQL. Finalmente, la información se visualiza en un dashboard interactivo en Power BI.

## Tecnologías Utilizadas
* **Lenguaje:** Python 3
* **Librerías Principales:** Pandas, SQLAlchemy, psycopg2, python-dotenv
* **Base de Datos:** PostgreSQL (pgAdmin 4)
* **Visualización:** Power BI
* **Orquestación:** Módulo `subprocess` de Python

## Arquitectura del Proyecto
1. **Fase 1 (Exploración de Datos):** Análisis inicial del dataset crudo para identificar valores nulos, duplicados e inconsistencias lógicas.
2. **Fase 2 (Limpieza y Transformación):** Estandarización de textos usando Regex (eliminación de títulos redundantes como Dr./Mr., limpieza de caracteres), manejo de inconsistencias y creación de la métrica calculada `Days Admitted`.
3. **Fase 3 (Modelado Estrella):** Normalización del DataFrame limpio en 1 Tabla de Hechos (`fact_admissions`) y 3 Tablas de Dimensiones (`dim_hospital`, `dim_doctor`, `dim_seguro`).
4. **Fase 4 (Visualización):** Conexión de Power BI a PostgreSQL para responder a 5 preguntas clave de negocio mediante un dashboard interactivo.
5. **Fase 5 (Orquestación):** Ejecución automatizada del flujo completo de inicio a fin mediante un script maestro.


## Instrucciones ejecutar este proyecto

### Paso 1: Preparar los Datos
1. Extraiga el archivo `healthcare_dataset.csv.zip` que se encuentra en la raíz del proyecto.
2. Coloque el archivo extraído (`healthcare_dataset.csv`) dentro de la carpeta `dataset/`.

### Paso 2: Instalar Dependencias
Asegúrese de tener Python instalado. Abra su terminal en la carpeta raíz del proyecto y ejecute el siguiente comando para instalar las librerías necesarias:
```bash
pip install pandas sqlalchemy psycopg2 python-dotenv
```
### Paso 3: Configurar la Base de Datos
1. Abra pgAdmin o su gestor de PostgreSQL y cree una base de datos vacía llamada exactamente `healthcare_db`.
2. El script asume que su usuario de PostgreSQL es el predeterminado (`postgres`) y el puerto es `5432`.
3. En la raíz de este proyecto, busque el archivo `.env.example`.
4. Renómbrelo a `.env` y coloque únicamente su contraseña local de PostgreSQL:
   ```text
   DB_PASSWORD=su_contraseña_aqui

### Paso 4: Ejecutar el Pipeline (Fase 5)
Abra su terminal en la carpeta raíz del proyecto y ejecute el script orquestador:
```bash
python Fase_5_orquestador.py
```
*El script limpiará los datos automáticamente, generará el modelo relacional y creará las tablas directamente en su base de datos PostgreSQL.*

### Paso 5: Visualización en Power BI
Puede abrir el archivo `Fase_4_Reporte_Hospitalario.pbix` incluido en la carpeta para interactuar con el dashboard final. 
Nota: Para actualizar los datos en Power BI, deberá editar los parámetros de origen de datos para que apunten a su servidor `localhost` con sus credenciales.
