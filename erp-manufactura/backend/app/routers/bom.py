"""
Endpoints API REST para BOMs (Listas de Materiales).
Incluye endpoints para activar/archivar.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.bom import BOMCreate, BOMUpdate, BOMResponse
from app.services.bom_service import BOMService

router = APIRouter(prefix="/api/boms", tags=["BOMs"])


@router.get("/", response_model=list[BOMResponse])
def listar_boms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos los BOMs con paginacion."""
    return BOMService.get_all(db, skip=skip, limit=limit)


@router.get("/next-code")
def siguiente_codigo_bom(db: Session = Depends(get_db)):
    """Retorna el proximo codigo que se generara para un nuevo BOM."""
    return {"codigo": BOMService._generar_codigo(db)}


@router.get("/{bom_id}", response_model=BOMResponse)
def obtener_bom(bom_id: int, db: Session = Depends(get_db)):
    """Obtiene un BOM por ID incluyendo sus lineas."""
    bom = BOMService.get_by_id(db, bom_id)
    if not bom:
        raise HTTPException(status_code=404, detail="BOM no encontrado")
    return bom


@router.post("/", response_model=BOMResponse, status_code=201)
def crear_bom(data: BOMCreate, db: Session = Depends(get_db)):
    """Crea un nuevo BOM con sus lineas."""
    return BOMService.create(db, data)


@router.put("/{bom_id}", response_model=BOMResponse)
def actualizar_bom(bom_id: int, data: BOMUpdate, db: Session = Depends(get_db)):
    """Actualiza un BOM y sincroniza sus lineas."""
    return BOMService.update(db, bom_id, data)


@router.delete("/{bom_id}", status_code=204)
def eliminar_bom(bom_id: int, db: Session = Depends(get_db)):
    """Elimina un BOM (solo si no esta en uso por producciones activas)."""
    BOMService.delete(db, bom_id)


@router.post("/{bom_id}/activar", response_model=BOMResponse)
def activar_bom(bom_id: int, db: Session = Depends(get_db)):
    """Cambia el estado del BOM a 'activo'."""
    return BOMService.activar(db, bom_id)


@router.post("/{bom_id}/archivar", response_model=BOMResponse)
def archivar_bom(bom_id: int, db: Session = Depends(get_db)):
    """Cambia el estado del BOM a 'archivado'."""
    return BOMService.archivar(db, bom_id)
