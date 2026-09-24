#!/bin/sh
set -e

if [ "${DB_ENGINE:-mysql}" = "mysql" ]; then
  echo "Esperando a que la base de datos MySQL esté disponible en ${DB_HOST:-mysql}:${DB_PORT:-3306}..."
  intentos=0
  hasta=30
  until mysqladmin ping -h"${DB_HOST:-mysql}" -P"${DB_PORT:-3306}" -u"${DB_USER:-root}" -p"${DB_PASSWORD:-}" --silent; do
    intentos=$((intentos + 1))
    if [ "$intentos" -ge "$hasta" ]; then
      echo "MySQL no respondió después de $hasta intentos. Abortando."
      exit 1
    fi
    echo "  MySQL aún no disponible (intento $intentos/$hasta), reintentando en 2s..."
    sleep 2
  done
  echo "Base de datos disponible."
else
  echo "DB_ENGINE=${DB_ENGINE:-sqlite3}; usando SQLite local para esta ejecución."
fi

# --fake-initial: la tabla 'aprendiz' ya la crea el dump de Mysql-init/
# al arrancar el contenedor de MySQL, así que Django no debe intentar
# crearla de nuevo (fallaría con "table already exists"). Esto le dice
# a Django que revise si la tabla ya existe con esa forma y, si es así,
# solo marque esa migración como aplicada sin volver a correr el SQL.
# La migración 0002 (reglas de negocio nuevas) sí se ejecuta normal.
echo "Aplicando migraciones..."
python manage.py migrate --fake-initial --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando servidor Gunicorn en el puerto 8080..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8080 --workers 3
