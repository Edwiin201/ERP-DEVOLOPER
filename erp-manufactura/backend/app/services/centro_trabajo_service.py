"""
Servicio para Centros de Trabajo.
Contiene toda la logica de negocio y validaciones.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.models.centro_trabajo import CentroTrabajo
from app.schemas.centro_trabajo import CentroTrabajoCreate, CentroTrabajoUpdate


class CentroTrabajoService:
    """CRUD + validaciones para centros de trabajo."""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[CentroTrabajo]:
        """Lista todos los centros de trabajo con paginacion."""
        stmt = select(CentroTrabajo).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_by_id(db: Session, centro_id: int) -> CentroTrabajo | None:
        """Obtiene un centro de trabajo por ID."""
        return db.get(CentroTrabajo, centro_id)

    @staticmethod
    def create(db: Session, data: CentroTrabajoCreate) -> CentroTrabajo:
        """Crea un nuevo centro de trabajo validando codigo unico."""
        # Verificar que el codigo no exista
        stmt = select(CentroTrabajo).where(CentroTrabajo.codigo == data.codigo)
        existing = db.scalar(stmt)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un centro de trabajo con codigo '{data.codigo}'",
            )

        centro = CentroTrabajo(**data.model_dump())
        db.add(centro)
        db.commit()
        db.refresh(centro)
        return centro

    @staticmethod
    def update(
        db: Session, centro_id: int, data: CentroTrabajoUpdate
    ) -> CentroTrabajo:
        """Actualiza un centro de trabajo validando unicidad de codigo."""
        centro = db.get(CentroTrabajo, centro_id)
        if not centro:
            raise HTTPException(status_code=404, detail="Centro de trabajo no encontrado")

        # Si cambia el codigo, verificar que no exista otro con ese codigo
        if data.codigo is not None and data.codigo != centro.codigo:
            stmt = select(CentroTrabajo).where(CentroTrabajo.codigo == data.codigo)
            existing = db.scalar(stmt)
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe un centro de trabajo con codigo '{data.codigo}'",
                )

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(centro, key, value)

        db.commit()
        db.refresh(centro)
        return centro

    @staticmethod
    def delete(db: Session, centro_id: int) -> bool:
        """Elimina un centro solo si no tiene ordenes de trabajo activas."""
        centro = db.get(CentroTrabajo, centro_id)
        if not centro:
            raise HTTPException(status_code=404, detail="Centro de trabajo no encontrado")

        # Verificar que no tenga ordenes activas
        if centro.ordenes_trabajo:
            activas = [
                ot
                for ot in centro.ordenes_trabajo
                if ot.estado not in ("terminado", "cancelado")
            ]
            if activas:
                raise HTTPException(
                    status_code=400,
                    detail="No se puede eliminar: tiene ordenes de trabajo activas",
                )

        db.delete(centro)
        db.commit()
        return True
