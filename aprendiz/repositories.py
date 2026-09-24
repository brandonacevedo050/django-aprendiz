"""
Repositorio de Aprendiz.

Envuelve las consultas al ORM de Django. El ORM ya actúa como el
"repository" técnico (equivalente a Spring Data JPA), pero mantenemos
esta capa explícita para separar responsabilidades: aquí solo vive
acceso a datos, nunca reglas de negocio ni validaciones.
"""

from .models import Aprendiz


class AprendizRepository:
    def listar_todos(self):
        return Aprendiz.objects.all()

    def obtener_por_id(self, id):
        return Aprendiz.objects.filter(id=id).first()

    def obtener_por_ficha(self, ficha):
        """Todos los aprendices inscritos en una ficha específica."""
        return Aprendiz.objects.filter(ficha=ficha)

    def existe_cedula(self, cedula, excluir_id=None):
        qs = Aprendiz.objects.filter(cedula=cedula)
        if excluir_id is not None:
            qs = qs.exclude(id=excluir_id)
        return qs.exists()

    def existe_email(self, email, excluir_id=None):
        qs = Aprendiz.objects.filter(email=email)
        if excluir_id is not None:
            qs = qs.exclude(id=excluir_id)
        return qs.exists()

    def guardar(self, aprendiz: Aprendiz):
        aprendiz.save()
        return aprendiz

    def eliminar(self, aprendiz: Aprendiz):
        aprendiz.delete()
