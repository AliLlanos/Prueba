"""
👤 ERP Professional - Modelo de Usuario
=======================================

Este módulo define el modelo de Usuario para el sistema ERP.
Incluye autenticación, autorización, perfiles y gestión de sesiones.

Características incluidas:
- Autenticación con hash de contraseñas
- Roles y permisos granulares
- Información de perfil completa
- Auditoría de sesiones
- Integración con JWT
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum as SQLEnum, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from typing import Optional
import enum

from app.models.base import Base, NameMixin
from app.core.security import create_password_hash, verify_password


# ================================================================
# 🏷️ ENUMERACIONES
# ================================================================

class UserRole(str, enum.Enum):
    """
    👑 Roles de usuario en el sistema ERP
    
    Define los diferentes niveles de acceso y responsabilidades
    dentro del sistema empresarial.
    """
    SUPER_ADMIN = "super_admin"      # Acceso total al sistema
    ADMIN = "admin"                  # Administrador de empresa
    MANAGER = "manager"              # Gerente de área
    EMPLOYEE = "employee"            # Empleado estándar
    ACCOUNTANT = "accountant"        # Contador/Contabilidad
    SALES_REP = "sales_rep"          # Representante de ventas
    WAREHOUSE = "warehouse"          # Personal de almacén
    HR = "hr"                       # Recursos humanos
    VIEWER = "viewer"               # Solo lectura


class UserStatus(str, enum.Enum):
    """
    📊 Estados del usuario
    
    Define el estado actual de la cuenta del usuario.
    """
    ACTIVE = "active"               # Usuario activo
    INACTIVE = "inactive"           # Usuario inactivo temporal
    SUSPENDED = "suspended"         # Usuario suspendido
    PENDING = "pending"             # Pendiente de activación
    LOCKED = "locked"              # Cuenta bloqueada por seguridad


# ================================================================
# 👤 MODELO DE USUARIO
# ================================================================

class User(Base, NameMixin):
    """
    👤 Modelo de Usuario del sistema ERP
    
    Representa a todos los usuarios del sistema, desde administradores
    hasta empleados regulares. Incluye autenticación, autorización
    y información de perfil completa.
    
    Attributes:
        email (str): Email único del usuario (usado para login)
        password_hash (str): Hash bcrypt de la contraseña
        role (UserRole): Rol del usuario en el sistema
        status (UserStatus): Estado actual de la cuenta
        first_name (str): Nombre del usuario
        last_name (str): Apellido del usuario
        phone (str): Número de teléfono
        avatar_url (str): URL del avatar/foto de perfil
        department (str): Departamento al que pertenece
        position (str): Cargo o posición
        is_superuser (bool): Si es superusuario
        is_verified (bool): Si el email está verificado
        last_login (datetime): Último inicio de sesión
        login_attempts (int): Intentos de login fallidos
        password_changed_at (datetime): Última vez que cambió contraseña
    """
    
    __tablename__ = "users"
    
    # ============================================================
    # 🔐 CAMPOS DE AUTENTICACIÓN
    # ============================================================
    
    email: str = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Email único del usuario (usado para login)"
    )
    
    password_hash: str = Column(
        String(255),
        nullable=False,
        comment="Hash bcrypt de la contraseña"
    )
    
    # ============================================================
    # 👑 CAMPOS DE AUTORIZACIÓN
    # ============================================================
    
    role: UserRole = Column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.EMPLOYEE,
        comment="Rol del usuario en el sistema"
    )
    
    status: UserStatus = Column(
        SQLEnum(UserStatus),
        nullable=False,
        default=UserStatus.PENDING,
        comment="Estado actual de la cuenta"
    )
    
    is_superuser: bool = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Si es superusuario con acceso total"
    )
    
    is_verified: bool = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Si el email está verificado"
    )
    
    # ============================================================
    # 📋 INFORMACIÓN PERSONAL
    # ============================================================
    
    first_name: str = Column(
        String(100),
        nullable=False,
        comment="Nombre del usuario"
    )
    
    last_name: str = Column(
        String(100),
        nullable=False,
        comment="Apellido del usuario"
    )
    
    phone: Optional[str] = Column(
        String(20),
        nullable=True,
        comment="Número de teléfono"
    )
    
    avatar_url: Optional[str] = Column(
        String(500),
        nullable=True,
        comment="URL del avatar/foto de perfil"
    )
    
    # ============================================================
    # 🏢 INFORMACIÓN LABORAL
    # ============================================================
    
    department: Optional[str] = Column(
        String(100),
        nullable=True,
        comment="Departamento al que pertenece"
    )
    
    position: Optional[str] = Column(
        String(100),
        nullable=True,
        comment="Cargo o posición"
    )
    
    employee_id: Optional[str] = Column(
        String(50),
        nullable=True,
        unique=True,
        comment="ID de empleado único"
    )
    
    hire_date: Optional[datetime] = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Fecha de contratación"
    )
    
    # ============================================================
    # 🔒 CAMPOS DE SEGURIDAD
    # ============================================================
    
    last_login: Optional[datetime] = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Último inicio de sesión exitoso"
    )
    
    login_attempts: int = Column(
        Integer,
        default=0,
        nullable=False,
        comment="Intentos de login fallidos consecutivos"
    )
    
    password_changed_at: datetime = Column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
        comment="Última vez que cambió la contraseña"
    )
    
    locked_until: Optional[datetime] = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Fecha hasta la cual está bloqueada la cuenta"
    )
    
    # ============================================================
    # 📝 CAMPOS ADICIONALES
    # ============================================================
    
    notes: Optional[str] = Column(
        Text,
        nullable=True,
        comment="Notas administrativas sobre el usuario"
    )
    
    preferences: Optional[str] = Column(
        Text,
        nullable=True,
        comment="Preferencias del usuario en formato JSON"
    )
    
    timezone: str = Column(
        String(50),
        default="UTC",
        nullable=False,
        comment="Zona horaria del usuario"
    )
    
    language: str = Column(
        String(10),
        default="es",
        nullable=False,
        comment="Idioma preferido del usuario"
    )
    
    # ============================================================
    # 🔗 RELACIONES
    # ============================================================
    
    # TODO: Añadir relaciones cuando se creen otros modelos
    # created_sales = relationship("Sale", back_populates="created_by_user")
    # assigned_tasks = relationship("Task", back_populates="assigned_user")
    
    # ============================================================
    # 🔧 MÉTODOS DE CONTRASEÑA
    # ============================================================
    
    def set_password(self, password: str) -> None:
        """
        🔐 Establece una nueva contraseña para el usuario
        
        Hashea la contraseña usando bcrypt y actualiza el timestamp
        de cambio de contraseña.
        
        Args:
            password (str): Nueva contraseña en texto plano
        """
        self.password_hash = create_password_hash(password)
        self.password_changed_at = datetime.utcnow()
        self.login_attempts = 0  # Reset intentos fallidos
    
    def verify_password(self, password: str) -> bool:
        """
        ✅ Verifica si una contraseña es correcta
        
        Args:
            password (str): Contraseña a verificar
            
        Returns:
            bool: True si la contraseña es correcta
        """
        return verify_password(password, self.password_hash)
    
    def is_password_expired(self, days: int = 90) -> bool:
        """
        ⏰ Verifica si la contraseña ha expirado
        
        Args:
            days (int): Días máximos de validez de la contraseña
            
        Returns:
            bool: True si la contraseña ha expirado
        """
        if not self.password_changed_at:
            return True
        
        expiry_date = self.password_changed_at + timedelta(days=days)
        return datetime.utcnow() > expiry_date
    
    # ============================================================
    # 🔒 MÉTODOS DE SEGURIDAD
    # ============================================================
    
    def increment_login_attempts(self) -> None:
        """
        📈 Incrementa el contador de intentos fallidos de login
        
        Bloquea la cuenta si se excede el límite de intentos.
        """
        self.login_attempts += 1
        
        # Bloquear cuenta después de 5 intentos fallidos
        if self.login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)
            self.status = UserStatus.LOCKED
    
    def reset_login_attempts(self) -> None:
        """
        🔄 Resetea el contador de intentos fallidos
        
        Se llama después de un login exitoso.
        """
        self.login_attempts = 0
        self.last_login = datetime.utcnow()
        
        # Desbloquear cuenta si estaba bloqueada
        if self.status == UserStatus.LOCKED:
            self.status = UserStatus.ACTIVE
            self.locked_until = None
    
    def is_account_locked(self) -> bool:
        """
        🔒 Verifica si la cuenta está bloqueada
        
        Returns:
            bool: True si la cuenta está bloqueada
        """
        if self.status == UserStatus.LOCKED:
            # Verificar si el bloqueo ha expirado
            if self.locked_until and datetime.utcnow() > self.locked_until:
                self.status = UserStatus.ACTIVE
                self.locked_until = None
                self.login_attempts = 0
                return False
            return True
        return False
    
    def can_login(self) -> tuple[bool, str]:
        """
        ✅ Verifica si el usuario puede iniciar sesión
        
        Returns:
            tuple[bool, str]: (puede_login, mensaje_error)
        """
        if not self.is_active:
            return False, "Cuenta desactivada"
        
        if self.status == UserStatus.SUSPENDED:
            return False, "Cuenta suspendida"
        
        if self.status == UserStatus.PENDING:
            return False, "Cuenta pendiente de activación"
        
        if self.is_account_locked():
            return False, "Cuenta bloqueada por intentos fallidos"
        
        return True, ""
    
    # ============================================================
    # 👑 MÉTODOS DE AUTORIZACIÓN
    # ============================================================
    
    def has_role(self, role: UserRole) -> bool:
        """
        👑 Verifica si el usuario tiene un rol específico
        
        Args:
            role (UserRole): Rol a verificar
            
        Returns:
            bool: True si tiene el rol
        """
        return self.role == role
    
    def has_permission(self, permission: str) -> bool:
        """
        🛡️ Verifica si el usuario tiene un permiso específico
        
        Args:
            permission (str): Permiso a verificar
            
        Returns:
            bool: True si tiene el permiso
        """
        # Superusuarios tienen todos los permisos
        if self.is_superuser:
            return True
        
        # Mapeo de roles a permisos (simplificado)
        role_permissions = {
            UserRole.SUPER_ADMIN: ["all"],
            UserRole.ADMIN: ["users.manage", "inventory.manage", "sales.manage", "reports.view"],
            UserRole.MANAGER: ["inventory.view", "sales.manage", "reports.view"],
            UserRole.EMPLOYEE: ["inventory.view", "sales.view"],
            UserRole.ACCOUNTANT: ["accounting.manage", "reports.view"],
            UserRole.SALES_REP: ["sales.manage", "customers.manage"],
            UserRole.WAREHOUSE: ["inventory.manage"],
            UserRole.HR: ["employees.manage"],
            UserRole.VIEWER: ["*.view"],
        }
        
        user_permissions = role_permissions.get(self.role, [])
        return permission in user_permissions or "all" in user_permissions
    
    def is_admin(self) -> bool:
        """
        👑 Verifica si el usuario es administrador
        
        Returns:
            bool: True si es admin o superuser
        """
        return self.is_superuser or self.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN]
    
    # ============================================================
    # 📋 MÉTODOS DE INFORMACIÓN
    # ============================================================
    
    @property
    def full_name(self) -> str:
        """
        📝 Nombre completo del usuario
        
        Returns:
            str: Nombre y apellido concatenados
        """
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def display_name(self) -> str:
        """
        🏷️ Nombre para mostrar en la interfaz
        
        Returns:
            str: Nombre para mostrar
        """
        return self.name or self.full_name or self.email
    
    @property
    def initials(self) -> str:
        """
        🔤 Iniciales del usuario
        
        Returns:
            str: Iniciales del nombre y apellido
        """
        first_initial = self.first_name[0].upper() if self.first_name else ""
        last_initial = self.last_name[0].upper() if self.last_name else ""
        return f"{first_initial}{last_initial}"
    
    def get_avatar_url(self, size: int = 150) -> str:
        """
        🖼️ Obtiene URL del avatar del usuario
        
        Si no tiene avatar, genera uno usando un servicio de avatares.
        
        Args:
            size (int): Tamaño del avatar en píxeles
            
        Returns:
            str: URL del avatar
        """
        if self.avatar_url:
            return self.avatar_url
        
        # Generar avatar por defecto usando iniciales
        return f"https://ui-avatars.com/api/?name={self.initials}&size={size}&background=1976d2&color=fff"
    
    # ============================================================
    # 🔄 MÉTODOS DE SERIALIZACIÓN
    # ============================================================
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        📋 Convierte el usuario a diccionario
        
        Args:
            include_sensitive (bool): Si incluir información sensible
            
        Returns:
            dict: Datos del usuario
        """
        data = super().to_dict(exclude_fields=["password_hash"])
        
        # Añadir campos calculados
        data.update({
            "full_name": self.full_name,
            "display_name": self.display_name,
            "initials": self.initials,
            "avatar_url": self.get_avatar_url(),
            "can_login": self.can_login()[0],
            "is_admin": self.is_admin(),
        })
        
        # Incluir información sensible solo si se solicita
        if not include_sensitive:
            sensitive_fields = ["login_attempts", "locked_until", "notes"]
            for field in sensitive_fields:
                data.pop(field, None)
        
        return data
    
    def __repr__(self) -> str:
        """
        📋 Representación string del usuario
        """
        return f"<User(email='{self.email}', role='{self.role}', active={self.is_active})>"


# ================================================================
# 🔧 FUNCIONES UTILITARIAS
# ================================================================

def create_user(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    role: UserRole = UserRole.EMPLOYEE,
    **kwargs
) -> User:
    """
    👤 Crea un nuevo usuario con validaciones
    
    Args:
        email (str): Email del usuario
        password (str): Contraseña en texto plano
        first_name (str): Nombre
        last_name (str): Apellido
        role (UserRole): Rol del usuario
        **kwargs: Campos adicionales
        
    Returns:
        User: Nuevo usuario creado
    """
    user = User(
        email=email.lower().strip(),
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        role=role,
        status=UserStatus.ACTIVE,
        **kwargs
    )
    
    # Establecer contraseña (se hashea automáticamente)
    user.set_password(password)
    
    return user


def create_admin_user(
    email: str,
    password: str,
    first_name: str,
    last_name: str
) -> User:
    """
    👑 Crea un usuario administrador
    
    Args:
        email (str): Email del administrador
        password (str): Contraseña
        first_name (str): Nombre
        last_name (str): Apellido
        
    Returns:
        User: Usuario administrador creado
    """
    return create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=UserRole.ADMIN,
        is_superuser=True,
        status=UserStatus.ACTIVE,
        is_verified=True
    )