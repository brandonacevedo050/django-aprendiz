"""
Repositorio de Aprendiz.

Se mantiene la capa de acceso a datos para MySQL y se añade una
implementación compatible con MongoDB usando PyMongo. La API continúa
igual, sin que el frontend tenga que conocer la base de datos interna.
"""

import os

from bson import ObjectId
from bson.errors import InvalidId
from django.conf import settings
from pymongo import MongoClient

from .models import Aprendiz


class AprendizRepository:
    def listar_todos(self):
        return Aprendiz.objects.all()

    def obtener_por_id(self, id):
        if id is None:
            return None
        try:
            id_int = int(str(id))
        except (TypeError, ValueError):
            return None
        return Aprendiz.objects.filter(id=id_int).first()

    def obtener_por_ficha(self, ficha):
        """Todos los aprendices inscritos en una ficha específica."""
        return Aprendiz.objects.filter(ficha=ficha)

    def existe_cedula(self, cedula, excluir_id=None):
        qs = Aprendiz.objects.filter(cedula=cedula)
        if excluir_id is not None:
            try:
                excluir_id = int(str(excluir_id))
            except (TypeError, ValueError):
                pass
            qs = qs.exclude(id=excluir_id)
        return qs.exists()

    def existe_email(self, email, excluir_id=None):
        qs = Aprendiz.objects.filter(email=email)
        if excluir_id is not None:
            try:
                excluir_id = int(str(excluir_id))
            except (TypeError, ValueError):
                pass
            qs = qs.exclude(id=excluir_id)
        return qs.exists()

    def guardar(self, aprendiz: Aprendiz):
        aprendiz.save()
        return aprendiz

    def eliminar(self, aprendiz: Aprendiz):
        aprendiz.delete()


class MongoAprendizRepository:
    def __init__(self):
        mongo_uri = os.environ.get("MONGODB_URI", getattr(settings, "MONGODB_URI", "mongodb://localhost:27017"))
        mongo_name = os.environ.get("MONGODB_NAME", getattr(settings, "MONGODB_NAME", "aprendiz"))
        self.client = MongoClient(mongo_uri)
        self.collection = self.client[mongo_name]["aprendiz"]
        self._ensure_indexes()

    def _ensure_indexes(self):
        self.collection.create_index("cedula", unique=True, sparse=True)
        self.collection.create_index("email", unique=True, sparse=True)
        self.collection.create_index("ficha")

    def _get_object_id(self, id):
        if id is None:
            return None
        if isinstance(id, ObjectId):
            return id
        try:
            return ObjectId(str(id))
        except (InvalidId, TypeError):
            return None

    def listar_todos(self):
        return list(self.collection.find({}))

    def obtener_por_id(self, id):
        oid = self._get_object_id(id)
        if oid is None:
            return None
        return self.collection.find_one({"_id": oid})

    def obtener_por_ficha(self, ficha):
        return list(self.collection.find({"ficha": ficha}))

    def existe_cedula(self, cedula, excluir_id=None):
        query = {"cedula": cedula}
        if excluir_id is not None:
            oid = self._get_object_id(excluir_id)
            if oid is not None:
                query["_id"] = {"$ne": oid}
        return self.collection.find_one(query) is not None

    def existe_email(self, email, excluir_id=None):
        query = {"email": email}
        if excluir_id is not None:
            oid = self._get_object_id(excluir_id)
            if oid is not None:
                query["_id"] = {"$ne": oid}
        return self.collection.find_one(query) is not None

    def guardar(self, aprendiz):
        payload = dict(aprendiz)
        payload.pop("_id", None)
        payload.pop("id", None)
        result = self.collection.insert_one(payload)
        return self.collection.find_one({"_id": result.inserted_id})

    def actualizar(self, id, datos_validados):
        oid = self._get_object_id(id)
        if oid is None:
            return None
        datos = dict(datos_validados)
        datos.pop("_id", None)
        datos.pop("id", None)
        self.collection.update_one({"_id": oid}, {"$set": datos})
        return self.collection.find_one({"_id": oid})

    def eliminar(self, id):
        oid = self._get_object_id(id)
        if oid is None:
            return
        self.collection.delete_one({"_id": oid})


def get_aprendiz_repository():
    engine = os.environ.get("DATABASE_ENGINE", os.environ.get("DB_ENGINE", "mysql")).lower()
    if engine == "mongodb":
        return MongoAprendizRepository()
    return AprendizRepository()
