import subprocess
import sys
import os

def ejecutar_fase(ruta_script, descripcion):
    print(f"\n>>> Iniciando {descripcion}...")
    try:
        # Ejecuta el script de la fase correspondiente
        resultado = subprocess.run([sys.executable, ruta_script], check=True)
        print(f"{descripcion} completada con éxito.")
    except Exception as e:
        print(f"Error en {descripcion}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("INICIANDO PIPELINE AUTOMATIZADO")

    # Definimos las rutas exactas a los scripts dentro de la carpeta 'scripts'
    script_limpieza = os.path.join("scripts", "Limpieza_F2.py")
    script_carga = os.path.join("scripts", "Fase_3_cargar_datos.py")

    # Ejecutamos en orden
    ejecutar_fase(script_limpieza, "Fase 2: Limpieza y Transformación")
    ejecutar_fase(script_carga, "Fase 3: Modelado Estrella y Carga a PostgreSQL")

    print("PIPELINE FINALIZADO")