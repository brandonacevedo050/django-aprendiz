"""
Serializer de Aprendiz.

Se mantiene una representación común para que MySQL y MongoDB entreguen
exactamente el mismo JSON en la API. El objetivo es que el frontend no
sepa si la fuente es MySQL o MongoDB.
"""

from rest_framework import serializers

from .repositories import get_aprendiz_repository


class AprendizSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombre = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    apellido = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    cedula = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    tipo_id = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    telefono = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    direccion = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    genero = serializers.ChoiceField(
        choices=["Masculino", "Femenino"],
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    ficha = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    jornada = serializers.ChoiceField(
        choices=["Diurna", "Tarde", "Nocturna"],
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    def to_representation(self, instance):
        if instance is None:
            return {}

        if isinstance(instance, dict):
            data = {
                "id": str(instance["_id"]) if instance.get("_id") is not None else None,
                "nombre": instance.get("nombre"),
                "apellido": instance.get("apellido"),
                "cedula": instance.get("cedula"),
                "tipo_id": instance.get("tipo_id"),
                "email": instance.get("email"),
                "telefono": instance.get("telefono"),
                "direccion": instance.get("direccion"),
                "genero": instance.get("genero"),
                "ficha": instance.get("ficha"),
                "jornada": instance.get("jornada"),
            }
        else:
            data = {
                "id": getattr(instance, "id", None),
                "nombre": getattr(instance, "nombre", None),
                "apellido": getattr(instance, "apellido", None),
                "cedula": getattr(instance, "cedula", None),
                "tipo_id": getattr(instance, "tipo_id", None),
                "email": getattr(instance, "email", None),
                "telefono": getattr(instance, "telefono", None),
                "direccion": getattr(instance, "direccion", None),
                "genero": getattr(instance, "genero", None),
                "ficha": getattr(instance, "ficha", None),
                "jornada": getattr(instance, "jornada", None),
            }

        if data.get("id") is not None:
            data["id"] = str(data["id"])

        return {
            "id": data.get("id"),
            "nombre": data.get("nombre"),
            "apellido": data.get("apellido"),
            "cedula": data.get("cedula"),
            "tipo_id": data.get("tipo_id"),
            "email": data.get("email"),
            "telefono": data.get("telefono"),
            "direccion": data.get("direccion"),
            "genero": data.get("genero"),
            "ficha": data.get("ficha"),
            "jornada": data.get("jornada"),
        }

    def validate(self, attrs):
        repo = get_aprendiz_repository()
        cedula = attrs.get("cedula")
        email = attrs.get("email")
        current_id = self.instance.get("_id") if isinstance(self.instance, dict) else getattr(self.instance, "id", None)

        if cedula and repo.existe_cedula(cedula, current_id):
            raise serializers.ValidationError({"cedula": "Ya existe un aprendiz con esta cédula."})

        if email and repo.existe_email(email, current_id):
            raise serializers.ValidationError({"email": "Ya existe un aprendiz con este email."})

        return attrs
