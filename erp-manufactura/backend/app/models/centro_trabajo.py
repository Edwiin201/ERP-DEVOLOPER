"""
Modelo SQLAlchemy para Centros de Trabajo.
Equivalente a mrp.workcenter en Odoo.
"""

from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class CentroTrabajo(Base):
    """Centro de trabajo donde se ejecutan operaciones de manufactura."""

    __tablename__ = "centros_trabajo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    capacidad = Column(Numeric(10, 2), default=1.0)
    costo_hora = Column(Numeric(10, 2), default=0.0)
    activo = Column(Boolean, default=True)
    notas = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    ordenes_trabajo = relationship("OrdenTrabajo", back_populates="centro_trabajo")
    producciones = relationship("Produccion", back_populates="centro_trabajo")

    def __repr__(self):
        return f"<CentroTrabajo(id={self.id}, codigo='{self.codigo}', nombre='{self.nombre}')>"
