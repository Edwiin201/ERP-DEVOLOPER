"""
Endpoints API REST para Ordenes de Trabajo.
Incluye endpoints para transiciones de estado.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.orden_trabajo import (
    OrdenTrabajoCreate,
    OrdenTrabajoUpdate,
    OrdenTrabajoResponse,
)
from app.services.orden_trabajo_service import OrdenTrabajoService

router = APIRouter(prefix="/api/ordenes-trabajo", tags=["Ordenes de Trabajo"])


@router.get("/", response_model=list[OrdenTrabajoResponse])
def listar_ordenes(
    skip: int = 0, limit: int = 100, estado: str | None = None, db: Session = Depends(get_db)
):
    """Lista todas las ordenes de trabajo con filtro opcional por estado."""
    return OrdenTrabajoService.get_all(db, skip=skip, limit=limit, estado=estado)


@router.get("/next-code")
def siguiente_codigo_orden(db: Session = Depends(get_db)):
    """Retorna el proximo codigo que se generara para una nueva orden."""
    return {"codigo": OrdenTrabajoService._generar_nombre(db)}


@router.get("/{orden_id}", response_model=OrdenTrabajoResponse)
def obtener_orden(orden_id: int, db: Session = Depends(get_db)):
    """Obtiene una orden de trabajo por ID."""
    orden = OrdenTrabajoService.get_by_id(db, orden_id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")
    return orden


@router.post("/", response_model=OrdenTrabajoResponse, status_code=201)
def crear_orden(data: OrdenTrabajoCreate, db: Session = Depends(get_db)):
    """Crea una nueva orden de trabajo."""
    return OrdenTrabajoService.create(db, data)


@router.put("/{orden_id}", response_model=OrdenTrabajoResponse)
def actualizar_orden(
    orden_id: int, data: OrdenTrabajoUpdate, db: Session = Depends(get_db)
):
    """Actualiza una orden de trabajo existente."""
    return OrdenTrabajoService.update(db, orden_id, data)


@router.delete("/{orden_id}", status_code=204)
def eliminar_orden(orden_id: int, db: Session = Depends(get_db)):
    """Elimina una orden (solo si esta en pendiente o cancelado)."""
    OrdenTrabajoService.delete(db, orden_id)


@router.post("/{orden_id}/iniciar", response_model=OrdenTrabajoResponse)
def iniciar_orden(orden_id: int, db: Session = Depends(get_db)):
    """Transicion: pendiente/listo -> en_proceso."""
    return OrdenTrabajoService.iniciar(db, orden_id)


@router.post("/{orden_id}/terminar", response_model=OrdenTrabajoResponse)
def terminar_orden(orden_id: int, db: Session = Depends(get_db)):
    """Transicion: en_proceso -> terminado. Calcula duracion_real."""
    return OrdenTrabajoService.terminar(db, orden_id)


@router.post("/{orden_id}/cancelar", response_model=OrdenTrabajoResponse)
def cancelar_orden(orden_id: int, db: Session = Depends(get_db)):
    """Transicion: cualquier estado -> cancelado."""
    return OrdenTrabajoService.cancelar(db, orden_id)
