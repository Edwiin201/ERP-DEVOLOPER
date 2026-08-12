"""
Endpoints API REST para Productos.
Operaciones CRUD basicas.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.producto import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse,
)
from app.services.producto_service import ProductoService

router = APIRouter(prefix="/api/productos", tags=["Productos"])


@router.get("/", response_model=list[ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos los productos con paginacion."""
    return ProductoService.get_all(db, skip=skip, limit=limit)


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """Obtiene un producto por ID."""
    producto = ProductoService.get_by_id(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(data: ProductoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo producto."""
    return ProductoService.create(db, data)


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int, data: ProductoUpdate, db: Session = Depends(get_db)
):
    """Actualiza un producto existente."""
    return ProductoService.update(db, producto_id, data)


@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """Elimina un producto."""
    ProductoService.delete(db, producto_id)
