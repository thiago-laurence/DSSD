# Ecocycle
Bienvenido a la documentación de la API de EcoCycle. Aquí encontrarás toda la información necesaria para interactuar con nuestra aplicación.
La misma es una aplicación web correspondiente al proyecto municipal "Ecocycle", el cual permite agrupar eslabones integrados en la economía circular, con el fin de promover el reciclado y actividades económicas sustentables entre los miembros de la comunidad.

<div align="center">
    <img width="80" src="https://1000marcas.net/wp-content/uploads/2021/06/Django-Logo.png" alt="Django logo" />
    <img width="80" src="https://avatars.githubusercontent.com/u/4619712?s=280&v=4" alt="BonitaSoft logo" />
</div>


| <img src="https://raw.githubusercontent.com/thiago-laurence/DSSD/refs/heads/main/app/ecocycle/static/img/logo.jpeg" alt="logo-ecocycle" width="100" /> | <img src="https://raw.githubusercontent.com/thiago-laurence/DSSD/refs/heads/main/app/ecocycle/static/img/home-page.png" alt="home" width="500" /> |
|--------------|--------------|

## URL de Producción

Enlace de sistema en producción sobre PaaS Render [Ecocycle](https://django-app-aer5.onrender.com).

## Documentación de API en Swagger

- **Archivo:** `openapi.yml`
- **URL para ver el documento Swagger:** [Swagger Editor](https://editor.swagger.io/)

## Credenciales de Usuarios

- **Usuario con rol Recolector:**
  - **Email:** walter.bates@example.com
  - **Contraseña:** bpm

- **Usuario con rol Centro:**
  - **Email:** april.sanchez@example.com
  - **Contraseña:** bpm
 
- **Usuario con rol Deposito:**
  - **Email:** misa.kumagai@example.com
  - **Contraseña:** bpm

- **Usuario con rol Administrador:**
  - **Email:** admin1@example.com
  - **Contraseña:** 123

---

¡Gracias por utilizar EcoCycle! Si tienes alguna pregunta, no dudes en contactarnos.

## Ejecucion local

El proyecto se encuentra dockerizado con sus respectivos servicios web Django y base de datos PostgreSQL.

    docker compose up -d --build

