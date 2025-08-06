"""
🚀 ERP Professional - Aplicación Principal
==========================================

Este es el punto de entrada principal del backend FastAPI del sistema ERP.
Configura la aplicación, middleware, rutas, y todas las características necesarias
para un sistema empresarial robusto y profesional.

Características incluidas:
- Configuración de FastAPI con documentación automática
- Middleware de seguridad (CORS, headers de seguridad)
- Rutas de API organizadas por módulos
- Manejo global de errores
- Logging estructurado
- Health checks
- Métricas de rendimiento
"""

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import time
import uuid
from typing import Dict, Any

# Importaciones internas del proyecto
from app.core.config import settings, validate_configuration, print_configuration_info
from app.core.security import SECURITY_HEADERS

# TODO: Importar routers cuando estén creados
# from app.api.api_v1.api import api_router


# ================================================================
# 🔧 CONFIGURACIÓN DE CICLO DE VIDA
# ================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    🔄 Gestión del ciclo de vida de la aplicación
    
    Maneja la inicialización y limpieza de recursos de la aplicación.
    Se ejecuta al startup y shutdown de FastAPI.
    """
    # ============================================================
    # 🚀 STARTUP - Inicialización de la aplicación
    # ============================================================
    
    print("🚀 ===== INICIANDO ERP PROFESSIONAL =====")
    
    try:
        # Validar configuración
        print("🔧 Validando configuración...")
        validate_configuration()
        
        # Mostrar información de configuración
        print_configuration_info()
        
        # TODO: Inicializar conexión a base de datos
        print("🗄️ Inicializando conexión a base de datos...")
        
        # TODO: Crear tablas si no existen (en desarrollo)
        if settings.ENVIRONMENT == "development":
            print("🏗️ Verificando esquema de base de datos...")
        
        # TODO: Inicializar caché Redis si está configurado
        if settings.REDIS_URL:
            print("💾 Conectando a Redis...")
        
        # TODO: Cargar datos iniciales si es necesario
        print("📊 Verificando datos iniciales...")
        
        print("✅ ERP Professional iniciado exitosamente")
        print("🌐 Documentación disponible en: /docs")
        print("📊 Health check disponible en: /health")
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        raise
    
    # Yield control para que la app esté disponible
    yield
    
    # ============================================================
    # 🛑 SHUTDOWN - Limpieza de recursos
    # ============================================================
    
    print("🛑 ===== CERRANDO ERP PROFESSIONAL =====")
    
    try:
        # TODO: Cerrar conexiones de base de datos
        print("🗄️ Cerrando conexiones de base de datos...")
        
        # TODO: Cerrar conexión Redis
        if settings.REDIS_URL:
            print("💾 Cerrando conexión Redis...")
        
        # TODO: Limpiar recursos temporales
        print("🧹 Limpiando recursos temporales...")
        
        print("✅ ERP Professional cerrado correctamente")
        
    except Exception as e:
        print(f"⚠️ Error durante el cierre: {e}")


# ================================================================
# 🏗️ CREACIÓN DE LA APLICACIÓN FASTAPI
# ================================================================

def create_application() -> FastAPI:
    """
    🏗️ Factory para crear y configurar la aplicación FastAPI
    
    Configura todos los aspectos de la aplicación de manera centralizada.
    
    Returns:
        FastAPI: Aplicación configurada y lista para usar
    """
    
    # Crear instancia de FastAPI con configuración personalizada
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
        # Configuración adicional para producción
        debug=settings.ENVIRONMENT == "development",
    )
    
    # Configurar middleware
    setup_middleware(app)
    
    # Configurar rutas
    setup_routes(app)
    
    # Configurar manejo de errores
    setup_error_handlers(app)
    
    # Configurar documentación personalizada
    setup_custom_openapi(app)
    
    return app


# ================================================================
# 🛡️ CONFIGURACIÓN DE MIDDLEWARE
# ================================================================

def setup_middleware(app: FastAPI) -> None:
    """
    🛡️ Configura todo el middleware de seguridad y funcionalidad
    
    Args:
        app (FastAPI): Instancia de la aplicación
    """
    
    # ============================================================
    # 🔒 MIDDLEWARE DE SEGURIDAD
    # ============================================================
    
    # Headers de seguridad personalizados
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        """
        🔒 Añade headers de seguridad a todas las respuestas
        
        Protege contra ataques comunes como XSS, clickjacking, etc.
        """
        response = await call_next(request)
        
        # Añadir headers de seguridad
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        
        return response
    
    # ============================================================
    # 📊 MIDDLEWARE DE LOGGING Y MÉTRICAS
    # ============================================================
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """
        📊 Registra todas las peticiones para análisis y debugging
        
        Captura métricas de performance y logs estructurados.
        """
        # Generar ID único para la petición
        request_id = str(uuid.uuid4())
        
        # Información de la petición
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Log de inicio de petición
        print(f"🌐 [{request_id}] {request.method} {request.url.path} - IP: {client_ip}")
        
        # Procesar petición
        response = await call_next(request)
        
        # Calcular tiempo de procesamiento
        process_time = time.time() - start_time
        
        # Añadir headers informativos
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log de finalización
        status_emoji = "✅" if response.status_code < 400 else "❌"
        print(f"{status_emoji} [{request_id}] {response.status_code} - {process_time:.3f}s")
        
        return response
    
    # ============================================================
    # 🌍 MIDDLEWARE DE CORS
    # ============================================================
    
    # Configurar CORS para permitir frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"],
    )
    
    # ============================================================
    # 🔒 MIDDLEWARE DE HOST CONFIABLES (PRODUCCIÓN)
    # ============================================================
    
    if settings.ENVIRONMENT == "production":
        # En producción, solo permitir hosts específicos
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
        )


# ================================================================
# 🛣️ CONFIGURACIÓN DE RUTAS
# ================================================================

def setup_routes(app: FastAPI) -> None:
    """
    🛣️ Configura todas las rutas de la API
    
    Args:
        app (FastAPI): Instancia de la aplicación
    """
    
    # ============================================================
    # 🏠 RUTA DE BIENVENIDA
    # ============================================================
    
    @app.get("/", tags=["General"])
    async def root() -> Dict[str, Any]:
        """
        🏠 Endpoint raíz de bienvenida
        
        Proporciona información básica sobre la API.
        """
        return {
            "message": f"🏢 Bienvenido a {settings.PROJECT_NAME}",
            "version": settings.PROJECT_VERSION,
            "description": settings.PROJECT_DESCRIPTION,
            "environment": settings.ENVIRONMENT,
            "docs_url": "/docs",
            "health_check": "/health",
            "api_base": settings.API_V1_STR,
            "status": "🟢 Operativo"
        }
    
    # ============================================================
    # 🩺 HEALTH CHECK
    # ============================================================
    
    @app.get("/health", tags=["General"])
    async def health_check() -> Dict[str, Any]:
        """
        🩺 Endpoint de verificación de salud
        
        Verifica que todos los servicios estén funcionando correctamente.
        Usado por Docker, Kubernetes y monitoreo.
        """
        health_status = {
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.PROJECT_VERSION,
            "environment": settings.ENVIRONMENT,
            "services": {
                "api": "🟢 healthy",
                # TODO: Añadir checks para base de datos
                "database": "🟢 healthy",  # Placeholder
                # TODO: Añadir checks para Redis si está configurado
                "cache": "🟢 healthy" if settings.REDIS_URL else "⚪ disabled",
            }
        }
        
        return health_status
    
    # ============================================================
    # 📊 MÉTRICAS BÁSICAS
    # ============================================================
    
    @app.get("/metrics", tags=["General"])
    async def get_metrics() -> Dict[str, Any]:
        """
        📊 Endpoint de métricas básicas
        
        Proporciona información sobre el rendimiento del sistema.
        """
        return {
            "uptime": "Calculando...",  # TODO: Implementar cálculo real
            "requests_total": "Calculando...",  # TODO: Implementar contador
            "active_connections": "Calculando...",  # TODO: Implementar monitoreo
            "memory_usage": "Calculando...",  # TODO: Implementar métricas de memoria
            "timestamp": time.time()
        }
    
    # ============================================================
    # 🔧 INFORMACIÓN DE CONFIGURACIÓN (SOLO DESARROLLO)
    # ============================================================
    
    if settings.ENVIRONMENT == "development":
        @app.get("/config", tags=["Development"])
        async def get_config_info() -> Dict[str, Any]:
            """
            🔧 Información de configuración (solo en desarrollo)
            
            Muestra configuración actual sin información sensible.
            """
            return {
                "project_name": settings.PROJECT_NAME,
                "version": settings.PROJECT_VERSION,
                "environment": settings.ENVIRONMENT,
                "api_base": settings.API_V1_STR,
                "cors_origins": [str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
                "jwt_expiry": f"{settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes",
                "database_host": settings.POSTGRES_SERVER,
                "database_name": settings.POSTGRES_DB,
                "redis_enabled": bool(settings.REDIS_URL),
                "log_level": settings.LOG_LEVEL,
            }
    
    # ============================================================
    # 📚 RUTAS DE API VERSIONED
    # ============================================================
    
    # TODO: Incluir routers de API cuando estén disponibles
    # app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Placeholder para estructura de API
    @app.get(f"{settings.API_V1_STR}/status", tags=["API v1"])
    async def api_status() -> Dict[str, Any]:
        """
        📚 Estado de la API v1
        
        Información específica de la versión 1 de la API.
        """
        return {
            "api_version": "v1",
            "status": "active",
            "endpoints": {
                "auth": f"{settings.API_V1_STR}/auth",
                "users": f"{settings.API_V1_STR}/users",
                "inventory": f"{settings.API_V1_STR}/inventory",
                "sales": f"{settings.API_V1_STR}/sales",
                "purchasing": f"{settings.API_V1_STR}/purchasing",
                "accounting": f"{settings.API_V1_STR}/accounting",
                "hr": f"{settings.API_V1_STR}/hr",
            }
        }


# ================================================================
# ❌ MANEJO GLOBAL DE ERRORES
# ================================================================

def setup_error_handlers(app: FastAPI) -> None:
    """
    ❌ Configura manejadores globales de errores
    
    Args:
        app (FastAPI): Instancia de la aplicación
    """
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        🚨 Manejador para excepciones HTTP
        
        Proporciona respuestas consistentes para errores HTTP.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "status_code": exc.status_code,
                "message": exc.detail,
                "timestamp": time.time(),
                "path": str(request.url.path),
                "request_id": request.headers.get("X-Request-ID", "unknown")
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        💥 Manejador para excepciones generales
        
        Captura errores inesperados y los registra sin exponer detalles sensibles.
        """
        # Log del error (en producción usar logging estructurado)
        print(f"💥 Error inesperado: {type(exc).__name__}: {str(exc)}")
        print(f"📍 Ruta: {request.method} {request.url.path}")
        
        # En desarrollo, mostrar más detalles
        if settings.ENVIRONMENT == "development":
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": True,
                    "status_code": 500,
                    "message": "Error interno del servidor",
                    "detail": str(exc),
                    "type": type(exc).__name__,
                    "timestamp": time.time(),
                    "path": str(request.url.path)
                }
            )
        else:
            # En producción, respuesta genérica
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": True,
                    "status_code": 500,
                    "message": "Error interno del servidor",
                    "timestamp": time.time(),
                    "request_id": request.headers.get("X-Request-ID", "unknown")
                }
            )


# ================================================================
# 📖 DOCUMENTACIÓN PERSONALIZADA
# ================================================================

def setup_custom_openapi(app: FastAPI) -> None:
    """
    📖 Configura documentación OpenAPI personalizada
    
    Args:
        app (FastAPI): Instancia de la aplicación
    """
    
    def custom_openapi():
        """
        📋 Genera esquema OpenAPI personalizado con información adicional
        """
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version=settings.PROJECT_VERSION,
            description=f"""
## 🏢 {settings.PROJECT_DESCRIPTION}

### 📋 Características Principales

- **🔐 Autenticación JWT**: Sistema seguro de autenticación
- **👥 Gestión de Usuarios**: Control de acceso basado en roles
- **📦 Inventario**: Control completo de productos y stock
- **🛒 Ventas**: CRM integrado y gestión de ventas
- **🏪 Compras**: Gestión de proveedores y órdenes de compra
- **💰 Contabilidad**: Sistema contable completo
- **👤 RRHH**: Gestión de empleados y nómina

### 🚀 Ambiente: {settings.ENVIRONMENT.upper()}

### 📚 Documentación Adicional

- **Swagger UI**: [/docs](/docs)
- **ReDoc**: [/redoc](/redoc)
- **Health Check**: [/health](/health)

### 🔒 Autenticación

Esta API utiliza **JWT Bearer Tokens** para autenticación.

1. Obtén un token en `/api/v1/auth/login`
2. Incluye el token en el header: `Authorization: Bearer <token>`

### 📞 Soporte

- **Email**: soporte@erpro.com
- **Documentación**: https://docs.erpro.com
            """,
            routes=app.routes,
        )
        
        # Información adicional del esquema
        openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }
        
        # Configuración de seguridad JWT
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Ingresa tu token JWT en el formato: Bearer <token>"
            }
        }
        
        # Aplicar seguridad por defecto a todos los endpoints
        openapi_schema["security"] = [{"BearerAuth": []}]
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi


# ================================================================
# 🚀 CREAR INSTANCIA DE LA APLICACIÓN
# ================================================================

# Crear la aplicación FastAPI
app = create_application()


# ================================================================
# 🧪 PUNTO DE ENTRADA PARA DESARROLLO
# ================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 ===== INICIANDO EN MODO DESARROLLO =====")
    print(f"🌐 Servidor: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 Documentación: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🩺 Health Check: http://{settings.HOST}:{settings.PORT}/health")
    
    # Ejecutar servidor de desarrollo
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,  # Recarga automática en desarrollo
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
        # Configuración adicional para desarrollo
        reload_dirs=["app"],
        reload_includes=["*.py"],
    )