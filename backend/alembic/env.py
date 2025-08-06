"""
🗄️ ERP Professional - Entorno de Alembic
==========================================

Este archivo configura el entorno de Alembic para las migraciones de base de datos.
Define cómo Alembic se conecta a la base de datos y genera las migraciones.

Características incluidas:
- Configuración automática desde settings de FastAPI
- Soporte para migraciones offline y online
- Configuración de metadatos con todos los modelos
- Logging estructurado para debugging
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Añadir el directorio raíz al path para importar módulos de la aplicación
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Importar configuración y modelos de la aplicación
from app.core.config import settings
from app.models.base import Base

# Importar todos los modelos para que estén disponibles en metadata
# Esto es crucial para que Alembic detecte automáticamente los cambios
from app.models import *  # noqa

# ================================================================
# 🔧 CONFIGURACIÓN DE ALEMBIC
# ================================================================

# Objeto de configuración de Alembic
config = context.config

# Configurar logging si existe archivo de configuración
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadatos de SQLAlchemy con todos los modelos
# Esto permite a Alembic detectar automáticamente cambios en los modelos
target_metadata = Base.metadata

# Esquemas adicionales a incluir en comparaciones (si se usan)
# include_schemas = True


# ================================================================
# 🌐 FUNCIONES DE MIGRACIÓN
# ================================================================

def get_url() -> str:
    """
    🔗 Obtiene la URL de conexión a la base de datos
    
    Prioriza la URL desde variables de entorno por seguridad,
    fallback a la configuración de alembic.ini
    
    Returns:
        str: URL de conexión a PostgreSQL
    """
    # Intentar obtener desde variable de entorno primero
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    
    # Fallback a configuración de settings
    return str(settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """
    🔄 Ejecuta migraciones en modo 'offline'
    
    Este modo genera scripts SQL sin conectarse realmente a la base de datos.
    Útil para generar archivos SQL que se pueden revisar antes de aplicar.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,          # Comparar tipos de columnas
        compare_server_default=True, # Comparar valores por defecto
        include_schemas=True,       # Incluir esquemas personalizados
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    🌐 Ejecuta migraciones en modo 'online'
    
    Este modo se conecta directamente a la base de datos y aplica
    las migraciones. Es el modo normal de operación.
    """
    # Configurar URL de conexión
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    # Crear engine de SQLAlchemy
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # No usar pooling en migraciones
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,          # Detectar cambios en tipos
            compare_server_default=True, # Detectar cambios en defaults
            include_schemas=True,       # Incluir múltiples esquemas
            
            # Configuración adicional para PostgreSQL
            render_as_batch=False,      # PostgreSQL soporta ALTER directo
            
            # Función personalizada para filtrar objetos a incluir
            include_object=include_object,
            
            # Función para comparar tipos personalizados
            compare_type=compare_type,
        )

        with context.begin_transaction():
            context.run_migrations()


def include_object(object, name, type_, reflected, compare_to):
    """
    🎯 Filtra qué objetos incluir en las migraciones
    
    Permite excluir ciertas tablas, índices o constraints
    de las migraciones automáticas.
    
    Args:
        object: Objeto de SQLAlchemy (tabla, índice, etc.)
        name: Nombre del objeto
        type_: Tipo de objeto ('table', 'column', 'index', etc.)
        reflected: Si el objeto viene de la base de datos
        compare_to: Objeto de comparación de metadata
        
    Returns:
        bool: True para incluir el objeto, False para excluir
    """
    # Excluir tablas temporales o de sistema
    if type_ == "table" and name.startswith("temp_"):
        return False
    
    # Excluir índices automáticos de PostgreSQL
    if type_ == "index" and name.startswith("ix_"):
        return True  # Incluir por ahora, se puede personalizar
    
    # Incluir todo por defecto
    return True


def compare_type(context, inspected_column, metadata_column, inspected_type, metadata_type):
    """
    🔍 Compara tipos de columnas para detectar cambios
    
    Función personalizada para manejar comparaciones de tipos específicas
    de PostgreSQL y evitar migraciones innecesarias.
    
    Args:
        context: Contexto de migración
        inspected_column: Columna desde la base de datos
        metadata_column: Columna desde los modelos
        inspected_type: Tipo desde la base de datos
        metadata_type: Tipo desde los modelos
        
    Returns:
        bool: True si los tipos son diferentes, False si son iguales
    """
    # Manejar UUID vs String en PostgreSQL
    if hasattr(metadata_type, 'impl'):
        if str(metadata_type.impl) == 'UUID':
            return str(inspected_type) != 'UUID'
    
    # Manejar ENUM types específicos
    if hasattr(metadata_type, 'enums'):
        if hasattr(inspected_type, 'enums'):
            return metadata_type.enums != inspected_type.enums
    
    # Usar comparación por defecto para otros tipos
    return None


# ================================================================
# 🚀 PUNTO DE ENTRADA PRINCIPAL
# ================================================================

def main():
    """
    🚀 Función principal que determina el modo de ejecución
    
    Alembic llama esta función para ejecutar migraciones.
    Detecta automáticamente si debe ejecutar en modo online u offline.
    """
    print("🗄️ Iniciando migraciones de ERP Professional...")
    
    if context.is_offline_mode():
        print("📄 Ejecutando en modo offline (generando SQL)")
        run_migrations_offline()
    else:
        print("🌐 Ejecutando en modo online (aplicando a base de datos)")
        run_migrations_online()
    
    print("✅ Migraciones completadas exitosamente")


# ================================================================
# 🔧 CONFIGURACIÓN ADICIONAL PARA DESARROLLO
# ================================================================

def get_revision_argument():
    """
    🔖 Obtiene el argumento de revisión para migraciones
    
    Útil para debugging y logs de migración.
    """
    try:
        return context.get_revision_argument()
    except:
        return "unknown"


def log_migration_info():
    """
    📊 Registra información útil sobre la migración actual
    
    Ayuda con debugging y auditoría de migraciones.
    """
    revision = get_revision_argument()
    url = get_url()
    
    print(f"🔖 Revisión: {revision}")
    print(f"🗄️ Base de datos: {url.split('@')[-1] if '@' in url else 'local'}")
    print(f"📋 Modelos cargados: {len(target_metadata.tables)} tablas")


# Ejecutar logging si estamos en modo verbose
if context.is_offline_mode() or os.getenv("ALEMBIC_VERBOSE"):
    log_migration_info()


# ================================================================
# 🏃‍♂️ EJECUTAR MIGRACIONES
# ================================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()