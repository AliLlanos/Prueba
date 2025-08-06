# ⚛️ ERP Professional - Frontend Dockerfile
# Imagen Docker optimizada para la aplicación React TypeScript

# ============================================================================
# 🏗️ ETAPA 1: BUILD STAGE
# ============================================================================
FROM node:18-alpine as builder

# Información del mantenedor
LABEL maintainer="ERP Professional Team <dev@erpro.com>"
LABEL description="Frontend React TypeScript para ERP Professional"
LABEL version="1.0.0"

# Variables de entorno para optimización de Node.js
ENV NODE_ENV=production \
    NPM_CONFIG_LOGLEVEL=warn \
    NPM_CONFIG_PROGRESS=false

# Instalar dependencias del sistema para Node.js
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    && rm -rf /var/cache/apk/*

# Crear usuario no privilegiado
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración de dependencias
COPY package*.json ./
COPY tsconfig.json ./

# Instalar dependencias
RUN npm ci --only=production --silent && \
    npm cache clean --force

# Copiar código fuente
COPY src/ ./src/
COPY public/ ./public/

# Configurar ownership de archivos
RUN chown -R nextjs:nodejs /app

# Cambiar a usuario no privilegiado para build
USER nextjs

# Construir la aplicación para producción
RUN npm run build

# ============================================================================
# 🚀 ETAPA 2: RUNTIME STAGE - NGINX
# ============================================================================
FROM nginx:alpine

# Variables de entorno
ENV NODE_ENV=production

# Instalar dependencias adicionales
RUN apk add --no-cache \
    curl \
    && rm -rf /var/cache/apk/*

# Copiar build desde etapa anterior
COPY --from=builder /app/build /usr/share/nginx/html

# Configuración personalizada de Nginx
COPY <<EOF /etc/nginx/conf.d/default.conf
# 🌐 Configuración Nginx para ERP Professional Frontend

server {
    listen 80;
    server_name localhost;
    
    # Configuración de compresión
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Configuración de archivos estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files \$uri =404;
    }

    # Configuración para React Router (SPA)
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files \$uri \$uri/ /index.html;
        
        # Headers de seguridad
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    }

    # Configuración para API proxy (desarrollo)
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Configuración de logs
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
}
EOF

# Crear directorio para logs con permisos correctos
RUN mkdir -p /var/log/nginx && \
    touch /var/log/nginx/access.log /var/log/nginx/error.log && \
    chown -R nginx:nginx /var/log/nginx

# Puerto que expone la aplicación
EXPOSE 80

# Health check para Docker
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]

# ============================================================================
# 🏷️ LABELS ADICIONALES
# ============================================================================
LABEL org.opencontainers.image.title="ERP Professional Frontend"
LABEL org.opencontainers.image.description="React TypeScript frontend para sistema ERP"
LABEL org.opencontainers.image.vendor="ERP Professional"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.url="https://github.com/erp-professional/frontend"
LABEL org.opencontainers.image.documentation="https://docs.erpro.com"
LABEL org.opencontainers.image.source="https://github.com/erp-professional/frontend"

# ============================================================================
# 📝 INSTRUCCIONES DE USO
# ============================================================================
# Build:
#   docker build -t erp-frontend .
#
# Run:
#   docker run -p 3000:80 erp-frontend
#
# Development:
#   docker run -v $(pwd)/src:/app/src -p 3000:80 erp-frontend
#
# Production:
#   docker run --restart=unless-stopped -d -p 80:80 erp-frontend