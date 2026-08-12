"""
Servicio para BOMs (Listas de Materiales).
Manja creacion/actualizacion con lineas anidadas en transaccion.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from fastapi import HTTPException
from app.models.bom import BOM, BOMLinea
from app.models.produccion import Produccion
from app.schemas.bom import BOMCreate, BOMUpdate


class BOMService:
    """CRUD + activar/archivar para BOMs."""

    @staticmethod
    def _generar_codigo(db: Session) -> str:
        """Genera codigo automatico tipo 'BOM-00001' basado en el count actual."""
        stmt = select(func.count(BOM.id))
        total = db.scalar(stmt) or 0
        secuencia = total + 1
        return f"BOM-{secuencia:05d}"

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[BOM]:
        """Lista todos los BOMs con paginacion."""
        stmt = select(BOM).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_by_id(db: Session, bom_id: int) -> BOM | None:
        """Obtiene un BOM por ID con sus lineas precargadas."""
        return db.get(BOM, bom_id)

    @staticmethod
    def create(db: Session, data: BOMCreate) -> BOM:
        """Crea un BOM con codigo auto-generado y sus lineas en una transaccion."""
        codigo = BOMService._generar_codigo(db)
        bom_data = data.model_dump(exclude={"lineas"})
        bom_data["codigo"] = codigo
        bom = BOM(**bom_data)
        db.add(bom)
        db.flush()  # Obtener ID del BOM

        # Crear las lineas
        for linea_data in data.lineas:
            linea = BOMLinea(bom_id=bom.id, **linea_data.model_dump())
            db.add(linea)

        db.commit()
        db.refresh(bom)
        return bom

    @staticmethod
    def update(db: Session, bom_id: int, data: BOMUpdate) -> BOM:
        """Actualiza un BOM y sincroniza sus lineas."""
        bom = db.get(BOM, bom_id)
        if not bom:
            raise HTTPException(status_code=404, detail="BOM no encontrado")

        # Actualizar campos del BOM
        update_data = data.model_dump(exclude_unset=True, exclude={"lineas"})
        for key, value in update_data.items():
            setattr(bom, key, value)

        # Si se proporcionan lineas nuevas, reemplazar las existentes
        if data.lineas is not None:
            # Eliminar lineas actuales
            for linea in bom.lineas:
                db.delete(linea)
            db.flush()

            # Crear nuevas lineas
            for linea_data in data.lineas:
                linea = BOMLinea(bom_id=bom.id, **linea_data.model_dump())
                db.add(linea)

        db.commit()
        db.refresh(bom)
        return bom

    @staticmethod
    def delete(db: Session, bom_id: int) -> bool:
        """Elimina un BOM solo si no esta en uso por producciones activas."""
        bom = db.get(BOM, bom_id)
        if not bom:
            raise HTTPException(status_code=404, detail="BOM no encontrado")

        # Verificar que no este referenciado por producciones activas
        stmt = select(Produccion).where(
            Produccion.bom_id == bom_id,
            Produccion.estado.in_(["confirmado", "en_proceso"]),
        )
        producciones_activas = db.scalars(stmt).all()
        if producciones_activas:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar: esta en uso por producciones activas",
            )

        db.delete(bom)
        db.commit()
        return True

    @staticmethod
    def activar(db: Session, bom_id: int) -> BOM:
        """Cambia el estado del BOM a 'activo'."""
        bom = db.get(BOM, bom_id)
        if not bom:
            raise HTTPException(status_code=404, detail="BOM no encontrado")

        bom.estado = "activo"
        db.commit()
        db.refresh(bom)
        return bom

    @staticmethod
    def archivar(db: Session, bom_id: int) -> BOM:
        """Cambia el estado del BOM a 'archivado'."""
        bom = db.get(BOM, bom_id)
        if not bom:
            raise HTTPException(status_code=404, detail="BOM no encontrado")

        bom.estado = "archivado"
        db.commit()
        db.refresh(bom)
        return bom
