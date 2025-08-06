"""
🔧 ERP Professional - Configuración Central
==================================================

Este módulo contiene toda la configuración del sistema ERP, incluyendo:
- Variables de entorno
- Configuración de base de datos  
- Configuración de seguridad (JWT)
- Configuración de CORS
- Configuración de logs y monitoreo

Utiliza Pydantic Settings para validación automática de tipos
y carga desde variables de entorno.
"""

import os
from typing import Any, Dict, List, Optional, Union
from pydantic import (
    AnyHttpUrl,
    BaseSettings, 
    EmailStr,
    PostgresDsn,
    validator
)


class Settings(BaseSettings):
    """
    🏗️ Configuración principal del sistema ERP
    
    Esta clase maneja todas las configuraciones del sistema utilizando
    Pydantic Settings para validación automática y carga desde variables
    de entorno con valores por defecto apropiados.
    """
    
    # ================================================================
    # 🏢 INFORMACIÓN GENERAL DEL PROYECTO
    # ================================================================
    PROJECT_NAME: str = "ERP Professional"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "Sistema de Gestión Empresarial Profesional"
    
    # ================================================================
    # 🌐 CONFIGURACIÓN DEL SERVIDOR
    # ================================================================
    # URL base de la API - importante para CORS y documentación
    API_V1_STR: str = "/api/v1"
    
    # Configuración del servidor web
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Ambiente de ejecución (development, staging, production)
    ENVIRONMENT: str = "development"
    
    # ================================================================
    # 🔐 CONFIGURACIÓN DE SEGURIDAD JWT
    # ================================================================
    # Clave secreta para firmar tokens JWT - CAMBIAR EN PRODUCCIÓN
    SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production-please"
    
    # Algoritmo de encriptación para JWT
    ALGORITHM: str = "HS256"
    
    # Tiempo de expiración de tokens de acceso (en minutos)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Tiempo de expiración de tokens de refresco (en días)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # ================================================================
    # 🗄️ CONFIGURACIÓN DE BASE DE DATOS
    # ================================================================
    # URL completa de conexión a PostgreSQL
    DATABASE_URL: Optional[PostgresDsn] = None
    
    # Configuración individual de base de datos (usado si no hay DATABASE_URL)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "erp_user"
    POSTGRES_PASSWORD: str = "erp_password_2024"
    POSTGRES_DB: str = "erp_professional"
    POSTGRES_PORT: int = 5432
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """
        🔗 Construye la URL de base de datos si no está proporcionada
        
        Si DATABASE_URL no está definida, construye la URL usando los
        componentes individuales de configuración de PostgreSQL.
        """
        if isinstance(v, str):
            return v
        
        # Construir URL desde componentes individuales
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=str(values.get("POSTGRES_PORT")),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    # ================================================================
    # 🌍 CONFIGURACIÓN DE CORS
    # ================================================================
    # Dominios permitidos para CORS - importante para frontend
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # React development server
        "http://localhost:8080",  # Alternative frontend port
        "http://frontend:3000",   # Docker internal network
    ]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        🌐 Procesa los orígenes CORS
        
        Convierte string JSON en lista de URLs para configuración CORS.
        Permite tanto formato de string JSON como lista directa.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # ================================================================
    # 👤 CONFIGURACIÓN DE USUARIO ADMINISTRADOR
    # ================================================================
    # Credenciales del primer usuario administrador del sistema
    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@erpro.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    FIRST_SUPERUSER_NAME: str = "Administrador"
    
    # ================================================================
    # 📧 CONFIGURACIÓN DE EMAIL
    # ================================================================
    # Configuración del servidor SMTP para envío de emails
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Email por defecto para notificaciones del sistema
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """
        📧 Establece el nombre por defecto para emails
        """
        if not v:
            return values["PROJECT_NAME"]
        return v
    
    # ================================================================
    # 📂 CONFIGURACIÓN DE ARCHIVOS
    # ================================================================
    # Directorios para almacenamiento de archivos
    UPLOAD_FOLDER: str = "uploads"
    TEMP_FOLDER: str = "temp"
    REPORTS_FOLDER: str = "reports"
    
    # Tamaño máximo de archivo (en bytes) - 10MB por defecto
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    
    # Tipos de archivo permitidos
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/gif",
        "application/pdf",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/csv"
    ]
    
    # ================================================================
    # 🔄 CONFIGURACIÓN DE REDIS CACHE
    # ================================================================
    # URL de conexión a Redis para caché (opcional)
    REDIS_URL: Optional[str] = None
    
    # Configuración individual de Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # Tiempo de vida por defecto para caché (en segundos)
    CACHE_DEFAULT_TTL: int = 3600  # 1 hora
    
    # ================================================================
    # 📊 CONFIGURACIÓN DE LOGS Y MONITOREO
    # ================================================================
    # Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG_LEVEL: str = "INFO"
    
    # Formato de logs (json para producción, texto para desarrollo)
    LOG_FORMAT: str = "json" if ENVIRONMENT == "production" else "text"
    
    # Archivo de logs
    LOG_FILE: str = "logs/erp_backend.log"
    
    # Rotación de logs (tamaño máximo en MB)
    LOG_MAX_SIZE: int = 100
    
    # Cantidad de archivos de logs a mantener
    LOG_BACKUP_COUNT: int = 5
    
    # ================================================================
    # 🏭 CONFIGURACIÓN ESPECÍFICA DEL ERP
    # ================================================================
    # Configuración de la empresa por defecto
    DEFAULT_COMPANY_NAME: str = "Mi Empresa"
    DEFAULT_COMPANY_EMAIL: EmailStr = "contacto@miempresa.com"
    DEFAULT_COMPANY_PHONE: str = "+1234567890"
    
    # Configuración fiscal
    DEFAULT_TAX_RATE: float = 0.19  # 19% IVA por defecto
    DEFAULT_CURRENCY: str = "USD"
    DEFAULT_CURRENCY_SYMBOL: str = "$"
    
    # Configuración de inventario
    LOW_STOCK_THRESHOLD: int = 10  # Alerta de stock bajo
    ENABLE_STOCK_TRACKING: bool = True
    
    # Configuración de numeración automática
    INVOICE_PREFIX: str = "FAC"
    QUOTE_PREFIX: str = "COT"
    PURCHASE_ORDER_PREFIX: str = "OC"
    
    # ================================================================
    # 🔍 CONFIGURACIÓN DE PAGINACIÓN
    # ================================================================
    # Tamaño por defecto de página para listados
    DEFAULT_PAGE_SIZE: int = 20
    
    # Tamaño máximo de página permitido
    MAX_PAGE_SIZE: int = 100
    
    # ================================================================
    # ⚡ CONFIGURACIÓN DE RENDIMIENTO
    # ================================================================
    # Número de workers para uvicorn en producción
    WORKERS_COUNT: int = 1
    
    # Tiempo límite para requests (en segundos)
    REQUEST_TIMEOUT: int = 30
    
    # Configuración de rate limiting
    RATE_LIMIT_REQUESTS: int = 100  # requests por minuto
    RATE_LIMIT_WINDOW: int = 60     # ventana en segundos
    
    class Config:
        """
        🔧 Configuración de Pydantic
        
        Define el comportamiento del modelo de configuración:
        - case_sensitive: Distingue mayúsculas/minúsculas en variables
        - env_file: Archivo .env a cargar automáticamente
        """
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# ================================================================
# 🌟 INSTANCIA GLOBAL DE CONFIGURACIÓN
# ================================================================
# Instancia única de configuración para usar en toda la aplicación
settings = Settings()


# ================================================================
# 🔧 FUNCIONES DE UTILIDAD PARA CONFIGURACIÓN
# ================================================================

def get_database_url() -> str:
    """
    🗄️ Obtiene la URL de base de datos completa
    
    Returns:
        str: URL de conexión a PostgreSQL
    """
    return str(settings.DATABASE_URL)


def is_development() -> bool:
    """
    🚧 Verifica si estamos en ambiente de desarrollo
    
    Returns:
        bool: True si es ambiente de desarrollo
    """
    return settings.ENVIRONMENT.lower() == "development"


def is_production() -> bool:
    """
    🏭 Verifica si estamos en ambiente de producción
    
    Returns:
        bool: True si es ambiente de producción
    """
    return settings.ENVIRONMENT.lower() == "production"


def get_cors_origins() -> List[str]:
    """
    🌐 Obtiene la lista de orígenes CORS permitidos
    
    Returns:
        List[str]: Lista de URLs permitidas para CORS
    """
    return [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]


def get_upload_path(filename: str) -> str:
    """
    📁 Construye la ruta completa para un archivo subido
    
    Args:
        filename (str): Nombre del archivo
        
    Returns:
        str: Ruta completa del archivo
    """
    return os.path.join(settings.UPLOAD_FOLDER, filename)


def get_log_config() -> Dict[str, Any]:
    """
    📊 Obtiene configuración de logging
    
    Returns:
        Dict[str, Any]: Configuración para el sistema de logs
    """
    return {
        "level": settings.LOG_LEVEL,
        "format": settings.LOG_FORMAT,
        "file": settings.LOG_FILE,
        "max_size": settings.LOG_MAX_SIZE,
        "backup_count": settings.LOG_BACKUP_COUNT,
    }


# ================================================================
# 📋 VALIDACIONES ADICIONALES
# ================================================================

def validate_configuration() -> None:
    """
    ✅ Valida que la configuración sea correcta
    
    Verifica que todas las configuraciones críticas estén presentes
    y sean válidas antes de iniciar la aplicación.
    
    Raises:
        ValueError: Si alguna configuración es inválida
    """
    # Verificar que la clave secreta no sea la por defecto en producción
    if is_production() and settings.SECRET_KEY == "your-super-secret-jwt-key-change-in-production-please":
        raise ValueError(
            "🚨 PELIGRO: Debes cambiar SECRET_KEY en producción!"
        )
    
    # Verificar configuración de base de datos
    if not settings.DATABASE_URL:
        raise ValueError(
            "🗄️ ERROR: DATABASE_URL o configuración de PostgreSQL requerida"
        )
    
    # Verificar configuración de email en producción
    if is_production() and not settings.SMTP_HOST:
        raise ValueError(
            "📧 ADVERTENCIA: Configuración SMTP recomendada en producción"
        )
    
    print("✅ Configuración validada exitosamente")


# ================================================================
# 📖 INFORMACIÓN DE CONFIGURACIÓN
# ================================================================

def print_configuration_info() -> None:
    """
    📋 Imprime información de configuración actual
    
    Útil para debugging y verificación de configuración
    (sin mostrar información sensible).
    """
    print("🔧 ===== CONFIGURACIÓN ERP PROFESSIONAL =====")
    print(f"📋 Proyecto: {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    print(f"🌍 Ambiente: {settings.ENVIRONMENT}")
    print(f"🌐 Host: {settings.HOST}:{settings.PORT}")
    print(f"📂 API Base: {settings.API_V1_STR}")
    print(f"🗄️ Base de datos: PostgreSQL en {settings.POSTGRES_SERVER}")
    print(f"🔐 JWT Expira: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} min")
    print(f"📊 Log Level: {settings.LOG_LEVEL}")
    print(f"💾 Caché Redis: {'Habilitado' if settings.REDIS_URL else 'Deshabilitado'}")
    print("🔧 ==========================================")


if __name__ == "__main__":
    # Si se ejecuta directamente, mostrar configuración y validar
    validate_configuration()
    print_configuration_info()