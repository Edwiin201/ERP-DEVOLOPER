"""
Modelo SQLAlchemy para Ordenes de Trabajo.
Equivalente a mrp.workorder en Odoo.
"""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class OrdenTrabajo(Base):
    """Orden de trabajo vinculada a una produccion y centro de trabajo."""

    __tablename__ = "ordenes_trabajo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    produccion_id = Column(
        Integer, ForeignKey("producciones.id", ondelete="CASCADE"), nullable=False
    )
    centro_trabajo_id = Column(Integer, ForeignKey("centros_trabajo.id"), nullable=True)
    estado = Column(String(20), default="pendiente")
    duracion_esperada = Column(Numeric(10, 2), nullable=True)
    duracion_real = Column(Numeric(10, 2), nullable=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    secuencia = Column(Integer, default=10)
    notas = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    produccion = relationship("Produccion", back_populates="ordenes_trabajo")
    centro_trabajo = relationship("CentroTrabajo", back_populates="ordenes_trabajo")

    def __repr__(self):
        return f"<OrdenTrabajo(id={self.id}, nombre='{self.nombre}', estado='{self.estado}')>"
