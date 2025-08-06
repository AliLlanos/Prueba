"""
🗄️ ERP Professional - Modelos de Base de Datos
===============================================

Este paquete contiene todos los modelos SQLAlchemy para el sistema ERP.
Los modelos están organizados por módulos de negocio para mejor mantenimiento.

Módulos incluidos:
- User: Gestión de usuarios y autenticación
- Company: Información de la empresa
- Inventory: Productos, categorías, stock
- Sales: Clientes, cotizaciones, ventas
- Purchasing: Proveedores, órdenes de compra
- Accounting: Contabilidad, plan de cuentas
- HR: Recursos humanos, empleados, nómina
"""

# Importar todos los modelos para que estén disponibles
from app.models.user import User
from app.models.company import Company
from app.models.inventory import Category, Product, Stock, StockMovement
from app.models.sales import Customer, Quote, Sale, SaleDetail
from app.models.purchasing import Supplier, PurchaseOrder, PurchaseOrderDetail
from app.models.accounting import Account, Transaction, TransactionDetail
from app.models.hr import Employee, Department, Position

# Lista de todos los modelos para fácil importación
__all__ = [
    # Usuario y empresa
    "User",
    "Company",
    
    # Inventario
    "Category",
    "Product", 
    "Stock",
    "StockMovement",
    
    # Ventas
    "Customer",
    "Quote",
    "Sale",
    "SaleDetail",
    
    # Compras
    "Supplier",
    "PurchaseOrder",
    "PurchaseOrderDetail",
    
    # Contabilidad
    "Account",
    "Transaction",
    "TransactionDetail",
    
    # Recursos Humanos
    "Employee",
    "Department",
    "Position",
]