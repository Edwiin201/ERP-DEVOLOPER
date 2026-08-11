"""
Servicio para Ordenes de Trabajo.
Maneja transiciones de estado y calculo de duracion real.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException
from app.models.orden_trabajo import OrdenTrabajo
from app.schemas.orden_trabajo import OrdenTrabajoCreate, OrdenTrabajoUpdate


class OrdenTrabajoService:
    """CRUD + transiciones de estado para ordenes de trabajo."""

    @staticmethod
    def get_all(
        db: Session, skip: int = 0, limit: int = 100, estado: str | None = None
    ) -> list[OrdenTrabajo]:
        """Lista ordenes de trabajo con filtro opcional por estado."""
        stmt = select(OrdenTrabajo)
        if estado:
            stmt = stmt.where(OrdenTrabajo.estado == estado)
        stmt = stmt.offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_by_id(db: Session, orden_id: int) -> OrdenTrabajo | None:
        """Obtiene una orden de trabajo por ID."""
        return db.get(OrdenTrabajo, orden_id)

    @staticmethod
    def create(db: Session, data: OrdenTrabajoCreate) -> OrdenTrabajo:
        """Crea una orden de trabajo con estado 'pendiente' por defecto."""
        orden_data = data.model_dump()
        orden_data["estado"] = "pendiente"

        orden = OrdenTrabajo(**orden_data)
        db.add(orden)
        db.commit()
        db.refresh(orden)
        return orden

    @staticmethod
    def update(
        db: Session, orden_id: int, data: OrdenTrabajoUpdate
    ) -> OrdenTrabajo:
        """Actualiza una orden de trabajo."""
        orden = db.get(OrdenTrabajo, orden_id)
        if not orden:
            raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(orden, key, value)

        db.commit()
        db.refresh(orden)
        return orden

    @staticmethod
    def delete(db: Session, orden_id: int) -> bool:
        """Elimina una orden solo si esta en pendiente o cancelado."""
        orden = db.get(OrdenTrabajo, orden_id)
        if not orden:
            raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")

        if orden.estado not in ("pendiente", "cancelado"):
            raise HTTPException(
                status_code=400,
                detail=f"Solo se puede eliminar ordenes en estado 'pendiente' o 'cancelado' (actual: '{orden.estado}')",
            )

        db.delete(orden)
        db.commit()
        return True

    @staticmethod
    def iniciar(db: Session, orden_id: int) -> OrdenTrabajo:
        """Transicion: pendiente/listo -> en_proceso. Registra fecha_inicio."""
        orden = db.get(OrdenTrabajo, orden_id)
        if not orden:
            raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")

        if orden.estado not in ("pendiente", "listo"):
            raise HTTPException(
                status_code=400,
                detail=f"Solo se puede iniciar ordenes en estado 'pendiente' o 'listo' (actual: '{orden.estado}')",
            )

        orden.estado = "en_proceso"
        orden.fecha_inicio = datetime.now()
        db.commit()
        db.refresh(orden)
        return orden

    @staticmethod
    def terminar(db: Session, orden_id: int) -> OrdenTrabajo:
        """Transicion: en_proceso -> terminado. Calcula duracion_real."""
        orden = db.get(OrdenTrabajo, orden_id)
        if not orden:
            raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")

        if orden.estado != "en_proceso":
            raise HTTPException(
                status_code=400,
                detail=f"Solo se puede terminar ordenes en estado 'en_proceso' (actual: '{orden.estado}')",
            )

        orden.estado = "terminado"
        orden.fecha_fin = datetime.now()

        # Calcular duracion real en minutos
        if orden.fecha_inicio:
            delta = orden.fecha_fin - orden.fecha_inicio
            duracion_minutos = Decimal(str(delta.total_seconds() / 60))
            orden.duracion_real = duracion_minutos

        db.commit()
        db.refresh(orden)
        return orden

    @staticmethod
    def cancelar(db: Session, orden_id: int) -> OrdenTrabajo:
        """Transicion: cualquier estado (excepto terminado) -> cancelado."""
        orden = db.get(OrdenTrabajo, orden_id)
        if not orden:
            raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")

        if orden.estado == "terminado":
            raise HTTPException(
                status_code=400,
                detail="No se puede cancelar una orden ya terminada",
            )

        orden.estado = "cancelado"
        db.commit()
        db.refresh(orden)
        return orden
