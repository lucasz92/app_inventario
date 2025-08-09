from openpyxl import Workbook

def generar_excel_ejemplo(ruta_archivo="ejemplo_importacion.xlsx"):
    wb = Workbook()

    # 🧱 Hoja producto
    ws_producto = wb.active
    ws_producto.title = "producto"
    ws_producto.append([
        "codigo", "descripcion", "proveedor", "tipo",
        "maxmin", "categoria", "puesto", "observacion"
    ])
    ws_producto.append([
        "P001", "Martillo de acero", "Ferretería Central", "max",
        "50", "Herramientas", "Puesto A", "Sin observaciones"
    ])
    ws_producto.append([
        "P002", "Maceta de cerámica", "Jardín Feliz", "min",
        "10", "Jardinería", "Puesto B", "Frágil"
    ])

    # 📦 Hoja ubicacion
    ws_ubicacion = wb.create_sheet(title="ubicacion")
    ws_ubicacion.append([
        "fk_codigo", "fila", "columna", "estante",
        "deposito", "sector", "ubicacion"
    ])
    ws_ubicacion.append([
        "P001", "1", "A", "Estante 1", "Depósito Norte", "Sector Herramientas", "U001"
    ])
    ws_ubicacion.append([
        "P002", "2", "B", "Estante 3", "Depósito Sur", "Sector Jardinería", "U002"
    ])

    wb.save(ruta_archivo)
    print(f"✅ Archivo de ejemplo guardado en: {ruta_archivo}")

# Ejecutar directamente
if __name__ == "__main__":
    generar_excel_ejemplo()