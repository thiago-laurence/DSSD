-- CREATE DATABASE ecocycle;

CREATE USER AdminGrupo1 WITH PASSWORD 'AdminPass';

GRANT
    ALL PRIVILEGES
ON DATABASE ecocycle TO AdminGrupo1;

\c ecocycle

GRANT ALL 
ON SCHEMA public TO AdminGrupo1;