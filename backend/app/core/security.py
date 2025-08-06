"""
🔐 ERP Professional - Módulo de Seguridad
===========================================

Este módulo maneja todos los aspectos de seguridad del sistema ERP:
- Autenticación JWT (JSON Web Tokens)
- Hash y verificación de contraseñas con bcrypt
- Generación de tokens de acceso y refresco
- Validación de tokens y obtención de usuarios actuales
- Middleware de seguridad para proteger endpoints

Utiliza las mejores prácticas de seguridad para aplicaciones empresariales.
"""

from datetime import datetime, timedelta
from typing import Any, Union, Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings


# ================================================================
# 🔒 CONFIGURACIÓN DE SEGURIDAD
# ================================================================

# Contexto de bcrypt para hash de contraseñas
# Bcrypt es altamente recomendado para hash de contraseñas por su resistencia
# a ataques de fuerza bruta y rainbow tables
password_context = CryptContext(
    schemes=["bcrypt"],  # Algoritmo de hashing
    deprecated="auto",   # Manejo automático de esquemas deprecados
    bcrypt__rounds=12    # Número de rondas (balance seguridad/performance)
)

# Bearer token security scheme para FastAPI
# Extrae automáticamente el token JWT del header Authorization
security = HTTPBearer()


# ================================================================
# 🔑 FUNCIONES DE HASH DE CONTRASEÑAS
# ================================================================

def create_password_hash(password: str) -> str:
    """
    🔐 Genera hash seguro de una contraseña
    
    Utiliza bcrypt con salt automático y múltiples rondas para crear
    un hash seguro de la contraseña que puede almacenarse en la base de datos.
    
    Args:
        password (str): Contraseña en texto plano
        
    Returns:
        str: Hash bcrypt de la contraseña
        
    Example:
        >>> hash_pwd = create_password_hash("mi_contraseña_segura")
        >>> print(hash_pwd)
        $2b$12$abcdef...
    """
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    ✅ Verifica si una contraseña coincide con su hash
    
    Compara una contraseña en texto plano con su hash almacenado
    utilizando bcrypt para determinar si coinciden.
    
    Args:
        plain_password (str): Contraseña en texto plano
        hashed_password (str): Hash almacenado en la base de datos
        
    Returns:
        bool: True si la contraseña es correcta, False si no
        
    Example:
        >>> is_valid = verify_password("contraseña123", stored_hash)
        >>> print(is_valid)  # True o False
    """
    return password_context.verify(plain_password, hashed_password)


# ================================================================
# 🎫 FUNCIONES DE TOKENS JWT
# ================================================================

def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    🎫 Crea un token JWT de acceso
    
    Genera un token JWT firmado que contiene información del usuario
    y tiempo de expiración. Este token se usa para autenticar requests.
    
    Args:
        subject (Union[str, Any]): Identificador del usuario (email, ID, etc.)
        expires_delta (Optional[timedelta]): Tiempo de expiración personalizado
        
    Returns:
        str: Token JWT firmado
        
    Example:
        >>> token = create_access_token(subject="usuario@empresa.com")
        >>> print(token)
        eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
    """
    # Determinar tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Payload del token con información del usuario y expiración
    to_encode = {
        "exp": expire,          # Tiempo de expiración (estándar JWT)
        "sub": str(subject),    # Sujeto del token (usuario)
        "type": "access",       # Tipo de token para validación
        "iat": datetime.utcnow()  # Tiempo de emisión
    }
    
    # Firmar el token con la clave secreta
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    🔄 Crea un token JWT de refresco
    
    Genera un token de larga duración usado para obtener nuevos tokens
    de acceso sin requerir credenciales nuevamente.
    
    Args:
        subject (Union[str, Any]): Identificador del usuario
        expires_delta (Optional[timedelta]): Tiempo de expiración personalizado
        
    Returns:
        str: Token de refresco JWT firmado
    """
    # Determinar tiempo de expiración (más largo que access token)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    # Payload del token de refresco
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",      # Diferenciamos del access token
        "iat": datetime.utcnow()
    }
    
    # Firmar el token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """
    🔍 Verifica y decodifica un token JWT
    
    Valida la firma del token, verifica que no haya expirado y
    extrae el identificador del usuario.
    
    Args:
        token (str): Token JWT a verificar
        token_type (str): Tipo de token esperado ("access" o "refresh")
        
    Returns:
        Optional[str]: Identificador del usuario si el token es válido, None si no
        
    Raises:
        HTTPException: Si el token es inválido o ha expirado
    """
    try:
        # Decodificar el token usando la clave secreta
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Extraer el identificador del usuario
        user_id: str = payload.get("sub")
        token_type_claim: str = payload.get("type")
        
        # Validar que el token contenga el usuario y sea del tipo correcto
        if user_id is None or token_type_claim != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return user_id
        
    except JWTError:
        # Token malformado, expirado o firma inválida
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


def decode_token_payload(token: str) -> dict:
    """
    📋 Decodifica un token JWT y retorna su payload completo
    
    Útil para obtener información adicional del token como tiempo
    de expiración, tipo, etc.
    
    Args:
        token (str): Token JWT a decodificar
        
    Returns:
        dict: Payload completo del token
        
    Raises:
        HTTPException: Si el token es inválido
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ================================================================
# 🛡️ FUNCIONES DE VALIDACIÓN DE TOKENS
# ================================================================

def validate_access_token(token: str) -> str:
    """
    🎫 Valida específicamente un token de acceso
    
    Wrapper especializado para validar tokens de acceso y extraer
    el identificador del usuario.
    
    Args:
        token (str): Token de acceso JWT
        
    Returns:
        str: Identificador del usuario
        
    Raises:
        HTTPException: Si el token no es válido
    """
    return verify_token(token, token_type="access")


def validate_refresh_token(token: str) -> str:
    """
    🔄 Valida específicamente un token de refresco
    
    Wrapper especializado para validar tokens de refresco y extraer
    el identificador del usuario.
    
    Args:
        token (str): Token de refresco JWT
        
    Returns:
        str: Identificador del usuario
        
    Raises:
        HTTPException: Si el token no es válido
    """
    return verify_token(token, token_type="refresh")


# ================================================================
# 🔧 FUNCIONES AUXILIARES DE SEGURIDAD
# ================================================================

def extract_token_from_credentials(
    credentials: HTTPAuthorizationCredentials
) -> str:
    """
    🎫 Extrae el token JWT de las credenciales HTTP Bearer
    
    Procesa las credenciales HTTP Authorization para extraer
    el token JWT limpio.
    
    Args:
        credentials (HTTPAuthorizationCredentials): Credenciales HTTP Bearer
        
    Returns:
        str: Token JWT extraído
        
    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    if not credentials or credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales Bearer requeridas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials


def is_token_expired(token: str) -> bool:
    """
    ⏰ Verifica si un token JWT ha expirado
    
    Útil para verificaciones adicionales sin lanzar excepciones.
    
    Args:
        token (str): Token JWT a verificar
        
    Returns:
        bool: True si el token ha expirado, False si aún es válido
    """
    try:
        payload = decode_token_payload(token)
        exp_timestamp = payload.get("exp")
        
        if not exp_timestamp:
            return True  # Sin expiración = consideramos expirado
            
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        return datetime.utcnow() > exp_datetime
        
    except HTTPException:
        return True  # Token inválido = consideramos expirado


def get_token_remaining_time(token: str) -> timedelta:
    """
    ⏱️ Obtiene el tiempo restante antes de que expire un token
    
    Calcula cuánto tiempo queda antes de que el token expire.
    
    Args:
        token (str): Token JWT
        
    Returns:
        timedelta: Tiempo restante (puede ser negativo si expiró)
        
    Raises:
        HTTPException: Si el token es inválido
    """
    payload = decode_token_payload(token)
    exp_timestamp = payload.get("exp")
    
    if not exp_timestamp:
        return timedelta(0)  # Sin expiración
        
    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    return exp_datetime - datetime.utcnow()


# ================================================================
# 🔐 FUNCIONES DE GENERACIÓN DE CREDENCIALES
# ================================================================

def generate_secure_token_pair(user_identifier: str) -> dict:
    """
    🎭 Genera un par de tokens (acceso + refresco) para un usuario
    
    Crea tanto un token de acceso como uno de refresco para autenticación
    completa del usuario.
    
    Args:
        user_identifier (str): Identificador único del usuario
        
    Returns:
        dict: Diccionario con access_token, refresh_token, token_type y expires_in
        
    Example:
        >>> tokens = generate_secure_token_pair("usuario@empresa.com")
        >>> print(tokens)
        {
            "access_token": "eyJ0eXAiOiJKV1Q...",
            "refresh_token": "eyJ0eXAiOiJKV1Q...",
            "token_type": "bearer",
            "expires_in": 1800
        }
    """
    # Crear token de acceso
    access_token = create_access_token(subject=user_identifier)
    
    # Crear token de refresco
    refresh_token = create_refresh_token(subject=user_identifier)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # en segundos
    }


# ================================================================
# 🧪 FUNCIONES DE TESTING Y DESARROLLO
# ================================================================

def create_test_token(user_identifier: str, expires_minutes: int = 60) -> str:
    """
    🧪 Crea un token de prueba con expiración extendida
    
    Útil para testing y desarrollo. NO usar en producción.
    
    Args:
        user_identifier (str): Identificador del usuario de prueba
        expires_minutes (int): Minutos hasta expiración
        
    Returns:
        str: Token JWT de prueba
    """
    expires_delta = timedelta(minutes=expires_minutes)
    return create_access_token(subject=user_identifier, expires_delta=expires_delta)


# ================================================================
# 📊 INFORMACIÓN Y LOGS DE SEGURIDAD
# ================================================================

def log_security_event(
    event_type: str, 
    user_id: str, 
    details: str = "", 
    ip_address: str = ""
) -> None:
    """
    📊 Registra eventos de seguridad para auditoría
    
    Importante para cumplimiento y monitoreo de seguridad en entornos empresariales.
    
    Args:
        event_type (str): Tipo de evento (login, logout, token_refresh, etc.)
        user_id (str): Identificador del usuario involucrado
        details (str): Detalles adicionales del evento
        ip_address (str): Dirección IP del cliente
    """
    # TODO: Implementar logging estructurado con Loguru
    # Por ahora un print simple (se mejorará en el módulo de logs)
    timestamp = datetime.utcnow().isoformat()
    print(f"🔐 [{timestamp}] {event_type}: {user_id} - {details} (IP: {ip_address})")


# ================================================================
# 🛡️ VALIDADORES ADICIONALES
# ================================================================

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    💪 Valida la fortaleza de una contraseña
    
    Verifica que la contraseña cumple con los requisitos mínimos de seguridad
    para un entorno empresarial.
    
    Args:
        password (str): Contraseña a validar
        
    Returns:
        tuple[bool, str]: (es_válida, mensaje_de_error)
        
    Example:
        >>> is_valid, message = validate_password_strength("MiPassword123!")
        >>> print(f"Válida: {is_valid}, Mensaje: {message}")
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not any(c.isupper() for c in password):
        return False, "La contraseña debe contener al menos una mayúscula"
    
    if not any(c.islower() for c in password):
        return False, "La contraseña debe contener al menos una minúscula"
    
    if not any(c.isdigit() for c in password):
        return False, "La contraseña debe contener al menos un número"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "La contraseña debe contener al menos un carácter especial"
    
    return True, "Contraseña válida"


# ================================================================
# 📋 CONSTANTES DE SEGURIDAD
# ================================================================

# Mensajes de error estándar para evitar information leakage
INVALID_CREDENTIALS_MESSAGE = "Email o contraseña incorrectos"
TOKEN_EXPIRED_MESSAGE = "Token expirado, por favor inicie sesión nuevamente"
INSUFFICIENT_PERMISSIONS_MESSAGE = "Permisos insuficientes para esta operación"
ACCOUNT_DISABLED_MESSAGE = "Cuenta deshabilitada, contacte al administrador"

# Headers de seguridad recomendados
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
}


if __name__ == "__main__":
    # Ejemplo de uso del módulo de seguridad
    print("🔐 ===== DEMO DEL MÓDULO DE SEGURIDAD =====")
    
    # Demostrar hash de contraseña
    password = "mi_contraseña_segura_123!"
    hashed = create_password_hash(password)
    print(f"🔒 Hash de contraseña: {hashed[:50]}...")
    
    # Verificar contraseña
    is_valid = verify_password(password, hashed)
    print(f"✅ Verificación: {is_valid}")
    
    # Crear tokens
    user_email = "admin@erpro.com"
    tokens = generate_secure_token_pair(user_email)
    print(f"🎫 Access token creado: {tokens['access_token'][:50]}...")
    print(f"🔄 Refresh token creado: {tokens['refresh_token'][:50]}...")
    
    # Validar token
    user_from_token = validate_access_token(tokens['access_token'])
    print(f"👤 Usuario del token: {user_from_token}")
    
    print("🔐 ==========================================")