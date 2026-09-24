from django.test import TestCase
from rest_framework.test import APIClient


class AprendizAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_crear_y_listar_aprendiz(self):
        payload = {
            "nombre": "Brandon",
            "apellido": "Test",
            "cedula": "1000000001",
            "email": "brandon.test@example.com",
            "genero": "Masculino",
            "jornada": "Diurna",
            "ficha": "3173334",
        }
        respuesta = self.client.post("/api/v1/aprendiz/", payload, format="json")
        self.assertEqual(respuesta.status_code, 201)

        respuesta_lista = self.client.get("/api/v1/aprendiz/")
        self.assertEqual(respuesta_lista.status_code, 200)
        self.assertEqual(len(respuesta_lista.data), 1)

    def test_cedula_duplicada_falla(self):
        payload = {"nombre": "A", "cedula": "111", "email": "a@example.com"}
        self.client.post("/api/v1/aprendiz/", payload, format="json")

        payload_duplicado = {"nombre": "B", "cedula": "111", "email": "b@example.com"}
        respuesta = self.client.post(
            "/api/v1/aprendiz/", payload_duplicado, format="json"
        )
        self.assertEqual(respuesta.status_code, 400)

    def test_filtrar_por_ficha(self):
        self.client.post(
            "/api/v1/aprendiz/",
            {"nombre": "A", "cedula": "1", "email": "a@x.com", "ficha": "111"},
            format="json",
        )
        self.client.post(
            "/api/v1/aprendiz/",
            {"nombre": "B", "cedula": "2", "email": "b@x.com", "ficha": "222"},
            format="json",
        )
        respuesta = self.client.get("/api/v1/aprendiz/?ficha=111")
        self.assertEqual(len(respuesta.data), 1)
        self.assertEqual(respuesta.data[0]["nombre"], "A")
