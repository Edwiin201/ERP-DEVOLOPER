"""
Entry point de la aplicacion FastAPI.
Configura CORS, routers y endpoints de salud.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import (
    centro_trabajo_router,
    bom_router,
    produccion_router,
    orden_trabajo_router,
)

settings = get_settings()

# Crear aplicacion FastAPI
app = FastAPI(
    title="ERP Manufactura",
    description="Sistema CRUD de manufactura inspirado en MRP de Odoo",
    version="1.0.0",
)

# Configurar CORS para permitir requests del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(centro_trabajo_router)
app.include_router(bom_router)
app.include_router(produccion_router)
app.include_router(orden_trabajo_router)


@app.get("/health")
def health_check():
    """Endpoint de verificacion de salud."""
    return {"status": "ok", "version": "1.0.0"}
