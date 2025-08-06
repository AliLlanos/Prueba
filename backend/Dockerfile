# 🐍 ERP Professional - Backend Dockerfile
# Imagen Docker optimizada para el backend FastAPI

# ============================================================================
# 🏗️ ETAPA 1: BUILD STAGE
# ============================================================================
FROM python:3.11-slim as builder

# Información del mantenedor
LABEL maintainer="ERP Professional Team <dev@erpro.com>"
LABEL description="Backend FastAPI para ERP Professional"
LABEL version="1.0.0"

# Variables de entorno para optimización de Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema necesarias para compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no privilegiado para mayor seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================================
# 🚀 ETAPA 2: RUNTIME STAGE
# ============================================================================
FROM python:3.11-slim

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    # FastAPI optimizations
    WORKERS=1 \
    MAX_WORKERS=10 \
    HOST=0.0.0.0 \
    PORT=8000

# Instalar solo dependencias de runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Crear usuario y grupo para la aplicación
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Crear directorios necesarios con permisos correctos
RUN mkdir -p /app/logs /app/uploads /app/temp && \
    chown -R appuser:appuser /app

# Copiar código de la aplicación
COPY --chown=appuser:appuser ./app /app/app/
COPY --chown=appuser:appuser ./alembic.ini /app/
COPY --chown=appuser:appuser ./alembic /app/alembic/

# Script de entrada personalizado
COPY --chown=appuser:appuser <<EOF /app/entrypoint.sh
#!/bin/bash
# 🚀 Script de entrada para el backend ERP

set -e

echo "🔧 Inicializando backend ERP Professional..."

# Esperar a que la base de datos esté disponible
echo "⏳ Esperando conexión a la base de datos..."
python -c "
import time
import sys
from sqlalchemy import create_engine
from app.core.config import settings

max_tries = 60
tries = 0

while tries < max_tries:
    try:
        engine = create_engine(settings.DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print('✅ Base de datos conectada exitosamente')
        break
    except Exception as e:
        tries += 1
        print(f'⏳ Intento {tries}/{max_tries}: Esperando base de datos...')
        time.sleep(1)
else:
    print('❌ No se pudo conectar a la base de datos')
    sys.exit(1)
"

# Ejecutar migraciones si es necesario
echo "🔄 Verificando migraciones de base de datos..."
alembic upgrade head

# Crear datos iniciales si es necesario
echo "📊 Inicializando datos iniciales..."
python -c "
from app.db.init_db import init_db
from app.db.session import SessionLocal

db = SessionLocal()
try:
    init_db(db)
    print('✅ Datos iniciales creados exitosamente')
except Exception as e:
    print(f'⚠️  Datos iniciales ya existen o error: {e}')
finally:
    db.close()
"

echo "🚀 Iniciando servidor FastAPI..."

# Ejecutar el comando pasado como argumentos
exec "\$@"
EOF

# Hacer el script ejecutable
RUN chmod +x /app/entrypoint.sh

# Cambiar al usuario no privilegiado
USER appuser

# Puerto que expone la aplicación
EXPOSE 8000

# Configurar el punto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================================================
# 📋 HEALTH CHECK
# ============================================================================
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ============================================================================
# 🏷️ LABELS ADICIONALES
# ============================================================================
LABEL org.opencontainers.image.title="ERP Professional Backend"
LABEL org.opencontainers.image.description="FastAPI backend para sistema ERP"
LABEL org.opencontainers.image.vendor="ERP Professional"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.url="https://github.com/erp-professional/backend"
LABEL org.opencontainers.image.documentation="https://docs.erpro.com"
LABEL org.opencontainers.image.source="https://github.com/erp-professional/backend"

# ============================================================================
# 📝 INSTRUCCIONES DE USO
# ============================================================================
# Build:
#   docker build -t erp-backend .
#
# Run:
#   docker run -p 8000:8000 -e DATABASE_URL=postgresql://... erp-backend
#
# Development:
#   docker run -v $(pwd):/app -p 8000:8000 erp-backend
#
# Production:
#   docker run --restart=unless-stopped -d -p 8000:8000 erp-backend