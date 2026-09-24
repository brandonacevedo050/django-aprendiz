"""
URLs raíz del proyecto.

Aquí se define el prefijo real del API: /api/v1/aprendiz/...
El mismo esquema que usaba el backend anterior en Spring Boot, para
que el frontend (aprendizService.js) no tenga que cambiar sus rutas.
"""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def api_root(request):
    return HttpResponse(
        '<h1>API funcionando</h1>'
        '<p><a href="/api/v1/aprendiz/">Ir a la API de aprendices</a></p>'
    )


urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api/v1/aprendiz/", include("aprendiz.urls")),
]
