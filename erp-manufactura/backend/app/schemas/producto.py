"""
Schemas Pydantic para Producto.
Define estructuras de request y response validadas.
"""

from pydantic import BaseModel
from datetime import datetime


class ProductoCreate(BaseModel):
    """Datos para crear un producto."""

    nombre: str
    tipo: str = "producto_final"


class ProductoUpdate(BaseModel):
    """Datos para actualizar un producto."""

    nombre: str | None = None
    tipo: str | None = None


class ProductoResponse(BaseModel):
    """Respuesta con datos completos del producto."""

    id: int
    nombre: str
    tipo: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
