"""
Schemas Pydantic para Orden de Trabajo.
Define estructuras de request y response validadas.
"""

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class OrdenTrabajoCreate(BaseModel):
    """Datos para crear una orden de trabajo."""

    nombre: str | None = None
    produccion_id: int
    centro_trabajo_id: int | None = None
    duracion_esperada: Decimal | None = None
    secuencia: int = 10
    notas: str | None = None


class OrdenTrabajoUpdate(BaseModel):
    """Datos para actualizar una orden de trabajo."""

    nombre: str | None = None
    produccion_id: int | None = None
    centro_trabajo_id: int | None = None
    duracion_esperada: Decimal | None = None
    duracion_real: Decimal | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    secuencia: int | None = None
    notas: str | None = None


class OrdenTrabajoResponse(BaseModel):
    """Respuesta con datos completos de la orden de trabajo."""

    id: int
    nombre: str
    produccion_id: int
    centro_trabajo_id: int | None
    estado: str
    duracion_esperada: Decimal | None
    duracion_real: Decimal | None
    fecha_inicio: datetime | None
    fecha_fin: datetime | None
    secuencia: int
    notas: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
