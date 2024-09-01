# Usa la imagen oficial de PostgreSQL como base
FROM postgres:16.4

# Establece variables de entorno para la base de datos
ENV POSTGRES_DB=${DB_NAME}
ENV POSTGRES_USER=${DB_USER}
ENV POSTGRES_PASSWORD=${DB_PASS}

# Copia un archivo SQL opcional que se ejecutará al iniciar el contenedor
COPY ./init.sql /docker-entrypoint-initdb.d/

# Exponer el puerto PostgreSQL
EXPOSE 5432