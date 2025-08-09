import sqlite3
import os
from openpyxl import load_workbook, workbook

def crear_tablas():
    ruta = os.path.join("data", "inventario.db")
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
            codigo TEXT PRIMARY KEY,
            descripcion TEXT,
            proveedor TEXT,
            tipo TEXT, -- si es o no max/min
            maxmin TEXT, -- cantidad de maxmin
            categoria TEXT,
            puesto TEXT,
            observacion TEXT
        );
    """)

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS ubicacion (
            fk_codigo TEXT NOT NULL, -- viene desde 'producto'
            fila TEXT,
            columna TEXT,
            estante TEXT,
            deposito TEXT,
            sector TEXT,
            ubicacion TEXT,
            PRIMARY KEY (fk_codigo, fila, columna, estante, deposito, sector, ubicacion),
            FOREIGN KEY (fk_codigo) REFERENCES producto(codigo)
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            fk_codigo TEXT NOT NULL,
            fila TEXT,
            columna TEXT,
            estante TEXT,
            deposito TEXT,
            sector TEXT,
            ubicacion TEXT,
            fecha_inicio TIMESTAMP,
            fecha_fin TIMESTAMP,
            razon TEXT,
            accion TEXT,
            PRIMARY KEY (fk_codigo, fila, columna, estante, deposito, sector, ubicacion),
            FOREIGN KEY (fk_codigo, fila, columna, estante, deposito, sector, ubicacion)
                REFERENCES ubicacion (fk_codigo, fila, columna, estante, deposito, sector, ubicacion)
        );
    """)
    conexion.commit()
    conexion.close()
    
def inicializar_db():
    ruta = os.path.join("data", "inventario.db")
    if not os.path.exists(ruta):
        print("📦 Base de datos no encontrada. Creando...")
        crear_tablas()
    else:
        print("✅ Base de datos ya existe.")
            
def conectar_db():
    ruta = os.path.join("data", "inventario.db")
    conexion = sqlite3.connect(ruta)
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion

""" FUNCIONES PARA TAB_PRODUCTOS """

def buscar_productos(texto: str) -> list[tuple]:
    conn = conectar_db()
    cursor = conn.cursor()
    query = """
        SELECT p.codigo, p.descripcion, u.fila, u.columna, u.estante, u.ubicacion, u.deposito, u.sector
        FROM producto p
        JOIN ubicacion u ON p.codigo = u.fk_codigo
        WHERE
            p.codigo LIKE ?
            OR p.descripcion LIKE ?
            OR u.deposito LIKE ?
            OR u.sector LIKE ?
            OR p.puesto LIKE ?
        ORDER BY p.codigo;
    """
    like_text = f"%{texto}%"
    cursor.execute(query, (like_text,) * 5)
    resultados = cursor.fetchall()
    conn.close()
    return resultados



def obtener_productos_con_ubicacion():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            p.codigo,
            p.descripcion,
            u.fila,
            u.columna,
            u.estante,
            u.ubicacion,
            u.deposito,
            u.sector
        FROM producto p
        JOIN ubicacion u ON p.codigo = u.fk_codigo
        ORDER BY p.codigo;
    """)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def obtener_detalles_producto(codigo):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            proveedor,
            tipo,
            maxmin,
            categoria,
            puesto,
            observacion
        FROM producto
        WHERE codigo = ?;
    """, (codigo,))
    detalles = cursor.fetchone()
    conexion.close()
    return detalles

def exportar_a_excel(ruta_archivo):
    conn = conectar_db()
    cursor = conn.cursor()

    wb = Workbook()
    ws_productos = wb.active
    ws_productos.title = "producto"

    cursor.execute("SELECT * FROM producto")
    columnas = [desc[0] for desc in cursor.description]
    ws_productos.append(columnas)
    for fila in cursor.fetchall():
        ws_productos.append(fila)

    ws_ubicacion = wb.create_sheet(title="ubicacion")
    cursor.execute("SELECT * FROM ubicacion")
    columnas = [desc[0] for desc in cursor.description]
    ws_ubicacion.append(columnas)
    for fila in cursor.fetchall():
        ws_ubicacion.append(fila)

    wb.save(ruta_archivo)
    conn.close()
    
def importar_desde_excel(ruta_archivo):
    conn = conectar_db()
    cursor = conn.cursor()
    wb = load_workbook(ruta_archivo)
    hojas_faltantes = []

    for nombre_hoja in ["producto", "ubicacion"]:
        if nombre_hoja not in wb.sheetnames:
            hojas_faltantes.append(nombre_hoja)
            continue

        ws = wb[nombre_hoja]
        filas = list(ws.iter_rows(values_only=True))
        if not filas:
            continue

        columnas = filas[0]
        columnas_db = obtener_columnas_tabla(cursor, nombre_hoja)

        if set(columnas) != set(columnas_db):
            print(f"⚠️ Las columnas de la hoja '{nombre_hoja}' no coinciden con la tabla.")
            continue

        for fila in filas[1:]:
            if nombre_hoja == "ubicacion":
                fk_codigo = fila[columnas.index("fk_codigo")]
                cursor.execute("SELECT 1 FROM producto WHERE codigo = ?", (fk_codigo,))
                if not cursor.fetchone():
                    print(f"⚠️ fk_codigo '{fk_codigo}' no existe en producto. Se omite fila.")
                    continue

            cursor.execute(f"""
                INSERT OR REPLACE INTO {nombre_hoja} ({','.join(columnas)})
                VALUES ({','.join(['?'] * len(columnas))})
            """, fila)

    conn.commit()
    conn.close()

    if hojas_faltantes:
        print(f"⚠️ Hojas faltantes: {', '.join(hojas_faltantes)}")

def obtener_columnas_tabla(cursor, nombre_tabla):
    cursor.execute(f"PRAGMA table_info({nombre_tabla})")
    return [col[1] for col in cursor.fetchall()]


if __name__ == "__main__":
    crear_tablas()