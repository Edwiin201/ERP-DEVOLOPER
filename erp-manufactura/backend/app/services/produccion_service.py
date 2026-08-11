"""
Servicio para Producciones.
Maneja transiciones de estado y generacion automatica de nombre.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime
from fastapi import HTTPException
from app.models.produccion import Produccion
from app.schemas.produccion import ProduccionCreate, ProduccionUpdate


class ProduccionService:
    """CRUD + transiciones de estado para producciones."""

    @staticmethod
    def get_all(
        db: Session, skip: int = 0, limit: int = 100, estado: str | None = None
    ) -> list[Produccion]:
        """Lista producciones con filtro opcional por estado."""
        stmt = select(Produccion)
        if estado:
            stmt = stmt.where(Produccion.estado == estado)
        stmt = stmt.offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_by_id(db: Session, produccion_id: int) -> Produccion | None:
        """Obtiene una produccion por ID."""
        return db.get(Produccion, produccion_id)

    @staticmethod
    def _generar_nombre(db: Session) -> str:
        """Genera nombre automatico tipo 'MO-00001' basado en el count actual."""
        stmt = select(func.count(Produccion.id))
        total = db.scalar(stmt) or 0
        secuencia = total + 1
        return f"MO-{secuencia:05d}"

    @staticmethod
    def create(db: Session, data: ProduccionCreate) -> Produccion:
        """Crea una produccion con nombre auto-generado."""
        nombre = ProduccionService._generar_nombre(db)
        produccion_data = data.model_dump()
        produccion_data["nombre"] = nombre
        produccion_data["estado"] = "borrador"

        produccion = Produccion(**produccion_data)
        db.add(produccion)
        db.commit()
        db.refresh(produccion)
        return produccion

    @staticmethod
    def update(
        db: Session, produccion_id: int, data: ProduccionUpdate
    ) -> Produccion:
        """Actualiza una produccion. No permite modificar si esta terminada/cancelada."""
        produccion = db.get(Produccion, produccion_id)
        if not produccion:
            raise HTTPException(status_code=404, detail="Produccion no encontrada")

        if produccion.estado in ("terminado", "cancelado"):
            raise HTTPException(
                status_code=400,
                detail=f"No se puede editar una produccion en estado '{produccion.estado}'",
            )

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(produccion, key, value)

        db.commit()
        db.refresh(produccion)
        return produccion

    @staticmethod
    def delete(db: Session, produccion_id: int) -> bool:
        """Elimina una produccion solo si esta en borrador o cancelado."""
        produccion = db.get(Produccion, produccion_id)
        if not produccion:
            raise HTTPException(status_code=404, detail="Produccion no encontrada")

        if produccion.estado not in ("borrador", "cancelado"):
            raise HTTPException(
                status_code=400,
                detail=f"Solo se puede eliminar producciones en estado 'borrador' o 'cancelado' (actual: '{produccion.estado}')",
            )

        db.delete(produccion)
        db.commit()
        return True

    @staticmethod
    def confirmar(db: Session, produccion_id: int) -> Produccion:
        """Transicion: borrador -> confirmado."""
        produccion = db.get(Produccion, produccion_id)
        if not produccion:
            raise HTTPException(status_code=404, detail="Produccion no encontrada")

        if produccion.estado != "borrador":
            raise HTTPException(
                status_code=400,
                detail=f"Solo se puede confirmar producciones en estado 'borrador' (actual: '{produccion.estado}')",
            )

        produccion.estado = "confirmado"
        db.commit()
        db.refresh(produccion)
        return produccion

    @staticmethod
    def iniciar(db: Session, produccion_id: int) -> Produccion:
        """Transicion: confirmado -> en_proceso. Registra fecha_inicio."""
        produccion = db.get(Produccion, produccion_id)
        if not produccion:
            raise HTTPException(status_code=404, detail="Produccion no encontrada")

        if produccion.estado != "confirmado":
            raise HTTPException(
                status_code=400,
                detail=f"Solo se puede iniciar producciones en estado 'confirmado' (actual: '{produccion.estado}')",
            )

        produccion.estado = "en_proceso"
        produccion.fecha_inicio = datetime.now()
        db.commit()
        db.refresh(produccion)
        return produccion

    @staticmethod
    def terminar(db: Session, produccion_id: int) -> Produccion:
        """Transicion: en_proceso -> terminado. Registra fecha_fin."""
        produccion = db.get(Produccion, produccion_id)
        if not produccion:
            raise HTTPException(status_code=404, detail="Produccion no encontrada")

        if produccion.estado != "en_proceso":
            raise HTTPException(
                status_code=400,
                detail=f"Solo se puede terminar producciones en estado 'en_proceso' (actual: '{produccion.estado}')",
            )

        produccion.estado = "terminado"
        produccion.fecha_fin = datetime.now()
        db.commit()
        db.refresh(produccion)
        return produccion

    @staticmethod
    def cancelar(db: Session, produccion_id: int) -> Produccion:
        """Transicion: cualquier estado (excepto terminado/cancelado) -> cancelado."""
        produccion = db.get(Produccion, produccion_id)
        if not produccion:
            raise HTTPException(status_code=404, detail="Produccion no encontrada")

        if produccion.estado in ("terminado", "cancelado"):
            raise HTTPException(
                status_code=400,
                detail=f"No se puede cancelar una produccion en estado '{produccion.estado}'",
            )

        produccion.estado = "cancelado"
        db.commit()
        db.refresh(produccion)
        return produccion
