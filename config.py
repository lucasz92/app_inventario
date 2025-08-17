"""
Configuración de la aplicación Gestor de Inventario
"""

# Configuración de la base de datos
DATABASE_PATH = "data/inventario.db"

# Configuración de la ventana principal
WINDOW_TITLE = "Gestor de Productos"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 300
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 200

# Configuración de estilos
STYLES_PATH = "ui/styles.qss"

# Configuración de exportación
EXPORT_FORMATS = {
    "Excel": "*.xlsx",
    "CSV": "*.csv"
}

# Configuración de alertas
ALERT_TYPES = ["Alta prioridad", "Media", "Baja"]
ALERT_STATES = ["sin iniciar", "en progreso", "completada", "cancelada"]

# Configuración de productos
PRODUCT_FIELDS = {
    "codigo": {"label": "Código", "required": True, "max_length": 20},
    "descripcion": {"label": "Descripción", "required": True, "max_length": 200},
    "categoria": {"label": "Categoría", "required": False, "max_length": 50},
    "proveedor": {"label": "Proveedor", "required": False, "max_length": 100},
    "puesto_trabajo": {"label": "Puesto", "required": False, "max_length": 50},
    "stock_actual": {"label": "Stock actual", "required": False, "type": "int", "min": 0},
    "unidad_medida": {"label": "Unidad", "required": False, "max_length": 20},
    "tipo_control": {"label": "Tipo control", "required": False, "max_length": 50},
    "stock_minimo": {"label": "Stock mínimo", "required": False, "type": "int", "min": 0},
    "stock_maximo": {"label": "Stock máximo", "required": False, "type": "int", "min": 0},
    "observacion": {"label": "Observación", "required": False, "max_length": 500}
}

# Configuración de ubicaciones
LOCATION_FIELDS = {
    "fila": {"label": "Fila", "required": True, "type": "int", "min": 1},
    "columna": {"label": "Columna", "required": True, "max_length": 10},
    "estante": {"label": "Estante", "required": True, "type": "int", "min": 1},
    "posicion": {"label": "Posición", "required": True, "type": "int", "min": 1},
    "orientacion": {"label": "Orientación", "required": False, "max_length": 20}
}

# Configuración de tabla
TABLE_COLUMN_WIDTHS = {
    "productos": [100, 200, 80, 80, 80, 90, 90, 90],
    "busqueda": [100, 200, 150, 120, 80],
    "alertas": [50, 100, 200, 60, 60, 60, 100, 100, 120]
}

# Mensajes de la aplicación
MESSAGES = {
    "confirm_delete": "¿Estás seguro de eliminar el producto {codigo}?",
    "product_added": "Producto agregado correctamente",
    "product_updated": "Producto actualizado correctamente",
    "product_deleted": "Producto eliminado correctamente",
    "alert_saved": "Alerta guardada correctamente",
    "data_imported": "Datos importados correctamente",
    "data_exported": "Datos exportados correctamente",
    "select_product": "Selecciona un producto para {action}",
    "product_not_found": "Producto no encontrado",
    "database_error": "Error en la base de datos: {error}",
    "file_error": "Error con el archivo: {error}"
}