# ============================================================
# Imagen del backend Django (API propia, no un puerto del
# Spring Boot anterior — mismas funciones, arquitectura Django).
# ============================================================
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# build-essential + default-libmysqlclient-dev + pkg-config: para
# compilar mysqlclient. default-mysql-client: trae 'mysqladmin',
# usado por entrypoint.sh para esperar a que MySQL esté listo.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiamos primero solo requirements.txt para aprovechar la cache
# de Docker y no reinstalar dependencias en cada build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ahora copiamos el resto del código fuente.
# (.dockerignore excluye .venv, __pycache__, .env, etc.)
COPY . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]
