"""
Vistas de Aprendiz (capa Controller).

Equivalente a AprendizController en Spring Boot: recibe el request
HTTP, delega la lógica al service, y devuelve la respuesta. No habla
directo con el ORM ni con el repositorio.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AprendizSerializer
from .services import AprendizService


class AprendizListCreateView(APIView):
    """
    GET  /api/v1/aprendiz/            -> lista todos los aprendices
    GET  /api/v1/aprendiz/?ficha=XXXX -> lista solo los de esa ficha
    POST /api/v1/aprendiz/            -> crea un aprendiz nuevo
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AprendizService()

    def get(self, request):
        ficha = request.query_params.get("ficha")
        if ficha:
            aprendices = self.service.listar_por_ficha(ficha)
        else:
            aprendices = self.service.listar_todos()
        serializer = AprendizSerializer(aprendices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AprendizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        aprendiz = self.service.crear(serializer.validated_data)
        return Response(
            AprendizSerializer(aprendiz).data, status=status.HTTP_201_CREATED
        )


class AprendizDetailView(APIView):
    """
    GET    /api/v1/aprendiz/<id>/ -> obtiene un aprendiz
    PUT    /api/v1/aprendiz/<id>/ -> actualiza un aprendiz
    DELETE /api/v1/aprendiz/<id>/ -> elimina un aprendiz
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AprendizService()

    def _obtener_o_404(self, id):
        aprendiz = self.service.obtener_por_id(id)
        if aprendiz is None:
            return None
        return aprendiz

    def get(self, request, id):
        aprendiz = self._obtener_o_404(id)
        if aprendiz is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(AprendizSerializer(aprendiz).data)

    def put(self, request, id):
        aprendiz = self._obtener_o_404(id)
        if aprendiz is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AprendizSerializer(
            aprendiz, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        aprendiz = self.service.actualizar(aprendiz, serializer.validated_data)
        return Response(AprendizSerializer(aprendiz).data)

    def delete(self, request, id):
        aprendiz = self._obtener_o_404(id)
        if aprendiz is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.service.eliminar(aprendiz)
        return Response(status=status.HTTP_204_NO_CONTENT)
