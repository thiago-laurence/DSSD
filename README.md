# Ecocycle
Bienvenido a la documentación de la API de EcoCycle. Aquí encontrarás toda la información necesaria para interactuar con nuestra aplicación.
La misma es una aplicación web correspondiente al proyecto municipal "Ecocycle", el cual permite agrupar eslabones integrados en la economía circular, con el fin de promover el reciclado y actividades económicas sustentables entre los miembros de la comunidad.


## URL de Producción

[https://django-app-aer5.onrender.com](https://django-app-aer5.onrender.com)

## Endpoints de la API

### 1. Agregar Pedido

- **Método:** POST  
- **URI:** `/ecocycle/api/pedidos/add`  
- **PROD:** https://django-app-aer5.onrender.com/ecocycle/api/pedidos/add
- **Estructura de cuerpo de la solicitud:**

    ```json
    {
      "deposito": 88,
      "material": "Acero",
      "cantidad": 100
    }
    ```

### 2. Obtener Usuario

- **Método:** GET  
- **URI:** `/ecocycle/api/user/`  
- **PROD:** https://django-app-aer5.onrender.com/ecocycle/api/user/

### 3. Iniciar Sesión

- **Método:** POST  
- **URI:** `/ecocycle/api/login/`  
- **PROD:** https://django-app-aer5.onrender.com/ecocycle/api/login/
- **Estructura de cuerpo de la solicitud:**

    ```json
    {
      "email": "walter.bates@example.com",
      "password": "bpm"
    }
    ```

## Usuarios

- **Usuario con rol Recolector:**
  - **Email:** walter.bates@example.com
  - **Contraseña:** bpm

- **Usuario con rol Centro:**
  - **Email:** centro1@example.com
  - **Contraseña:** 123

- **Usuario con rol Administrador:**
  - **Email:** admin1@example.com
  - **Contraseña:** 123

## Documentación Swagger

- **Archivo:** `openapi.yml`  
- **URL para ver el documento Swagger:** [Swagger Editor](https://editor.swagger.io/)

---

¡Gracias por utilizar EcoCycle! Si tienes alguna pregunta, no dudes en contactarnos.



<center>
    <img width="200" src="https://1000marcas.net/wp-content/uploads/2021/06/Django-Logo.png" alt="Django logo" />
</center>

