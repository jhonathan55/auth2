# Documentacion Tecnica del Proyecto OAuth2

Esta carpeta contiene la documentacion funcional y tecnica del proyecto Django de autenticacion con MFA y recuperacion de contrasena por codigo.

## Indice

1. [Arquitectura de Alto Nivel](./01-arquitectura-alto-nivel.md)
2. [Diseno de Bajo Nivel](./02-diseno-bajo-nivel.md)
3. [API REST](./03-api-rest.md)
4. [Modelo de Datos](./04-modelo-datos.md)
5. [Seguridad OWASP](./05-seguridad-owasp.md)
6. [Operacion y Despliegue](./06-operacion-despliegue.md)
7. [Inventario de Codigo](./07-inventario-codigo.md)

## Alcance

- Backend Django + Django REST Framework.
- Persistencia en MySQL.
- Contenedores Docker Compose para API y base de datos.
- Casos de uso: registro, login, MFA por email, recuperacion de contrasena con codigo de 6 digitos.

## Resumen de Componentes

- `oauth2_project/`: configuracion principal del proyecto Django.
- `OAuth2/`: app de dominio de autenticacion.
- `OAuth2/services/`: servicios de MFA, correo y recuperacion.
- `OAuth2/models.py`: entidades `AppUser` y `MFAChallenge`.
- `docker-compose.yml`: orquestacion local de API + MySQL.
- `Dockerfile`: imagen de ejecucion de la API.

## Convenciones de esta documentacion

- Alto nivel: vistas de arquitectura, responsabilidades, integraciones.
- Bajo nivel: clases, funciones, validaciones, estados y transiciones.
- Seguridad: controles actuales y brechas para roadmap.
- Diagramas: Mermaid para poder renderizarse en Markdown moderno.
