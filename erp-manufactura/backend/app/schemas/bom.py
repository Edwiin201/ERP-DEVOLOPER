"""
Schemas Pydantic para BOM (Lista de Materiales) y sus lineas.
Soporta estructuras anidadas para crear/actualizar con lineas.
"""

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


# ============================================
# Schemas para Lineas de BOM
# ============================================


class BOMLineaCreate(BaseModel):
    """Datos para crear una linea de BOM."""

    producto_id: int
    cantidad: Decimal = Decimal("1.0")
    producto_uom: str | None = None
    secuencia: int = 10


class BOMLineaUpdate(BaseModel):
    """Datos para actualizar una linea de BOM."""

    producto_id: int | None = None
    cantidad: Decimal | None = None
    producto_uom: str | None = None
    secuencia: int | None = None


class BOMLineaResponse(BaseModel):
    """Respuesta con datos de una linea de BOM."""

    id: int
    bom_id: int
    producto_id: int
    cantidad: Decimal
    producto_uom: str | None
    secuencia: int

    class Config:
        from_attributes = True


# ============================================
# Schemas para BOM
# ============================================


class BOMCreate(BaseModel):
    """Datos para crear un BOM con sus lineas."""

    codigo: str | None = None
    nombre: str
    producto_id: int
    cantidad: Decimal = Decimal("1.0")
    producto_uom: str | None = None
    estado: str = "activo"
    company_id: int | None = None
    lineas: list[BOMLineaCreate] = []


class BOMUpdate(BaseModel):
    """Datos para actualizar un BOM y sus lineas."""

    codigo: str | None = None
    nombre: str | None = None
    producto_id: int | None = None
    cantidad: Decimal | None = None
    producto_uom: str | None = None
    estado: str | None = None
    company_id: int | None = None
    lineas: list[BOMLineaCreate] | None = None


class BOMResponse(BaseModel):
    """Respuesta con datos completos del BOM incluyendo lineas."""

    id: int
    codigo: str | None
    nombre: str
    producto_id: int
    cantidad: Decimal
    producto_uom: str | None
    estado: str
    company_id: int | None
    created_at: datetime
    updated_at: datetime
    lineas: list[BOMLineaResponse] = []

    class Config:
        from_attributes = True
