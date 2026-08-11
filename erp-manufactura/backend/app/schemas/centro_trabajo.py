"""
Schemas Pydantic para Centro de Trabajo.
Define estructuras de request y response validadas.
"""

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class CentroTrabajoCreate(BaseModel):
    """Datos para crear un centro de trabajo."""

    nombre: str
    codigo: str
    capacidad: Decimal = Decimal("1.0")
    costo_hora: Decimal = Decimal("0.0")
    activo: bool = True
    notas: str | None = None


class CentroTrabajoUpdate(BaseModel):
    """Datos para actualizar un centro de trabajo (todos opcionales)."""

    nombre: str | None = None
    codigo: str | None = None
    capacidad: Decimal | None = None
    costo_hora: Decimal | None = None
    activo: bool | None = None
    notas: str | None = None


class CentroTrabajoResponse(BaseModel):
    """Respuesta con datos completos del centro de trabajo."""

    id: int
    nombre: str
    codigo: str
    capacidad: Decimal
    costo_hora: Decimal
    activo: bool
    notas: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
