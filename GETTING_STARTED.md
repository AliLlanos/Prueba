# 🚀 Guía de Inicio Rápido - ERP Professional

¡Bienvenido a **ERP Professional**! Esta guía te ayudará a poner en marcha el sistema de gestión empresarial más moderno y completo en pocos minutos.

## 📋 Tabla de Contenidos

1. [Prerrequisitos](#-prerrequisitos)
2. [Instalación Rápida](#-instalación-rápida)
3. [Primer Acceso](#-primer-acceso)
4. [Estructura del Proyecto](#-estructura-del-proyecto)
5. [Comandos Útiles](#-comandos-útiles)
6. [Configuración Avanzada](#-configuración-avanzada)
7. [Solución de Problemas](#-solución-de-problemas)

## 🔧 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

### Requerimientos Obligatorios
- **Docker**: [Instalar Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Instalar Docker Compose](https://docs.docker.com/compose/install/)

### Requerimientos del Sistema
- **RAM**: Mínimo 4GB (Recomendado 8GB)
- **Almacenamiento**: 5GB de espacio libre
- **Puertos**: 3000, 8000, 5432, 8080 disponibles

### Verificación de Instalación
```bash
# Verificar Docker
docker --version

# Verificar Docker Compose
docker-compose --version

# Verificar que Docker esté ejecutándose
docker info
```

## 🚀 Instalación Rápida

### Opción 1: Inicio Automático (Recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd erp-professional

# Ejecutar script de inicio automático
./start-erp.sh
```

**¡Eso es todo!** El script automático:
- ✅ Verifica dependencias
- ✅ Configura el entorno
- ✅ Construye las imágenes Docker
- ✅ Inicializa la base de datos
- ✅ Inicia todos los servicios
- ✅ Verifica que todo funcione correctamente

### Opción 2: Inicio Manual

```bash
# 1. Crear archivo de configuración
cp .env.example .env

# 2. Construir imágenes
docker-compose build

# 3. Iniciar servicios
docker-compose up -d

# 4. Verificar estado
docker-compose ps
```

## 🔑 Primer Acceso

Una vez que todos los servicios estén funcionando, puedes acceder a:

### 🌐 Interfaz Principal
**URL**: http://localhost:3000

**Credenciales de Administrador**:
- 📧 **Email**: `admin@erpro.com`
- 🔑 **Contraseña**: `admin123`

### 📚 Documentación de API
**URL**: http://localhost:8000/docs

### 🗄️ Administración de Base de Datos
**URL**: http://localhost:8080

**Credenciales de Base de Datos**:
- **Sistema**: PostgreSQL
- **Servidor**: postgres
- **Usuario**: `erp_user`
- **Contraseña**: `erp_password_2024`
- **Base de datos**: `erp_professional`

## 📁 Estructura del Proyecto

```
erp-professional/
├── 🐍 backend/                 # Backend FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints REST
│   │   ├── core/              # Configuración
│   │   ├── models/            # Modelos de DB
│   │   ├── schemas/           # Validación
│   │   └── services/          # Lógica de negocio
│   ├── tests/                 # Tests automatizados
│   ├── alembic/               # Migraciones de DB
│   └── requirements.txt       # Dependencias Python
├── ⚛️ frontend/                # Frontend React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── pages/             # Páginas
│   │   ├── store/             # Estado (Redux)
│   │   ├── services/          # APIs
│   │   └── types/             # Tipos TypeScript
│   └── package.json           # Dependencias Node.js
├── 🐳 docker-compose.yml       # Configuración Docker
├── 🚀 start-erp.sh            # Script de inicio
└── 📖 README.md               # Documentación
```

## 🛠️ Comandos Útiles

### Gestión de Servicios

```bash
# Iniciar ERP completo
./start-erp.sh start

# Parar todos los servicios
./start-erp.sh stop

# Reiniciar servicios
./start-erp.sh restart

# Ver estado de servicios
./start-erp.sh status

# Ver logs en tiempo real
./start-erp.sh logs

# Limpiar todo (¡CUIDADO! Borra datos)
./start-erp.sh clean
```

### Comandos Docker Compose

```bash
# Ver logs de un servicio específico
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Acceder a un container
docker-compose exec backend bash
docker-compose exec frontend sh

# Reconstruir un servicio
docker-compose build backend
docker-compose up -d backend

# Ver recursos utilizados
docker-compose top
```

### Comandos de Base de Datos

```bash
# Acceder a PostgreSQL
docker-compose exec postgres psql -U erp_user -d erp_professional

# Crear backup de base de datos
docker-compose exec postgres pg_dump -U erp_user erp_professional > backup.sql

# Restaurar backup
docker-compose exec -T postgres psql -U erp_user erp_professional < backup.sql

# Ver tablas
docker-compose exec postgres psql -U erp_user -d erp_professional -c "\dt"
```

## ⚙️ Configuración Avanzada

### Variables de Entorno

Edita el archivo `.env` para personalizar:

```bash
# Configuración de la aplicación
PROJECT_NAME=Mi ERP Personalizado
ENVIRONMENT=production

# Seguridad (¡CAMBIAR EN PRODUCCIÓN!)
SECRET_KEY=tu-clave-super-secreta-aqui

# Base de datos
POSTGRES_PASSWORD=tu-password-seguro

# Usuario administrador
FIRST_SUPERUSER_EMAIL=mi-admin@empresa.com
FIRST_SUPERUSER_PASSWORD=password-seguro
```

### Configuración de Producción

Para entorno de producción:

1. **Cambiar credenciales por defecto**
2. **Configurar HTTPS**
3. **Configurar respaldos automáticos**
4. **Configurar monitoreo**

```bash
# Ejemplo para producción
ENVIRONMENT=production
SECRET_KEY=clave-super-secreta-de-produccion
POSTGRES_PASSWORD=password-muy-seguro
```

### Puertos Personalizados

Si necesitas cambiar puertos:

```yaml
# En docker-compose.yml
services:
  frontend:
    ports:
      - "8080:80"  # Cambiar frontend a puerto 8080
  backend:
    ports:
      - "9000:8000"  # Cambiar backend a puerto 9000
```

## 🚨 Solución de Problemas

### Problemas Comunes

#### 1. Error "Puerto ya en uso"
```bash
# Verificar qué proceso usa el puerto
lsof -i :3000
lsof -i :8000

# Cambiar puertos en docker-compose.yml o detener proceso
```

#### 2. Error de conexión a base de datos
```bash
# Verificar que PostgreSQL esté ejecutándose
docker-compose ps postgres

# Verificar logs de PostgreSQL
docker-compose logs postgres

# Reiniciar servicio de base de datos
docker-compose restart postgres
```

#### 3. Frontend no carga
```bash
# Verificar logs del frontend
docker-compose logs frontend

# Reconstruir frontend
docker-compose build frontend
docker-compose up -d frontend
```

#### 4. Backend responde 500
```bash
# Verificar logs del backend
docker-compose logs backend

# Verificar configuración
docker-compose exec backend env | grep DATABASE_URL
```

### Comandos de Diagnóstico

```bash
# Estado completo del sistema
docker-compose ps
docker system df
docker system info

# Verificar conectividad
curl http://localhost:8000/health
curl http://localhost:3000

# Logs detallados
docker-compose logs --timestamps --follow
```

### Reinicio Completo

Si nada funciona, reinicio completo:

```bash
# Parar todo
docker-compose down

# Limpiar volúmenes (¡CUIDADO! Borra datos)
docker-compose down -v

# Limpiar imágenes
docker system prune -a

# Volver a construir
./start-erp.sh start
```

## 📞 Soporte y Ayuda

### Documentación Adicional
- 📚 **API Docs**: http://localhost:8000/docs
- 🔧 **Admin Panel**: http://localhost:8000/admin
- 📖 **Wiki**: [Documentación completa](docs/)

### Contacto
- 📧 **Email**: soporte@erpro.com
- 💬 **Chat**: [Discord/Slack]
- 🐛 **Bugs**: [GitHub Issues](issues/)

### Recursos Útiles
- [Guía de Docker](https://docs.docker.com/get-started/)
- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Documentación React](https://react.dev/)

---

## ✨ ¡Siguiente Pasos!

Una vez que tengas ERP Professional funcionando:

1. **🎯 Explora el Dashboard** - Familiarízate con la interfaz
2. **👥 Crea Usuarios** - Añade empleados y asigna roles
3. **🏢 Configura tu Empresa** - Personaliza información empresarial
4. **📦 Gestiona Inventario** - Añade productos y categorías
5. **🛒 Procesa Ventas** - Crea cotizaciones y órdenes
6. **📊 Revisa Reportes** - Analiza métricas de negocio

**¡Bienvenido a la nueva era de gestión empresarial! 🚀**