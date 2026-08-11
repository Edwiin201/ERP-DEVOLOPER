-- ============================================
-- ERP Manufactura - Schema PostgreSQL
-- ============================================
-- Tablas para gestion de produccion, BOMs,
-- ordenes de trabajo y centros de trabajo.
-- ============================================

-- 1. Centros de Trabajo
CREATE TABLE centros_trabajo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    capacidad DECIMAL(10,2) DEFAULT 1.0,
    costo_hora DECIMAL(10,2) DEFAULT 0.0,
    activo BOOLEAN DEFAULT TRUE,
    notas TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. BOMs (Listas de Materiales)
CREATE TABLE boms (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50),
    nombre VARCHAR(200) NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad DECIMAL(10,2) DEFAULT 1.0,
    producto_uom VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'activo',
    company_id INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 3. Lineas de BOM
CREATE TABLE bom_lineas (
    id SERIAL PRIMARY KEY,
    bom_id INTEGER REFERENCES boms(id) ON DELETE CASCADE,
    producto_id INTEGER NOT NULL,
    cantidad DECIMAL(10,2) DEFAULT 1.0,
    producto_uom VARCHAR(50),
    secuencia INTEGER DEFAULT 10
);

-- 4. Producciones
CREATE TABLE producciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL DEFAULT 1.0,
    producto_uom VARCHAR(50),
    bom_id INTEGER REFERENCES boms(id),
    centro_trabajo_id INTEGER REFERENCES centros_trabajo(id),
    fecha_inicio TIMESTAMP,
    fecha_fin TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'borrador',
    notas TEXT,
    company_id INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 5. Ordenes de Trabajo
CREATE TABLE ordenes_trabajo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    produccion_id INTEGER REFERENCES producciones(id) ON DELETE CASCADE,
    centro_trabajo_id INTEGER REFERENCES centros_trabajo(id),
    estado VARCHAR(20) DEFAULT 'pendiente',
    duracion_esperada DECIMAL(10,2),
    duracion_real DECIMAL(10,2),
    fecha_inicio TIMESTAMP,
    fecha_fin TIMESTAMP,
    secuencia INTEGER DEFAULT 10,
    notas TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indices para busquedas frecuentes
CREATE INDEX idx_boms_estado ON boms(estado);
CREATE INDEX idx_boms_producto ON boms(producto_id);
CREATE INDEX idx_bom_lineas_bom ON bom_lineas(bom_id);
CREATE INDEX idx_producciones_estado ON producciones(estado);
CREATE INDEX idx_producciones_bom ON producciones(bom_id);
CREATE INDEX idx_producciones_centro ON producciones(centro_trabajo_id);
CREATE INDEX idx_ordenes_produccion ON ordenes_trabajo(produccion_id);
CREATE INDEX idx_ordenes_centro ON ordenes_trabajo(centro_trabajo_id);
CREATE INDEX idx_ordenes_estado ON ordenes_trabajo(estado);

-- Trigger para actualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_centros_trabajo_updated_at
    BEFORE UPDATE ON centros_trabajo
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_boms_updated_at
    BEFORE UPDATE ON boms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_producciones_updated_at
    BEFORE UPDATE ON producciones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ordenes_trabajo_updated_at
    BEFORE UPDATE ON ordenes_trabajo
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
