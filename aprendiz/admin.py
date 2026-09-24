from django.contrib import admin

from .models import Aprendiz


@admin.register(Aprendiz)
class AprendizAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido", "cedula", "email", "ficha", "jornada")
    search_fields = ("nombre", "apellido", "cedula", "email", "ficha")
    list_filter = ("genero", "jornada", "ficha")
