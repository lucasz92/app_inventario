#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para insertar datos de ejemplo en la base de datos
"""

import sqlite3
import os
from data.database import conectar_db, crear_tablas

def insertar_datos_ejemplo():
    """Inserta datos de ejemplo en la base de datos."""
    
    # Asegurar que las tablas existen
    crear_tablas()
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        # Limpiar datos existentes (opcional)
        print("🧹 Limpiando datos existentes...")
        cursor.execute("DELETE FROM producto_ubicacion")
        cursor.execute("DELETE FROM alertas")
        cursor.execute("DELETE FROM ubicaciones")
        cursor.execute("DELETE FROM productos")
        
        # Insertar productos de ejemplo
        print("📦 Insertando productos de ejemplo...")
        productos = [
            ("TORN001", "Tornillo Phillips M6x20", "Ferretería", "Ferretería Central", "Taller Mecánico", 500, "unidad", "manual", 50, 1000, "Tornillos estándar para uso general"),
            ("TURC001", "Tuerca hexagonal M6", "Ferretería", "Ferretería Central", "Taller Mecánico", 300, "unidad", "manual", 30, 600, "Tuercas galvanizadas"),
            ("CABL001", "Cable eléctrico 2.5mm", "Eléctrico", "ElectroSur", "Taller Eléctrico", 1000, "metro", "automático", 100, 2000, "Cable para instalaciones domiciliarias"),
            ("INTE001", "Interruptor simple 10A", "Eléctrico", "ElectroSur", "Taller Eléctrico", 75, "unidad", "manual", 10, 150, "Interruptores para uso doméstico"),
            ("PINT001", "Pintura látex blanca 4L", "Pintura", "Pinturas del Norte", "Almacén General", 25, "litro", "manual", 5, 50, "Pintura interior lavable"),
            ("RODI001", "Rodillo lana 23cm", "Pintura", "Pinturas del Norte", "Almacén General", 40, "unidad", "manual", 8, 80, "Rodillos para pintura látex"),
            ("TALA001", "Taladro percutor 800W", "Herramientas", "Herramientas Pro", "Taller Mecánico", 8, "unidad", "manual", 2, 15, "Taladros profesionales con percutor"),
            ("BROC001", "Broca HSS 8mm", "Herramientas", "Herramientas Pro", "Taller Mecánico", 50, "unidad", "manual", 10, 100, "Brocas para metal alta velocidad"),
            ("SOLD001", "Soldadura E6013 3.2mm", "Soldadura", "Soldaduras Técnicas", "Taller Soldadura", 200, "kilogramo", "automático", 20, 400, "Electrodos para soldadura general"),
            ("DISC001", "Disco corte metal 115mm", "Herramientas", "Herramientas Pro", "Taller Mecánico", 120, "unidad", "manual", 20, 250, "Discos para amoladora angular"),
            ("ACEI001", "Aceite hidráulico ISO 68", "Lubricantes", "Lubricantes Industriales", "Almacén Químicos", 80, "litro", "automático", 15, 150, "Aceite para sistemas hidráulicos"),
            ("FILT001", "Filtro de aire K&N", "Filtros", "Repuestos Automotor", "Taller Automotriz", 25, "unidad", "manual", 5, 50, "Filtros de aire de alto rendimiento")
        ]
        
        cursor.executemany("""
            INSERT INTO productos (
                codigo, descripcion, categoria, proveedor, puesto_trabajo,
                stock_actual, unidad_medida, tipo_control, stock_minimo, 
                stock_maximo, observacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, productos)
        
        # Insertar ubicaciones de ejemplo
        print("📍 Insertando ubicaciones de ejemplo...")
        ubicaciones = [
            (1, "A", 1, 1, "NORTE", "DEP01", "PAÑOL 1"),
            (1, "A", 1, 2, "SUR", "DEP01", "PAÑOL 1"),
            (1, "A", 2, 1, "ESTE", "DEP01", "PAÑOL 1"),
            (1, "B", 1, 1, "OESTE", "DEP01", "PAÑOL 2"),
            (1, "B", 1, 2, "NORTE", "DEP01", "PAÑOL 2"),
            (1, "B", 2, 1, "SUR", "DEP01", "PAÑOL 2"),
            (2, "A", 1, 1, "ESTE", "DEP02", "PAÑOL 1"),
            (2, "A", 1, 2, "OESTE", "DEP02", "PAÑOL 1"),
            (2, "A", 2, 1, "NORTE", "DEP02", "PAÑOL 1"),
            (2, "B", 1, 1, "SUR", "DEP02", "PAÑOL 2"),
            (2, "B", 2, 1, "ESTE", "DEP02", "PAÑOL 2"),
            (3, "A", 1, 1, "OESTE", "DEP02", "PAÑOL 2")
        ]
        
        cursor.executemany("""
            INSERT INTO ubicaciones (fila, columna, estante, posicion, orientacion, deposito, sector)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ubicaciones)
        
        # Insertar relaciones producto-ubicación
        print("🔗 Insertando relaciones producto-ubicación...")
        producto_ubicaciones = [
            ("TORN001", 1, 500),
            ("TURC001", 2, 300),
            ("CABL001", 3, 1000),
            ("INTE001", 4, 75),
            ("PINT001", 5, 25),
            ("RODI001", 6, 40),
            ("TALA001", 7, 8),
            ("BROC001", 8, 50),
            ("SOLD001", 9, 200),
            ("DISC001", 10, 120),
            ("ACEI001", 11, 80),
            ("FILT001", 12, 25)
        ]
        
        cursor.executemany("""
            INSERT INTO producto_ubicacion (codigo_producto, id_ubicacion, cantidad)
            VALUES (?, ?, ?)
        """, producto_ubicaciones)
        
        # Insertar alertas de ejemplo
        print("⚠️ Insertando alertas de ejemplo...")
        alertas = [
            ("TORN001", 1, "Media", "Stock bajo", "El stock está por debajo del nivel recomendado", "sin iniciar", "2024-01-15 10:30:00"),
            ("PINT001", 5, "Alta prioridad", "Producto vencido", "Revisar fecha de vencimiento del lote actual", "en progreso", "2024-01-16 14:20:00"),
            ("TALA001", 7, "Baja", "Mantenimiento", "Programar mantenimiento preventivo de herramientas", "sin iniciar", "2024-01-17 09:15:00"),
            ("CABL001", 3, "Alta prioridad", "Reposición urgente", "Stock crítico para proyecto en curso", "sin iniciar", "2024-01-18 08:00:00"),
            ("ACEI001", 11, "Media", "Control de calidad", "Verificar viscosidad del lote actual", "en progreso", "2024-01-19 11:45:00")
        ]
        
        cursor.executemany("""
            INSERT INTO alertas (codigo_producto, id_ubicacion, tipo_alerta, razon, detalles, estado, fecha_inicio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, alertas)
        
        conn.commit()
        
        # Mostrar estadísticas
        cursor.execute("SELECT COUNT(*) FROM productos")
        total_productos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ubicaciones")
        total_ubicaciones = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM alertas")
        total_alertas = cursor.fetchone()[0]
        
        print("\n✅ Datos de ejemplo insertados correctamente!")
        print(f"📦 Productos: {total_productos}")
        print(f"📍 Ubicaciones: {total_ubicaciones}")
        print(f"⚠️ Alertas: {total_alertas}")
        print(f"🔗 Relaciones producto-ubicación: {len(producto_ubicaciones)}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al insertar datos: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    insertar_datos_ejemplo()