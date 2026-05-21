"""
Módulo encargado de generar información ficticia
de clientes para simular un entorno bancario.

El objetivo es construir un fichero RAW CSV
que posteriormente será utilizado por procesos ETL.

Este dataset simula solicitudes de crédito
realizadas por clientes.
"""

# ==========================================================
# IMPORTS
# ==========================================================

import csv
import random
import uuid

from datetime import datetime, timedelta

from faker import Faker


# ==========================================================
# CONFIGURACIÓN FAKER
# ==========================================================

# Configuramos Faker con localización UK
# para generar nombres, teléfonos y ciudades
# más realistas para el caso de uso.
fake = Faker("en_GB")


# ==========================================================
# CATÁLOGOS
# ==========================================================

# Posibles estados laborales del cliente
EMPLOYMENT_STATUS = [
    "EMPLOYED",
    "SELF_EMPLOYED",
    "UNEMPLOYED",
    "RETIRED",
    "STUDENT"
]

# Estado civil
MARITAL_STATUS = [
    "SINGLE",
    "MARRIED",
    "DIVORCED",
    "WIDOWED"
]

# Situación de vivienda
HOUSING_STATUS = [
    "OWNED",
    "MORTGAGED",
    "RENTED",
    "FAMILY_HOME"
]

# Motivo de solicitud del préstamo
LOAN_PURPOSE = [
    "MORTGAGE",
    "CAR",
    "PERSONAL",
    "BUSINESS",
    "EDUCATION"
]


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def random_date(start_year=2018, end_year=2025):
    """
    Genera una fecha aleatoria entre dos años.

    Args:
        start_year (int): Año inicial
        end_year (int): Año final

    Returns:
        str: Fecha en formato YYYY-MM-DD
    """

    start_date = datetime(start_year, 1, 1)

    end_date = datetime(end_year, 12, 31)

    delta = end_date - start_date

    random_days = random.randint(0, delta.days)

    return (
        start_date + timedelta(days=random_days)
    ).strftime("%Y-%m-%d")


def calculate_risk(
        annual_income,
        credit_score,
        debt_to_income_ratio
):
    """
    Calcula el riesgo financiero simplificado
    del cliente.

    Reglas:
    - LOW:
        Buen credit score y bajo endeudamiento
    - MEDIUM:
        Riesgo medio
    - HIGH:
        Alto riesgo

    Args:
        annual_income (int):
            Ingresos anuales

        credit_score (int):
            Puntuación crediticia

        debt_to_income_ratio (float):
            Ratio deuda / ingresos

    Returns:
        str:
            Categoría de riesgo
    """

    if credit_score >= 750 and debt_to_income_ratio < 30:
        return "LOW"

    elif credit_score >= 600 and debt_to_income_ratio < 50:
        return "MEDIUM"

    return "HIGH"


# ==========================================================
# GENERACIÓN DE CLIENTES
# ==========================================================

def generate_customer():
    """
    Genera un único cliente ficticio.

    Returns:
        dict:
            Información del cliente
    """

    # ======================================================
    # GENERACIÓN DE DATOS FINANCIEROS
    # ======================================================

    annual_income = random.randint(18000, 150000)

    existing_debt = random.randint(0, 80000)

    credit_score = random.randint(300, 850)

    loan_amount = random.randint(5000, 500000)

    # ======================================================
    # CÁLCULO DEL RATIO DEUDA / INGRESOS
    # ======================================================

    debt_to_income_ratio = round(
        (existing_debt / annual_income) * 100,
        2
    )

    # ======================================================
    # CÁLCULO DEL RIESGO
    # ======================================================

    risk_category = calculate_risk(
        annual_income,
        credit_score,
        debt_to_income_ratio
    )

    # ======================================================
    # CONSTRUCCIÓN DEL CLIENTE
    # ======================================================

    return {

        # Identificador único de la solicitud
        "application_id": str(uuid.uuid4()),

        # Identificador único del cliente
        "customer_id": str(uuid.uuid4()),

        # ==================================================
        # INFORMACIÓN PERSONAL
        # ==================================================

        "first_name": fake.first_name(),

        "last_name": fake.last_name(),

        "gender": random.choice(["M", "F"]),

        "date_of_birth": fake.date_of_birth(
            minimum_age=18,
            maximum_age=75
        ),

        "email": fake.email(),

        "phone_number": fake.phone_number(),

        "country": "UK",

        "city": fake.city(),

        # ==================================================
        # INFORMACIÓN LABORAL
        # ==================================================

        "employment_status": random.choice(
            EMPLOYMENT_STATUS
        ),

        "job_title": fake.job(),

        "years_in_current_job": random.randint(0, 40),

        # ==================================================
        # INFORMACIÓN FINANCIERA
        # ==================================================

        "annual_income": annual_income,

        "monthly_expenses": random.randint(500, 5000),

        "existing_debt": existing_debt,

        "credit_score": credit_score,

        "bank_balance": random.randint(0, 200000),

        # ==================================================
        # INFORMACIÓN DEL PRÉSTAMO
        # ==================================================

        "loan_amount_requested": loan_amount,

        "loan_purpose": random.choice(
            LOAN_PURPOSE
        ),

        "loan_term_months": random.choice(
            [12, 24, 36, 48, 60, 120, 240, 360]
        ),

        # ==================================================
        # INFORMACIÓN DE RIESGO
        # ==================================================

        "debt_to_income_ratio": debt_to_income_ratio,

        "risk_category": risk_category,

        # ==================================================
        # INFORMACIÓN FAMILIAR
        # ==================================================

        "marital_status": random.choice(
            MARITAL_STATUS
        ),

        "housing_status": random.choice(
            HOUSING_STATUS
        ),

        "number_of_dependents": random.randint(0, 5),

        # ==================================================
        # METADATA
        # ==================================================

        "application_date": random_date(),

        "record_creation_timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


# ==========================================================
# GENERACIÓN DEL CSV
# ==========================================================

def generate_customers_csv(number_of_customers,output_path ):
    """
    Genera un fichero CSV con clientes ficticios.

    Args:
        number_of_customers (int):
            Número de clientes a generar

        output_path (str):
            Ruta del fichero de salida
    """

    print(
        f"Generando {number_of_customers} clientes..."
    )

    # Generamos lista de clientes
    customers = [
        generate_customer()
        for _ in range(number_of_customers)
    ]

    # Extraemos nombres de columnas
    fieldnames = customers[0].keys()

    # ======================================================
    # ESCRITURA CSV
    # ======================================================

    with open(
            output_path,
            mode="w",
            newline="",
            encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        # Escribimos cabecera
        writer.writeheader()

        # Escribimos registros
        writer.writerows(customers)

    print(
        f"CSV generado correctamente: {output_path}"
    )