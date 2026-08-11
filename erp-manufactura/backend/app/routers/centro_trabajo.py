"""
Endpoints API REST para Centros de Trabajo.
Operaciones CRUD basicas.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.centro_trabajo import (
    CentroTrabajoCreate,
    CentroTrabajoUpdate,
    CentroTrabajoResponse,
)
from app.services.centro_trabajo_service import CentroTrabajoService

router = APIRouter(prefix="/api/centros-trabajo", tags=["Centros de Trabajo"])


@router.get("/", response_model=list[CentroTrabajoResponse])
def listar_centros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos los centros de trabajo con paginacion."""
    return CentroTrabajoService.get_all(db, skip=skip, limit=limit)


@router.get("/{centro_id}", response_model=CentroTrabajoResponse)
def obtener_centro(centro_id: int, db: Session = Depends(get_db)):
    """Obtiene un centro de trabajo por ID."""
    centro = CentroTrabajoService.get_by_id(db, centro_id)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro de trabajo no encontrado")
    return centro


@router.post("/", response_model=CentroTrabajoResponse, status_code=201)
def crear_centro(data: CentroTrabajoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo centro de trabajo."""
    return CentroTrabajoService.create(db, data)


@router.put("/{centro_id}", response_model=CentroTrabajoResponse)
def actualizar_centro(
    centro_id: int, data: CentroTrabajoUpdate, db: Session = Depends(get_db)
):
    """Actualiza un centro de trabajo existente."""
    return CentroTrabajoService.update(db, centro_id, data)


@router.delete("/{centro_id}", status_code=204)
def eliminar_centro(centro_id: int, db: Session = Depends(get_db)):
    """Elimina un centro de trabajo (solo si no tiene ordenes activas)."""
    CentroTrabajoService.delete(db, centro_id)
