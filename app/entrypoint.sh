#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate --no-input

# Inicializar la base de datos
echo "Inicializando la base de datos..."
python manage.py init-db

echo "Fin entrypoint.sh"
# Ejecutar el comando pasado al contenedor (por defecto: runserver)
exec "$@"
