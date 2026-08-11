"""
Schemas Pydantic para Produccion.
Define estructuras de request y response validadas.
"""

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class ProduccionCreate(BaseModel):
    """Datos para crear una orden de produccion."""

    producto_id: int
    cantidad: Decimal = Decimal("1.0")
    producto_uom: str | None = None
    bom_id: int | None = None
    centro_trabajo_id: int | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    notas: str | None = None
    company_id: int | None = None


class ProduccionUpdate(BaseModel):
    """Datos para actualizar una orden de produccion."""

    producto_id: int | None = None
    cantidad: Decimal | None = None
    producto_uom: str | None = None
    bom_id: int | None = None
    centro_trabajo_id: int | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    notas: str | None = None
    company_id: int | None = None


class ProduccionResponse(BaseModel):
    """Respuesta con datos completos de la produccion."""

    id: int
    nombre: str
    producto_id: int
    cantidad: Decimal
    producto_uom: str | None
    bom_id: int | None
    centro_trabajo_id: int | None
    fecha_inicio: datetime | None
    fecha_fin: datetime | None
    estado: str
    notas: str | None
    company_id: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
