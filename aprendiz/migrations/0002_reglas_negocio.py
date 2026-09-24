"""
Aplica las reglas de negocio nuevas sobre la tabla ya existente:

  - cedula pasa a ser única (esto SÍ ejecuta un ALTER TABLE para crear
    el índice único — si ya existieran cédulas duplicadas en los
    datos reciclados, esta migración fallará y hay que limpiarlas
    primero).
  - genero y jornada reciben `choices` (Diurna/Tarde/Nocturna y
    Masculino/Femenino). Esto NO ejecuta ningún ALTER TABLE real en
    MySQL: la columna sigue siendo VARCHAR(255), solo cambia la
    validación del lado de Django/DRF.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aprendiz", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aprendiz",
            name="cedula",
            field=models.CharField(
                blank=True, db_column="cedula", max_length=255, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="aprendiz",
            name="genero",
            field=models.CharField(
                blank=True,
                choices=[("Masculino", "Masculino"), ("Femenino", "Femenino")],
                db_column="genero",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="aprendiz",
            name="jornada",
            field=models.CharField(
                blank=True,
                choices=[("Diurna", "Diurna"), ("Tarde", "Tarde"), ("Nocturna", "Nocturna")],
                db_column="jornada",
                max_length=255,
                null=True,
            ),
        ),
    ]
