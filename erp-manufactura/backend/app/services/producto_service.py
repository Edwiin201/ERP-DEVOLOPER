"""
Servicio para Productos.
CRUD basico sin restricciones de negocio.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate


class ProductoService:
    """CRUD para productos."""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Producto]:
        """Lista todos los productos con paginacion."""
        stmt = select(Producto).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_by_id(db: Session, producto_id: int) -> Producto | None:
        """Obtiene un producto por ID."""
        return db.get(Producto, producto_id)

    @staticmethod
    def create(db: Session, data: ProductoCreate) -> Producto:
        """Crea un nuevo producto."""
        producto = Producto(**data.model_dump())
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto

    @staticmethod
    def update(db: Session, producto_id: int, data: ProductoUpdate) -> Producto:
        """Actualiza un producto."""
        producto = db.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(producto, key, value)

        db.commit()
        db.refresh(producto)
        return producto

    @staticmethod
    def delete(db: Session, producto_id: int) -> bool:
        """Elimina un producto."""
        producto = db.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        db.delete(producto)
        db.commit()
        return True
