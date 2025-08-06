#!/bin/bash

# 🚀 ERP Professional - Script de Inicio Rápido
# ==============================================
# 
# Este script inicia toda la aplicación ERP de manera fácil y rápida.
# Incluye verificaciones de dependencias, configuración automática y
# inicio de todos los servicios necesarios.

set -e  # Salir si algún comando falla

# ================================================================
# 🎨 COLORES PARA OUTPUT
# ================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ================================================================
# 📋 FUNCIONES UTILITARIAS
# ================================================================

print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🏢 ERP PROFESSIONAL                       ║"
    echo "║              Sistema de Gestión Empresarial                 ║"
    echo "║                        v1.0.0                               ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${CYAN}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

print_info() {
    echo -e "${PURPLE}ℹ️  $1${NC}"
}

# ================================================================
# 🔍 VERIFICACIÓN DE DEPENDENCIAS
# ================================================================

check_dependencies() {
    print_step "Verificando dependencias..."
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado. Por favor instálalo desde https://docs.docker.com/get-docker/"
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado. Por favor instálalo desde https://docs.docker.com/compose/install/"
    fi
    
    # Verificar que Docker esté ejecutándose
    if ! docker info &> /dev/null; then
        print_error "Docker no está ejecutándose. Por favor inicia Docker y vuelve a intentar."
    fi
    
    print_success "Todas las dependencias están disponibles"
}

# ================================================================
# 🔧 CONFIGURACIÓN INICIAL
# ================================================================

setup_environment() {
    print_step "Configurando entorno..."
    
    # Crear archivo .env si no existe
    if [ ! -f .env ]; then
        print_info "Creando archivo .env con configuración por defecto..."
        cat > .env << EOF
# 🏢 ERP Professional - Variables de Entorno
# ==========================================

# 🌍 Configuración General
ENVIRONMENT=development
PROJECT_NAME=ERP Professional
PROJECT_VERSION=1.0.0

# 🗄️ Base de Datos PostgreSQL
DATABASE_URL=postgresql://erp_user:erp_password_2024@postgres:5432/erp_professional
POSTGRES_SERVER=postgres
POSTGRES_USER=erp_user
POSTGRES_PASSWORD=erp_password_2024
POSTGRES_DB=erp_professional
POSTGRES_PORT=5432

# 🔐 Seguridad JWT
SECRET_KEY=your-super-secret-jwt-key-change-in-production-please
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# 🌐 CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://frontend:3000"]

# 👤 Usuario Administrador Inicial
FIRST_SUPERUSER_EMAIL=admin@erpro.com
FIRST_SUPERUSER_PASSWORD=admin123
FIRST_SUPERUSER_NAME=Administrador

# 🔄 Redis Cache (Opcional)
REDIS_URL=redis://redis:6379
REDIS_PASSWORD=redis_password_2024

# 📊 Logging
LOG_LEVEL=INFO

# ⚛️ Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
REACT_APP_VERSION=1.0.0
EOF
        print_success "Archivo .env creado"
    else
        print_info "Archivo .env ya existe"
    fi
    
    # Crear directorios necesarios
    print_info "Creando directorios necesarios..."
    mkdir -p logs uploads temp reports
    
    print_success "Entorno configurado correctamente"
}

# ================================================================
# 🏗️ CONSTRUCCIÓN DE IMÁGENES
# ================================================================

build_images() {
    print_step "Construyendo imágenes Docker..."
    
    # Construir imágenes sin cache para asegurar última versión
    docker-compose build --no-cache
    
    print_success "Imágenes construidas exitosamente"
}

# ================================================================
# 🗄️ INICIALIZACIÓN DE BASE DE DATOS
# ================================================================

init_database() {
    print_step "Inicializando base de datos..."
    
    # Iniciar solo PostgreSQL primero
    docker-compose up -d postgres
    
    # Esperar a que PostgreSQL esté listo
    print_info "Esperando a que PostgreSQL esté listo..."
    sleep 10
    
    # Verificar conexión a PostgreSQL
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose exec -T postgres pg_isready -U erp_user -d erp_professional &> /dev/null; then
            print_success "PostgreSQL está listo"
            break
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            print_error "No se pudo conectar a PostgreSQL después de $max_attempts intentos"
        fi
        
        print_info "Intento $attempt/$max_attempts - Esperando PostgreSQL..."
        sleep 2
        ((attempt++))
    done
    
    print_success "Base de datos inicializada"
}

# ================================================================
# 🚀 INICIO DE SERVICIOS
# ================================================================

start_services() {
    print_step "Iniciando todos los servicios..."
    
    # Iniciar todos los servicios
    docker-compose up -d
    
    # Esperar a que todos los servicios estén listos
    print_info "Esperando a que todos los servicios estén listos..."
    sleep 15
    
    print_success "Todos los servicios iniciados"
}

# ================================================================
# 📊 VERIFICACIÓN DE SALUD
# ================================================================

health_check() {
    print_step "Verificando salud de los servicios..."
    
    # Verificar backend
    backend_healthy=false
    for i in {1..10}; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            backend_healthy=true
            break
        fi
        sleep 2
    done
    
    if [ "$backend_healthy" = true ]; then
        print_success "Backend (FastAPI) está funcionando"
    else
        print_warning "Backend tardando en iniciar - verifica logs con: docker-compose logs backend"
    fi
    
    # Verificar frontend
    frontend_healthy=false
    for i in {1..10}; do
        if curl -f http://localhost:3000 &> /dev/null; then
            frontend_healthy=true
            break
        fi
        sleep 2
    done
    
    if [ "$frontend_healthy" = true ]; then
        print_success "Frontend (React) está funcionando"
    else
        print_warning "Frontend tardando en iniciar - verifica logs con: docker-compose logs frontend"
    fi
    
    # Verificar base de datos
    if docker-compose exec -T postgres pg_isready -U erp_user -d erp_professional &> /dev/null; then
        print_success "Base de datos (PostgreSQL) está funcionando"
    else
        print_warning "Problema con base de datos - verifica logs con: docker-compose logs postgres"
    fi
}

# ================================================================
# 📋 INFORMACIÓN FINAL
# ================================================================

show_info() {
    echo ""
    echo -e "${GREEN}🎉 ¡ERP Professional iniciado exitosamente!${NC}"
    echo ""
    echo -e "${BLUE}📍 Accesos a la aplicación:${NC}"
    echo -e "   🌐 Frontend (React):     ${CYAN}http://localhost:3000${NC}"
    echo -e "   🔧 Backend API:          ${CYAN}http://localhost:8000${NC}"
    echo -e "   📚 Documentación API:    ${CYAN}http://localhost:8000/docs${NC}"
    echo -e "   🗄️ Adminer (Base datos): ${CYAN}http://localhost:8080${NC}"
    echo ""
    echo -e "${PURPLE}👤 Credenciales de acceso:${NC}"
    echo -e "   📧 Email:    ${YELLOW}admin@erpro.com${NC}"
    echo -e "   🔑 Password: ${YELLOW}admin123${NC}"
    echo ""
    echo -e "${BLUE}🛠️ Comandos útiles:${NC}"
    echo -e "   Ver logs:           ${CYAN}docker-compose logs -f${NC}"
    echo -e "   Parar servicios:    ${CYAN}docker-compose down${NC}"
    echo -e "   Reiniciar:          ${CYAN}docker-compose restart${NC}"
    echo -e "   Estado servicios:   ${CYAN}docker-compose ps${NC}"
    echo ""
    echo -e "${GREEN}✨ ¡Disfruta usando ERP Professional!${NC}"
    echo ""
}

# ================================================================
# 🔧 MANEJO DE ARGUMENTOS
# ================================================================

show_help() {
    echo "🏢 ERP Professional - Script de Inicio"
    echo ""
    echo "Uso: $0 [opción]"
    echo ""
    echo "Opciones:"
    echo "  start     Iniciar ERP completo (opción por defecto)"
    echo "  stop      Parar todos los servicios"
    echo "  restart   Reiniciar todos los servicios"
    echo "  logs      Mostrar logs en tiempo real"
    echo "  status    Mostrar estado de servicios"
    echo "  clean     Limpiar volúmenes y containers"
    echo "  help      Mostrar esta ayuda"
    echo ""
}

# ================================================================
# 🚀 FUNCIÓN PRINCIPAL
# ================================================================

main() {
    local command=${1:-start}
    
    case $command in
        start)
            print_banner
            check_dependencies
            setup_environment
            build_images
            init_database
            start_services
            health_check
            show_info
            ;;
        stop)
            print_step "Parando todos los servicios..."
            docker-compose down
            print_success "Servicios parados"
            ;;
        restart)
            print_step "Reiniciando servicios..."
            docker-compose restart
            print_success "Servicios reiniciados"
            ;;
        logs)
            print_info "Mostrando logs en tiempo real (Ctrl+C para salir)..."
            docker-compose logs -f
            ;;
        status)
            print_step "Estado de los servicios:"
            docker-compose ps
            ;;
        clean)
            print_warning "⚠️  Esto eliminará todos los containers y volúmenes"
            read -p "¿Estás seguro? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_step "Limpiando containers y volúmenes..."
                docker-compose down -v --remove-orphans
                docker system prune -f
                print_success "Limpieza completada"
            else
                print_info "Operación cancelada"
            fi
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Comando desconocido: $command. Usa '$0 help' para ver opciones disponibles."
            ;;
    esac
}

# ================================================================
# 🎯 PUNTO DE ENTRADA
# ================================================================

main "$@"