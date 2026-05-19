# Operacion y Despliegue

## 1. Requisitos

- Docker
- Docker Compose

## 2. Estructura de Infraestructura

- `Dockerfile`: construye imagen Python 3.12 con dependencias de MySQL client.
- `docker-compose.yml`:
  - servicio `oauth2-api` (Django)
  - servicio `mysql` (MySQL 8.4)
  - volumen persistente `oauth2_mysql_data`

## 3. Variables de Entorno

Referencia principal: `.env` y `.env.example`.

Variables criticas:

- Base de datos: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- Email SMTP: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`
- Remitente: `DEFAULT_FROM_EMAIL`

## 4. Ciclo de Arranque

El servicio API ejecuta:

1. `python manage.py migrate --noinput`
2. `python manage.py runserver 0.0.0.0:8000`

Esto evita desalineacion entre modelo y esquema de BD al desplegar cambios.

## 5. Comandos Operativos

### 5.1 Levantar stack

```bash
docker compose up --build
```

### 5.2 Ver migraciones

```bash
docker compose exec oauth2-api python manage.py showmigrations OAuth2
```

### 5.3 Crear nuevas migraciones

```bash
docker compose run --rm oauth2-api python manage.py makemigrations
```

### 5.4 Aplicar migraciones

```bash
docker compose run --rm oauth2-api python manage.py migrate
```

### 5.5 Verificacion basica

```bash
docker compose run --rm oauth2-api python manage.py check
```

## 6. Dependencias Python

- `django`
- `djangorestframework`
- `mysqlclient`
- `python-dotenv`
- `django-cors-headers`
- `PyJWT`

## 7. Observabilidad Basica

- Logger `OAuth2` configurado en `settings.py`.
- Eventos de envio de email y recuperacion de contrasena.

## 8. Pendientes recomendados para produccion

- Gunicorn/Uvicorn en lugar de `runserver`.
- Proxy reverso (Nginx) con TLS.
- Health checks de API.
- Rotacion de logs y centralizacion.
- Backups de MySQL.
