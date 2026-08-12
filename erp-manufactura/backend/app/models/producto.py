"""
Modelo SQLAlchemy para Productos.
Entidad de referencia para producciones, BOMs y lineas de BOM.
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Producto(Base):
    """Producto de manufactura (materia prima o producto final)."""

    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    tipo = Column(String(20), default="producto_final")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones inversas
    producciones = relationship("Produccion", back_populates="producto")
    boms = relationship("BOM", back_populates="producto")
    bom_lineas = relationship("BOMLinea", back_populates="producto")

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo}')>"
