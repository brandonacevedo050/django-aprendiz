"""
Serializer de Aprendiz.

Django REST Framework no tiene equivalente directo en Spring Boot:
aquí se define qué campos se exponen en el JSON, y las validaciones
automáticas (como unicidad de cedula/email) que corren antes de que
el dato llegue al service.
"""

from rest_framework import serializers

from .models import Aprendiz


class AprendizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aprendiz
        fields = [
            "id",
            "nombre",
            "apellido",
            "cedula",
            "tipo_id",
            "email",
            "telefono",
            "direccion",
            "genero",
            "ficha",
            "jornada",
        ]
