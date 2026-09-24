"""
Modelo Aprendiz.

IMPORTANTE: esta tabla ya existe en la base de datos (se reutilizó la
del proyecto anterior). Los campos, tipos y db_column respetan ese
esquema para no romper los datos existentes. Las únicas reglas nuevas
que SÍ se aplican aquí son:

  - cedula: única (requiere la migración 0002, que agrega el índice
    único en la base de datos).
  - genero / jornada: choices — esto es validación a nivel de Django
    únicamente. MySQL sigue viendo la columna como VARCHAR normal,
    así que no se altera el tipo de columna ni se pierden datos
    existentes que no encajen exactamente (aunque sí se validarán
    los valores nuevos que entren desde el API).
"""

from django.db import models


class Genero(models.TextChoices):
    MASCULINO = "Masculino", "Masculino"
    FEMENINO = "Femenino", "Femenino"


class Jornada(models.TextChoices):
    DIURNA = "Diurna", "Diurna"
    TARDE = "Tarde", "Tarde"
    NOCTURNA = "Nocturna", "Nocturna"


class Aprendiz(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=255, db_column="nombre", blank=True, null=True
    )
    apellido = models.CharField(
        max_length=255, db_column="apellido", blank=True, null=True
    )
    cedula = models.CharField(
        max_length=255,
        db_column="cedula",
        unique=True,
        blank=True,
        null=True,
    )
    tipo_id = models.CharField(
        max_length=255, db_column="tipo_id", blank=True, null=True
    )
    email = models.CharField(
        max_length=255, db_column="email", unique=True, blank=True, null=True
    )
    telefono = models.CharField(
        max_length=255, db_column="telefono", blank=True, null=True
    )
    direccion = models.CharField(
        max_length=255, db_column="direccion", blank=True, null=True
    )
    genero = models.CharField(
        max_length=255,
        db_column="genero",
        choices=Genero.choices,
        blank=True,
        null=True,
    )
    ficha = models.CharField(
        max_length=255, db_column="ficha", blank=True, null=True
    )
    jornada = models.CharField(
        max_length=255,
        db_column="jornada",
        choices=Jornada.choices,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "aprendiz"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
