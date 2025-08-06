"""
🏗️ ERP Professional - Modelo Base
==================================

Este módulo define la clase base para todos los modelos SQLAlchemy del sistema ERP.
Incluye funcionalidades comunes como timestamps, soft delete, y métodos utilitarios.

Características incluidas:
- Timestamps automáticos (created_at, updated_at)
- Soft delete con campo deleted_at
- ID único con UUID
- Métodos utilitarios para serialización
- Auditoría básica con created_by, updated_by
"""

import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from sqlalchemy import Column, DateTime, String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session


@as_declarative()
class Base:
    """
    🏗️ Clase base para todos los modelos del ERP
    
    Proporciona funcionalidades comunes que todos los modelos necesitan:
    - ID único usando UUID
    - Timestamps automáticos  
    - Soft delete
    - Auditoría básica
    - Métodos de serialización
    """
    
    # ID único para cada registro usando UUID
    # UUID es mejor que auto-incremento para sistemas distribuidos
    id: UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="Identificador único del registro"
    )
    
    # ================================================================
    # 🕒 TIMESTAMPS AUTOMÁTICOS
    # ================================================================
    
    # Fecha y hora de creación del registro
    created_at: datetime = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="Fecha y hora de creación del registro"
    )
    
    # Fecha y hora de última actualización
    updated_at: datetime = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="Fecha y hora de última actualización"
    )
    
    # ================================================================
    # 🗑️ SOFT DELETE
    # ================================================================
    
    # Campo para soft delete - permite "eliminar" sin borrar realmente
    deleted_at: Optional[datetime] = Column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        comment="Fecha y hora de eliminación lógica (soft delete)"
    )
    
    # Flag de activo/inactivo para control adicional
    is_active: bool = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Indica si el registro está activo"
    )
    
    # ================================================================
    # 👤 AUDITORÍA BÁSICA
    # ================================================================
    
    # Usuario que creó el registro
    created_by: Optional[str] = Column(
        String(255),
        nullable=True,
        comment="Usuario que creó el registro"
    )
    
    # Usuario que actualizó el registro por última vez
    updated_by: Optional[str] = Column(
        String(255), 
        nullable=True,
        comment="Usuario que actualizó el registro por última vez"
    )
    
    # ================================================================
    # 🏷️ NOMBRE DE TABLA AUTOMÁTICO
    # ================================================================
    
    @declared_attr
    def __tablename__(cls) -> str:
        """
        🏷️ Genera nombre de tabla automáticamente
        
        Convierte el nombre de la clase a snake_case para el nombre de tabla.
        Ejemplo: ProductCategory -> product_category
        """
        import re
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return name
    
    # ================================================================
    # 🔧 MÉTODOS UTILITARIOS
    # ================================================================
    
    def to_dict(self, exclude_fields: Optional[list] = None) -> Dict[str, Any]:
        """
        📋 Convierte el modelo a diccionario
        
        Útil para serialización JSON y APIs. Excluye campos sensibles por defecto.
        
        Args:
            exclude_fields (Optional[list]): Campos a excluir de la serialización
            
        Returns:
            Dict[str, Any]: Diccionario con los datos del modelo
        """
        if exclude_fields is None:
            exclude_fields = []
        
        # Campos que se excluyen por defecto por seguridad
        default_exclude = ['deleted_at']
        exclude_fields.extend(default_exclude)
        
        result = {}
        for column in self.__table__.columns:
            field_name = column.name
            if field_name not in exclude_fields:
                value = getattr(self, field_name)
                
                # Convertir tipos especiales para JSON
                if isinstance(value, datetime):
                    result[field_name] = value.isoformat() if value else None
                elif isinstance(value, uuid.UUID):
                    result[field_name] = str(value)
                else:
                    result[field_name] = value
                    
        return result
    
    def update_from_dict(self, data: Dict[str, Any], exclude_fields: Optional[list] = None) -> None:
        """
        🔄 Actualiza el modelo desde un diccionario
        
        Útil para actualizar modelos desde datos de API.
        
        Args:
            data (Dict[str, Any]): Datos para actualizar
            exclude_fields (Optional[list]): Campos a no actualizar
        """
        if exclude_fields is None:
            exclude_fields = []
        
        # Campos que nunca se deben actualizar desde datos externos
        protected_fields = ['id', 'created_at', 'created_by']
        exclude_fields.extend(protected_fields)
        
        for key, value in data.items():
            if hasattr(self, key) and key not in exclude_fields:
                setattr(self, key, value)
    
    def soft_delete(self, deleted_by: Optional[str] = None) -> None:
        """
        🗑️ Realiza eliminación lógica (soft delete)
        
        Marca el registro como eliminado sin borrarlo físicamente de la base de datos.
        Esto es importante para auditoría y recuperación de datos.
        
        Args:
            deleted_by (Optional[str]): Usuario que realizó la eliminación
        """
        self.deleted_at = datetime.utcnow()
        self.is_active = False
        if deleted_by:
            self.updated_by = deleted_by
    
    def restore(self, restored_by: Optional[str] = None) -> None:
        """
        ♻️ Restaura un registro eliminado lógicamente
        
        Revierte la eliminación lógica del registro.
        
        Args:
            restored_by (Optional[str]): Usuario que realizó la restauración
        """
        self.deleted_at = None
        self.is_active = True
        if restored_by:
            self.updated_by = restored_by
    
    def is_deleted(self) -> bool:
        """
        ❓ Verifica si el registro está eliminado lógicamente
        
        Returns:
            bool: True si está eliminado, False si no
        """
        return self.deleted_at is not None
    
    def refresh_updated_at(self, updated_by: Optional[str] = None) -> None:
        """
        🔄 Actualiza manualmente el timestamp de modificación
        
        Útil cuando se hacen cambios que SQLAlchemy no detecta automáticamente.
        
        Args:
            updated_by (Optional[str]): Usuario que realizó la actualización
        """
        self.updated_at = datetime.utcnow()
        if updated_by:
            self.updated_by = updated_by
    
    def get_age_in_days(self) -> int:
        """
        📅 Obtiene la edad del registro en días
        
        Calcula cuántos días han pasado desde que se creó el registro.
        
        Returns:
            int: Número de días desde la creación
        """
        return (datetime.utcnow() - self.created_at).days
    
    def was_modified_today(self) -> bool:
        """
        📅 Verifica si el registro fue modificado hoy
        
        Returns:
            bool: True si fue modificado hoy, False si no
        """
        today = datetime.utcnow().date()
        return self.updated_at.date() == today
    
    # ================================================================
    # 🔍 MÉTODOS DE CONSULTA ESTÁTICOS
    # ================================================================
    
    @classmethod
    def get_active_records(cls, db: Session):
        """
        📋 Obtiene solo los registros activos (no eliminados)
        
        Args:
            db (Session): Sesión de base de datos
            
        Returns:
            Query: Query filtrado por registros activos
        """
        return db.query(cls).filter(
            cls.deleted_at.is_(None),
            cls.is_active == True
        )
    
    @classmethod
    def get_deleted_records(cls, db: Session):
        """
        🗑️ Obtiene solo los registros eliminados lógicamente
        
        Args:
            db (Session): Sesión de base de datos
            
        Returns:
            Query: Query filtrado por registros eliminados
        """
        return db.query(cls).filter(cls.deleted_at.isnot(None))
    
    @classmethod
    def get_recent_records(cls, db: Session, days: int = 7):
        """
        🆕 Obtiene registros creados en los últimos N días
        
        Args:
            db (Session): Sesión de base de datos
            days (int): Número de días hacia atrás
            
        Returns:
            Query: Query filtrado por registros recientes
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return cls.get_active_records(db).filter(
            cls.created_at >= cutoff_date
        )
    
    # ================================================================
    # 🎯 MÉTODOS ESPECIALES
    # ================================================================
    
    def __repr__(self) -> str:
        """
        📋 Representación string del modelo
        
        Útil para debugging y logs.
        """
        return f"<{self.__class__.__name__}(id={self.id})>"
    
    def __eq__(self, other) -> bool:
        """
        ⚖️ Compara dos instancias del modelo
        
        Dos modelos son iguales si tienen el mismo ID.
        """
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """
        🔢 Hash del modelo basado en el ID
        
        Permite usar modelos en sets y como keys de diccionarios.
        """
        return hash(self.id)


# ================================================================
# 🔧 FUNCIONES UTILITARIAS PARA MODELOS
# ================================================================

def create_audit_log(
    model_instance: Base,
    action: str,
    user_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    📊 Crea un log de auditoría para acciones en modelos
    
    Registra cambios importantes para cumplimiento y auditoría.
    
    Args:
        model_instance (Base): Instancia del modelo afectado
        action (str): Acción realizada (create, update, delete, etc.)
        user_id (Optional[str]): ID del usuario que realizó la acción
        details (Optional[Dict[str, Any]]): Detalles adicionales
        
    Returns:
        Dict[str, Any]: Entrada de log de auditoría
    """
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "model_type": model_instance.__class__.__name__,
        "model_id": str(model_instance.id),
        "action": action,
        "user_id": user_id,
        "details": details or {},
        "previous_state": model_instance.to_dict() if hasattr(model_instance, 'to_dict') else None
    }


def bulk_soft_delete(
    db: Session,
    model_class: Base,
    ids: list,
    deleted_by: Optional[str] = None
) -> int:
    """
    🗑️ Eliminación lógica en lote
    
    Elimina múltiples registros de manera eficiente.
    
    Args:
        db (Session): Sesión de base de datos
        model_class (Base): Clase del modelo a eliminar
        ids (list): Lista de IDs a eliminar
        deleted_by (Optional[str]): Usuario que realizó la eliminación
        
    Returns:
        int: Número de registros eliminados
    """
    from datetime import datetime
    
    update_data = {
        "deleted_at": datetime.utcnow(),
        "is_active": False,
        "updated_at": datetime.utcnow()
    }
    
    if deleted_by:
        update_data["updated_by"] = deleted_by
    
    result = db.query(model_class).filter(
        model_class.id.in_(ids),
        model_class.deleted_at.is_(None)
    ).update(update_data, synchronize_session=False)
    
    db.commit()
    return result


# ================================================================
# 📋 MIXINS ADICIONALES
# ================================================================

class NameMixin:
    """
    🏷️ Mixin para modelos que tienen nombre
    
    Proporciona campos y métodos comunes para modelos con nombre.
    """
    
    name: str = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Nombre del registro"
    )
    
    description: Optional[str] = Column(
        String(1000),
        nullable=True,
        comment="Descripción opcional del registro"
    )
    
    def __str__(self) -> str:
        """Representación string usando el nombre"""
        return self.name or f"{self.__class__.__name__}({self.id})"


class CodeMixin:
    """
    🔢 Mixin para modelos que tienen código único
    
    Proporciona campo de código con validaciones.
    """
    
    code: str = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        comment="Código único del registro"
    )
    
    @classmethod
    def generate_next_code(cls, db: Session, prefix: str = "") -> str:
        """
        🔢 Genera el siguiente código secuencial
        
        Args:
            db (Session): Sesión de base de datos
            prefix (str): Prefijo para el código
            
        Returns:
            str: Siguiente código disponible
        """
        # Buscar el último código con el prefijo
        last_record = db.query(cls).filter(
            cls.code.like(f"{prefix}%")
        ).order_by(cls.code.desc()).first()
        
        if not last_record:
            return f"{prefix}001"
        
        # Extraer número y incrementar
        last_code = last_record.code
        number_part = last_code.replace(prefix, "")
        
        try:
            next_number = int(number_part) + 1
            return f"{prefix}{next_number:03d}"
        except ValueError:
            return f"{prefix}001"


if __name__ == "__main__":
    # Ejemplo de uso del modelo base
    print("🏗️ ===== DEMO DEL MODELO BASE =====")
    
    # El modelo base se usa como herencia, no directamente
    print("✅ Modelo base definido con éxito")
    print("📋 Características incluidas:")
    print("   - ID único con UUID")
    print("   - Timestamps automáticos")
    print("   - Soft delete")
    print("   - Auditoría básica")
    print("   - Métodos de serialización")
    print("   - Mixins para nombre y código")
    print("🏗️ ====================================")