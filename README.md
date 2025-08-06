# 🏢 ERP Professional - Sistema de Gestión Empresarial

## 🌟 Descripción

ERP Professional es un sistema de gestión empresarial completo y moderno, diseñado con arquitectura profesional para manejar todos los aspectos operativos de una empresa.

## 🚀 Características Principales

### 📊 Módulos Implementados
- **💰 Gestión Financiera**: Contabilidad, facturación, reportes financieros
- **📦 Gestión de Inventario**: Control de stock, productos, categorías
- **🛒 Gestión de Ventas**: Clientes, cotizaciones, órdenes de venta
- **🏪 Gestión de Compras**: Proveedores, órdenes de compra, recepción
- **👥 Recursos Humanos**: Empleados, nómina, asistencia
- **📈 Dashboard Ejecutivo**: KPIs, gráficos, métricas en tiempo real

### 🏗️ Arquitectura Técnica

#### Backend (Python FastAPI)
- **Framework**: FastAPI 0.104+ (API REST moderna)
- **Base de Datos**: PostgreSQL con SQLAlchemy ORM
- **Autenticación**: JWT con refresh tokens
- **Validación**: Pydantic schemas
- **Documentación**: OpenAPI/Swagger automática
- **Testing**: Pytest con cobertura completa

#### Frontend (React TypeScript)
- **Framework**: React 18+ con TypeScript
- **UI Library**: Material-UI (MUI) + Custom Design System
- **State Management**: Redux Toolkit + RTK Query
- **Routing**: React Router v6
- **Charts**: Recharts para visualizaciones
- **Formularios**: React Hook Form + Yup validation

#### DevOps & Deployment
- **Containerización**: Docker + Docker Compose
- **Base de Datos**: PostgreSQL 15
- **Proxy**: Nginx para producción
- **Variables de Entorno**: Configuración segura

## 📁 Estructura del Proyecto

```
erp-professional/
├── backend/                 # API Backend (FastAPI)
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── core/           # Configuración y seguridad
│   │   ├── models/         # Modelos de base de datos
│   │   ├── schemas/        # Esquemas Pydantic
│   │   ├── services/       # Lógica de negocio
│   │   └── utils/          # Utilidades
│   ├── tests/              # Tests automatizados
│   └── requirements.txt    # Dependencias Python
├── frontend/               # Frontend (React TypeScript)
│   ├── src/
│   │   ├── components/     # Componentes reutilizables
│   │   ├── pages/          # Páginas principales
│   │   ├── store/          # Estado global (Redux)
│   │   ├── services/       # APIs y servicios
│   │   ├── types/          # Tipos TypeScript
│   │   └── utils/          # Utilidades
│   └── package.json        # Dependencias Node.js
├── docker-compose.yml      # Configuración Docker
└── docs/                   # Documentación adicional
```

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Docker & Docker Compose
- Node.js 18+ (para desarrollo frontend)
- Python 3.11+ (para desarrollo backend)

### Ejecución Rápida con Docker
```bash
# Clonar el repositorio
git clone <repository-url>
cd erp-professional

# Iniciar todos los servicios
docker-compose up -d

# Acceder a la aplicación
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Documentación API: http://localhost:8000/docs
```

### Desarrollo Local

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## 👤 Credenciales de Prueba

- **Usuario**: admin@erpro.com
- **Contraseña**: admin123

## 📊 Funcionalidades ERP

### 1. Dashboard Ejecutivo
- Métricas de ventas en tiempo real
- Gráficos de rendimiento financiero
- Indicadores de inventario
- Resumen de actividades recientes

### 2. Gestión de Inventario
- Catálogo completo de productos
- Control de stock por ubicación
- Alertas de stock mínimo
- Historial de movimientos

### 3. Gestión de Ventas
- CRM integrado de clientes
- Proceso de cotización → venta
- Seguimiento de órdenes
- Análisis de ventas

### 4. Gestión de Compras
- Base de datos de proveedores
- Órdenes de compra automatizadas
- Recepción y validación
- Control de costos

### 5. Contabilidad
- Plan de cuentas configurable
- Asientos contables automáticos
- Estados financieros
- Reportes fiscales

### 6. Recursos Humanos
- Gestión de empleados
- Control de asistencia
- Cálculo de nómina
- Evaluaciones de desempeño

## 🔧 Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para Python
- **PostgreSQL**: Base de datos relacional
- **JWT**: Autenticación segura
- **Pydantic**: Validación de datos
- **Pytest**: Framework de testing

### Frontend
- **React**: Biblioteca de UI componentes
- **TypeScript**: Tipado estático
- **Material-UI**: Biblioteca de componentes
- **Redux Toolkit**: Gestión de estado
- **React Router**: Enrutamiento
- **Recharts**: Gráficos y visualizaciones

## 📈 Métricas y Monitoreo

- Logs estructurados con identificadores únicos
- Métricas de performance de API
- Monitoreo de salud de base de datos
- Tracking de errores y excepciones

## 🔒 Seguridad

- Autenticación JWT con refresh tokens
- Autorización basada en roles (RBAC)
- Validación de entrada en todos los endpoints
- Cifrado de datos sensibles
- Rate limiting para APIs

## 🧪 Testing

- Cobertura de tests > 90%
- Tests unitarios para lógica de negocio
- Tests de integración para APIs
- Tests E2E para flujos críticos

## 📚 Documentación

- Documentación automática de API (Swagger/OpenAPI)
- Comentarios detallados en todo el código
- Guías de instalación y desarrollo
- Arquitectura y patrones utilizados

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para soporte técnico o consultas:
- Email: soporte@erpro.com
- Documentación: [Wiki del Proyecto](docs/)
- Issues: [GitHub Issues](issues/)

---
**ERP Professional** - Transformando la gestión empresarial con tecnología moderna 🚀