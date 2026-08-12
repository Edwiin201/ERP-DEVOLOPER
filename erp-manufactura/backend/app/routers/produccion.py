"""
Endpoints API REST para Producciones.
Incluye endpoints para transiciones de estado.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.produccion import (
    ProduccionCreate,
    ProduccionUpdate,
    ProduccionResponse,
)
from app.services.produccion_service import ProduccionService

router = APIRouter(prefix="/api/producciones", tags=["Producciones"])


@router.get("/", response_model=list[ProduccionResponse])
def listar_producciones(
    skip: int = 0, limit: int = 100, estado: str | None = None, db: Session = Depends(get_db)
):
    """Lista todas las producciones con filtro opcional por estado."""
    return ProduccionService.get_all(db, skip=skip, limit=limit, estado=estado)


@router.get("/next-code")
def siguiente_codigo_produccion(db: Session = Depends(get_db)):
    """Retorna el proximo codigo que se generara para una nueva produccion."""
    return {"codigo": ProduccionService._generar_nombre(db)}


@router.get("/{produccion_id}", response_model=ProduccionResponse)
def obtener_produccion(produccion_id: int, db: Session = Depends(get_db)):
    """Obtiene una produccion por ID."""
    produccion = ProduccionService.get_by_id(db, produccion_id)
    if not produccion:
        raise HTTPException(status_code=404, detail="Produccion no encontrada")
    return produccion


@router.post("/", response_model=ProduccionResponse, status_code=201)
def crear_produccion(data: ProduccionCreate, db: Session = Depends(get_db)):
    """Crea una nueva produccion con nombre auto-generado."""
    return ProduccionService.create(db, data)


@router.put("/{produccion_id}", response_model=ProduccionResponse)
def actualizar_produccion(
    produccion_id: int, data: ProduccionUpdate, db: Session = Depends(get_db)
):
    """Actualiza una produccion existente."""
    return ProduccionService.update(db, produccion_id, data)


@router.delete("/{produccion_id}", status_code=204)
def eliminar_produccion(produccion_id: int, db: Session = Depends(get_db)):
    """Elimina una produccion (solo si esta en borrador o cancelado)."""
    ProduccionService.delete(db, produccion_id)


@router.post("/{produccion_id}/confirmar", response_model=ProduccionResponse)
def confirmar_produccion(produccion_id: int, db: Session = Depends(get_db)):
    """Transicion: borrador -> confirmado."""
    return ProduccionService.confirmar(db, produccion_id)


@router.post("/{produccion_id}/iniciar", response_model=ProduccionResponse)
def iniciar_produccion(produccion_id: int, db: Session = Depends(get_db)):
    """Transicion: confirmado -> en_proceso."""
    return ProduccionService.iniciar(db, produccion_id)


@router.post("/{produccion_id}/terminar", response_model=ProduccionResponse)
def terminar_produccion(produccion_id: int, db: Session = Depends(get_db)):
    """Transicion: en_proceso -> terminado."""
    return ProduccionService.terminar(db, produccion_id)


@router.post("/{produccion_id}/cancelar", response_model=ProduccionResponse)
def cancelar_produccion(produccion_id: int, db: Session = Depends(get_db)):
    """Transicion: cualquier estado -> cancelado."""
    return ProduccionService.cancelar(db, produccion_id)
