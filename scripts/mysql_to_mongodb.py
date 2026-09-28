#!/usr/bin/env python
"""
Migra registros de Aprendiz desde MySQL hacia MongoDB sin borrar los datos
originales. Se ejecuta de forma controlada y reporta cuántos registros
fueron insertados.

Uso:
    python scripts/mysql_to_mongodb.py

Requiere:
    - MySQL disponible y Django conectado a MySQL
    - MONGODB_URI y MONGODB_NAME configurados
"""

import os
import sys

import django
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

def main():
    engine = os.environ.get("DATABASE_ENGINE", os.environ.get("DB_ENGINE", "mysql")).lower()
    if engine != "mysql":
        print(
            "Este importador requiere DATABASE_ENGINE=mysql o DB_ENGINE=mysql; "
            f"motor detectado: {engine!r}."
        )
        return 1

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    from aprendiz.models import Aprendiz

    mongo_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    mongo_name = os.environ.get("MONGODB_NAME", "aprendiz")

    client = MongoClient(mongo_uri)
    collection = client[mongo_name]["aprendiz"]
    collection.create_index("cedula", unique=True, sparse=True)
    collection.create_index("email", unique=True, sparse=True)
    collection.create_index("ficha")

    registros = list(Aprendiz.objects.all().order_by("id"))
    total_origen = len(registros)
    insertados = 0
    duplicados = 0

    for aprendiz in registros:
        documento = {
            "mysql_id_original": aprendiz.id,
            "nombre": aprendiz.nombre,
            "apellido": aprendiz.apellido,
            "cedula": aprendiz.cedula,
            "tipo_id": aprendiz.tipo_id,
            "email": aprendiz.email,
            "telefono": aprendiz.telefono,
            "direccion": aprendiz.direccion,
            "genero": aprendiz.genero,
            "ficha": aprendiz.ficha,
            "jornada": aprendiz.jornada,
        }

        try:
            collection.insert_one(documento)
            insertados += 1
        except DuplicateKeyError:
            duplicados += 1
            print(f"Registro duplicado omitido: id={aprendiz.id}, cedula={aprendiz.cedula}, email={aprendiz.email}")

    print(f"Registros en MySQL: {total_origen}")
    print(f"Registros insertados en MongoDB: {insertados}")
    print(f"Registros duplicados omitidos: {duplicados}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
