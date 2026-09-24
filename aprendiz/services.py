"""
Servicio de Aprendiz.

Aquí vive la lógica de negocio: qué se permite hacer y bajo qué
condiciones. Las vistas (views.py) llaman a este servicio en vez de
hablar directo con el repositorio o el ORM.
"""

from .models import Aprendiz
from .repositories import AprendizRepository


class AprendizService:
    def __init__(self, repository: AprendizRepository = None):
        self.repository = repository or AprendizRepository()

    def listar_todos(self):
        return self.repository.listar_todos()

    def obtener_por_id(self, id):
        return self.repository.obtener_por_id(id)

    def listar_por_ficha(self, ficha):
        """Todos los aprendices inscritos en una ficha determinada."""
        return self.repository.obtener_por_ficha(ficha)

    def crear(self, datos_validados: dict) -> Aprendiz:
        aprendiz = Aprendiz(**datos_validados)
        return self.repository.guardar(aprendiz)

    def actualizar(self, aprendiz: Aprendiz, datos_validados: dict) -> Aprendiz:
        for campo, valor in datos_validados.items():
            setattr(aprendiz, campo, valor)
        return self.repository.guardar(aprendiz)

    def eliminar(self, aprendiz: Aprendiz):
        self.repository.eliminar(aprendiz)
