"""
Servicio de Aprendiz.

Mantiene la lógica de negocio y delega el acceso a datos al repositorio
correcto según DATABASE_ENGINE. La API no cambia, ni el frontend necesita
saber si la persistencia está en MySQL o MongoDB.
"""

from django.core.exceptions import ValidationError

from .models import Aprendiz
from .repositories import get_aprendiz_repository


class AprendizService:
    def __init__(self, repository=None):
        self.repository = repository or get_aprendiz_repository()

    def listar_todos(self):
        return self.repository.listar_todos()

    def obtener_por_id(self, id):
        return self.repository.obtener_por_id(id)

    def listar_por_ficha(self, ficha):
        return self.repository.obtener_por_ficha(ficha)

    def _validar_unicidad(self, datos_validados: dict, registro_actual=None):
        cedula = datos_validados.get("cedula")
        email = datos_validados.get("email")

        current_id = registro_actual.get("_id") if isinstance(registro_actual, dict) else getattr(registro_actual, "id", None)

        if cedula and self.repository.existe_cedula(cedula, current_id):
            raise ValidationError({"cedula": "Ya existe un aprendiz con esta cédula."})

        if email and self.repository.existe_email(email, current_id):
            raise ValidationError({"email": "Ya existe un aprendiz con este email."})

    def crear(self, datos_validados: dict):
        self._validar_unicidad(datos_validados)
        if self.repository.__class__.__name__ == "MongoAprendizRepository":
            return self.repository.guardar(datos_validados)
        aprendiz = Aprendiz(**datos_validados)
        return self.repository.guardar(aprendiz)

    def actualizar(self, aprendiz, datos_validados: dict):
        registro_actual = aprendiz if isinstance(aprendiz, dict) else self.repository.obtener_por_id(getattr(aprendiz, "id", None)) or aprendiz
        self._validar_unicidad(datos_validados, registro_actual)

        if self.repository.__class__.__name__ == "MongoAprendizRepository":
            return self.repository.actualizar(aprendiz.get("_id"), datos_validados)

        for campo, valor in datos_validados.items():
            setattr(aprendiz, campo, valor)
        return self.repository.guardar(aprendiz)

    def eliminar(self, aprendiz):
        if self.repository.__class__.__name__ == "MongoAprendizRepository":
            self.repository.eliminar(aprendiz.get("_id"))
            return
        self.repository.eliminar(aprendiz)
