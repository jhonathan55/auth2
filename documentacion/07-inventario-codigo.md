# Inventario de Codigo Fuente

## 1. Raiz del Proyecto

- `manage.py`: entrypoint de comandos Django.
- `requirements.txt`: dependencias Python.
- `Dockerfile`: construccion de imagen backend.
- `docker-compose.yml`: orquestacion local API + MySQL.
- `.env.example`: plantilla de variables de entorno.

## 2. Proyecto Django `oauth2_project/`

- `__init__.py`: paquete Python.
- `settings.py`: configuracion global (DB, apps, correo, logging, i18n).
- `urls.py`: enrutamiento raiz (`/admin/`, `/api/auth/`).
- `asgi.py`: callable ASGI.
- `wsgi.py`: callable WSGI.

## 3. App `OAuth2/`

- `app.py`: configuracion de la app Django (`OAuth2Config`).
- `admin.py`: configuracion del admin para `AppUser` y `MFAChallenge`.
- `models.py`: modelos del dominio (`AppUser`, `MFAChallenge`).
- `serializers.py`: validacion de request payloads.
- `urls.py`: rutas de autenticacion y recuperacion.
- `views.py`: implementacion de endpoints REST.

## 4. Servicios de Dominio `OAuth2/services/`

- `mfa_service.py`: generacion y verificacion de MFA por codigo de 6 digitos.
- `email_service.py`: envio de emails MFA y recuperacion.
- `password_recovery_service.py`: flujo seguro de recuperacion y cambio de contrasena.

## 5. Migraciones `OAuth2/migrations/`

- `0001_initial.py`: creacion inicial de tablas.
- `0002_mfachallenge_verified_at.py`: agrega `verified_at` para separar verificacion y consumo en recovery.

## 6. Dependencias no codificadas directamente

- Motor MySQL 8.4.
- Servidor SMTP (Gmail) para notificaciones.

## 7. Nota tecnica

Actualmente no se detectaron archivos de tests automaticos en el arbol mostrado. Se recomienda crear pruebas unitarias e integracion para los flujos de seguridad.
