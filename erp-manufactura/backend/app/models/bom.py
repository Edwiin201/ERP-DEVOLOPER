"""
Modelos SQLAlchemy para BOM (Lista de Materiales) y sus lineas.
Equivalente a mrp.bom y mrp.bom.line en Odoo.
"""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class BOM(Base):
    """Lista de materiales (Bill of Materials)."""

    __tablename__ = "boms"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), nullable=True)
    nombre = Column(String(200), nullable=False)
    producto_id = Column(Integer, nullable=False, index=True)
    cantidad = Column(Numeric(10, 2), default=1.0)
    producto_uom = Column(String(50), nullable=True)
    estado = Column(String(20), default="activo")
    company_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    lineas = relationship(
        "BOMLinea",
        back_populates="bom",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    producciones = relationship("Produccion", back_populates="bom")

    def __repr__(self):
        return f"<BOM(id={self.id}, codigo='{self.codigo}', nombre='{self.nombre}')>"


class BOMLinea(Base):
    """Linea individual dentro de una lista de materiales."""

    __tablename__ = "bom_lineas"

    id = Column(Integer, primary_key=True, index=True)
    bom_id = Column(Integer, ForeignKey("boms.id", ondelete="CASCADE"), nullable=False)
    producto_id = Column(Integer, nullable=False)
    cantidad = Column(Numeric(10, 2), default=1.0)
    producto_uom = Column(String(50), nullable=True)
    secuencia = Column(Integer, default=10)

    # Relaciones
    bom = relationship("BOM", back_populates="lineas")

    def __repr__(self):
        return f"<BOMLinea(id={self.id}, bom_id={self.bom_id}, producto_id={self.producto_id})>"
