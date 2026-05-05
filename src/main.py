"""
Main entry point del proyecto.

Este módulo se encarga de:
1. Definir parámetros globales
2. Lanzar el proceso de generación de datos
3. Guardar el fichero RAW CSV

El objetivo es simular un fichero de entrada
para un proceso ETL bancario.
"""

# Importamos la función encargada de generar
# el fichero CSV con clientes ficticios
from generators.customer_generator import (
    generate_customers_csv
)

# ==========================================================
# CONFIGURACIÓN GLOBAL
# ==========================================================

# Número de clientes que queremos generar
NUMBER_OF_CUSTOMERS = 1000

# Ruta donde se almacenará el CSV RAW
OUTPUT_PATH = (
    "../data/raw/raw_credit_applications.csv"
)


# ==========================================================
# MAIN
# ==========================================================

def main():
    """
    Función principal del proyecto.

    Lanza el proceso de generación del CSV.
    """

    print("Iniciando generación de clientes...")

    generate_customers_csv(
        number_of_customers=NUMBER_OF_CUSTOMERS,
        output_path=OUTPUT_PATH
    )

    print("Proceso finalizado correctamente.")


# ==========================================================
# ENTRY POINT
# ==========================================================

# Este bloque garantiza que el programa
# solo se ejecuta si este fichero es lanzado
# directamente desde Python.
if __name__ == "__main__":
    main()