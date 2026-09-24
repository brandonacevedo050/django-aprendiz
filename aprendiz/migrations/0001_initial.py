from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Aprendiz",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(blank=True, db_column="nombre", max_length=255, null=True)),
                ("apellido", models.CharField(blank=True, db_column="apellido", max_length=255, null=True)),
                ("cedula", models.CharField(blank=True, db_column="cedula", max_length=255, null=True)),
                ("tipo_id", models.CharField(blank=True, db_column="tipo_id", max_length=255, null=True)),
                ("email", models.CharField(blank=True, db_column="email", max_length=255, null=True, unique=True)),
                ("telefono", models.CharField(blank=True, db_column="telefono", max_length=255, null=True)),
                ("direccion", models.CharField(blank=True, db_column="direccion", max_length=255, null=True)),
                ("genero", models.CharField(blank=True, db_column="genero", max_length=255, null=True)),
                ("ficha", models.CharField(blank=True, db_column="ficha", max_length=255, null=True)),
                ("jornada", models.CharField(blank=True, db_column="jornada", max_length=255, null=True)),
            ],
            options={
                "db_table": "aprendiz",
            },
        ),
    ]
