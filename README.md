# Backend Aprendiz — Django

API propia en Django + Django REST Framework para el CRUD de
Aprendices. No es un puerto directo del backend anterior en Spring
Boot: cumple la misma función (mismas rutas `/api/v1/aprendiz/...`,
mismo esquema de base de datos reciclado), pero está construido con
las convenciones naturales de Django.

## Arquitectura por capas

```
aprendiz/
├── models.py         Entidad Aprendiz (respeta el esquema ya
│                      existente en la base de datos reciclada)
├── repositories.py    Acceso a datos — envuelve el ORM
├── services.py        Lógica de negocio — a esto llaman las vistas
├── serializers.py      Traduce JSON <-> modelo, valida entrada
├── views.py             Controller — recibe el request HTTP, responde
├── urls.py               Rutas de la app
├── admin.py               Panel de administración de Django
├── tests.py                 Pruebas del API
└── migrations/
    ├── 0001_initial.py      Refleja el esquema ya existente (con
    │                         --fake-initial no se vuelve a crear)
    └── 0002_reglas_negocio.py   cedula única + choices de
                                  genero/jornada
```

Flujo de un request:

```
Request HTTP → urls.py → views.py (Controller)
                              ↓
                         services.py (reglas de negocio)
                              ↓
                       repositories.py (acceso a datos)
                              ↓
                          models.py (tabla 'aprendiz')
```

## Reglas de negocio implementadas

- `cedula`: única en el sistema (migración 0002 agrega el índice
  único — si ya hay cédulas duplicadas en tus datos reciclados, esta
  migración fallará y hay que limpiarlas primero).
- `email`: único (ya lo era en el esquema original).
- `genero`: solo admite `Masculino` o `Femenino`.
- `jornada`: solo admite `Diurna`, `Tarde` o `Nocturna`.
- `ficha`: texto libre. Se puede filtrar la lista completa por ficha:
  `GET /api/v1/aprendiz/?ficha=3173334`
- Sin autenticación: el API queda abierta, igual que el proyecto
  anterior.

## Endpoints

| Método | Ruta                          | Acción                          |
|--------|-------------------------------|----------------------------------|
| GET    | `/api/v1/aprendiz/`           | Lista todos los aprendices       |
| GET    | `/api/v1/aprendiz/?ficha=XXX` | Lista solo los de esa ficha      |
| POST   | `/api/v1/aprendiz/`           | Crea un aprendiz                 |
| GET    | `/api/v1/aprendiz/<id>/`      | Obtiene un aprendiz               |
| PUT    | `/api/v1/aprendiz/<id>/`      | Actualiza un aprendiz (parcial)   |
| DELETE | `/api/v1/aprendiz/<id>/`      | Elimina un aprendiz               |

## Cómo correr con Docker (recomendado)

1. Coloca `docker-compose.yml` en la raíz del proyecto (al mismo
   nivel que `django_aprendiz/` y `front_adso-main/`), reemplazando
   el que ya tenías.
2. Copia tu dump `.sql` existente dentro de
   `django_aprendiz/Mysql-init/` (reemplaza el placeholder
   `README.txt` que trae este paquete).
3. Desde la raíz del proyecto:
   ```powershell
   docker compose up -d --build
   ```
4. Verifica:
   ```powershell
   curl http://localhost:8080/api/v1/aprendiz/
   ```

## Cómo correr localmente (sin Docker, para desarrollo)

1. Copia `.env.example` a `.env` y ajusta `DB_PORT` según corresponda
   (ver comentarios dentro del archivo).
2. ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python manage.py migrate --fake-initial
   python manage.py runserver 0.0.0.0:8000
   ```
   Nota: en este modo el servidor queda en el puerto **8000**, no el
   8080 que usa Gunicorn dentro de Docker. Si vas a probar contra el
   frontend, asegúrate de que `API_BASE` en `aprendizService.js`
   apunte al puerto que estés usando realmente.

## Ejecutar las pruebas

```powershell
python manage.py test
```
