#!/bin/sh
set -e

ENGINE="${DATABASE_ENGINE:-${DB_ENGINE:-mysql}}"

if [ "$ENGINE" = "mysql" ]; then
  echo "Esperando a que la base de datos MySQL esté disponible en ${DB_HOST:-mysql}:${DB_PORT:-3306}..."
  intentos=0
  hasta=30
  until mysqladmin ping --skip-ssl -h"${DB_HOST:-mysql}" -P"${DB_PORT:-3306}" -u"${DB_USER:-root}" -p"${DB_PASSWORD:-}" --silent; do
    intentos=$((intentos + 1))
    if [ "$intentos" -ge "$hasta" ]; then
      echo "MySQL no respondió después de $hasta intentos. Abortando."
      exit 1
    fi
    echo "  MySQL aún no disponible (intento $intentos/$hasta), reintentando en 2s..."
    sleep 2
  done
  echo "MySQL disponible."
  echo "Aplicando migraciones..."
  python manage.py migrate --fake-initial --noinput
else
  echo "DATABASE_ENGINE=${ENGINE}; se usa MongoDB. No se ejecutan migraciones SQL."
fi

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando servidor Gunicorn en el puerto 8080..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8080 --workers 3
