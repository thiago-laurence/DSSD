#!/bin/sh

echo "📦 Aplicando migraciones..."
python manage.py migrate

echo "🔧 Inicializando base de datos..."
python manage.py init-db

echo "🚀 Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000