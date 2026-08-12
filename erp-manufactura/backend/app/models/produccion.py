"""
Modelo SQLAlchemy para Producciones.
Equivalente a mrp.production en Odoo.
"""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Produccion(Base):
    """Orden de produccion de manufactura."""

    __tablename__ = "producciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Numeric(10, 2), nullable=False, default=1.0)
    producto_uom = Column(String(50), nullable=True)
    bom_id = Column(Integer, ForeignKey("boms.id"), nullable=True)
    centro_trabajo_id = Column(Integer, ForeignKey("centros_trabajo.id"), nullable=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    estado = Column(String(20), default="borrador")
    notas = Column(Text, nullable=True)
    company_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    producto = relationship("Producto", back_populates="producciones")
    bom = relationship("BOM", back_populates="producciones")
    centro_trabajo = relationship("CentroTrabajo", back_populates="producciones")
    ordenes_trabajo = relationship(
        "OrdenTrabajo",
        back_populates="produccion",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Produccion(id={self.id}, nombre='{self.nombre}', estado='{self.estado}')>"
