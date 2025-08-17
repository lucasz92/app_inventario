# tab_productos.py
import re

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import Qt


from data.database import obtener_productos_con_ubicacion, obtener_detalles_producto, buscar_productos
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QGroupBox, QFrame
from PyQt6.QtGui import QColor

class TabProductos(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

# --- [crear_buscador]: layout con QLineEdit y botones

    def init_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setObjectName("layout_principal")

        # Título
        titulo = QLabel("Listado de Productos")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo)

        # Buscador
        layout_principal.addLayout(self.buscador())

        # Panel de contenido: tabla + detalles
        panel_contenido = QHBoxLayout()
        panel_contenido.setObjectName("panel_contenido")

        # Panel izquierdo: tabla
        panel_izquierdo = QVBoxLayout()
        panel_izquierdo.setObjectName("panel_izquierdo")
        panel_izquierdo.addWidget(self.crear_tabla())

        # Panel derecho: detalles
        self.panel_derecho_widget = QWidget()
        self.panel_derecho_widget.setObjectName("panel_derecho_widget")
        self.panel_derecho = QVBoxLayout(self.panel_derecho_widget)
        self.panel_derecho.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.detalles_label = QLabel("<b>Más información del producto</b>")
        self.detalles_label.setObjectName("detalles_label")
        self.panel_derecho.addWidget(self.detalles_label)

        self.detalles_campos = {}
        for campo in ["Proveedor", "Tipo", "Max/Min", "Categoría", "Puesto", "Observación"]:
            label = QLabel(f"{campo}:")
            label.setFont(QFont("Segoe UI", 11))
            label.setContentsMargins(8, 11, 8, 11)
            self.panel_derecho.addWidget(label)
            self.detalles_campos[campo] = label

        # Agregar paneles al panel de contenido
        panel_contenido.addLayout(panel_izquierdo, 4)
        panel_contenido.addWidget(self.panel_derecho_widget, 2)

        layout_principal.addLayout(panel_contenido)

        # Panel inferior: botones
        self.panel_inferior = QHBoxLayout()
        self.panel_inferior.addStretch(1)

        btnEliminar = QPushButton("Eliminar Producto")
        btnEliminar.setObjectName("btnEliminar")
        btnEliminar.clicked.connect(self.eliminar_producto)

        btnModificar = QPushButton("Modificar Producto")
        btnModificar.setObjectName("btnModificar")
        btnModificar.clicked.connect(self.modificar_producto)

        btnAgregar = QPushButton("Agregar Producto")
        btnAgregar.setObjectName("btnAgregar")
        btnAgregar.clicked.connect(self.agregar_producto)

        self.panel_inferior.addWidget(btnAgregar)
        self.panel_inferior.addWidget(btnModificar)
        self.panel_inferior.addWidget(btnEliminar)

        layout_principal.addLayout(self.panel_inferior)

        # Cargar datos iniciales
        datos_iniciales = obtener_productos_con_ubicacion()
        actualizar_tabla(self.tabla, datos_iniciales)
        
    def buscador(self):
        layout = QHBoxLayout()
        buscador_label = QLabel("<b>Buscar producto:</b>")
        buscador_label.setFont(QFont("Segoe UI", 12))

        self.buscador_textbox = QLineEdit()
        self.buscador_textbox.setFixedWidth(500)
        self.buscador_textbox.setObjectName("buscador")
        self.buscador_textbox.setPlaceholderText("Escribe el nombre del producto...")

        self.buscador_textbox.textChanged.connect(self.filtrar_tabla)

        layout.addWidget(buscador_label)
        layout.addWidget(self.buscador_textbox)
        layout.addStretch(1)
        return layout
    

    def filtrar_tabla(self, texto):
        texto = str(texto).strip()
        if texto:
            datos_filtrados = buscar_productos(texto)
        else:
            datos_filtrados = obtener_productos_con_ubicacion()
        actualizar_tabla(self.tabla, datos_filtrados)



    def crear_tabla(self):
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(9)
        anchos = [110, 220, 60, 60, 60, 60, 90, 90, 90]
        for i, ancho in enumerate(anchos):
            self.tabla.setColumnWidth(i, ancho)

        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setObjectName("tabla")
        self.tabla.setHorizontalHeaderLabels([
            "Código", "Descripción", "Fila", "Columna", "Estante",
            "Posición", "Orientación", "Depósito", "Sector"
        ])
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.cellClicked.connect(self.mostrar_detalles_producto)
        self.tabla.setAlternatingRowColors(True)
        actualizar_tabla(self.tabla, [])  # ← ahora es función externa
        return self.tabla


    def cargar_tabla_productos_con_ubicacion(self):
        datos = obtener_productos_con_ubicacion()
        self.tabla.setRowCount(len(datos))

        for fila_idx, fila in enumerate(datos):
            for col_idx, valor in enumerate(fila):
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla.setItem(fila_idx, col_idx, item)

        
    def mostrar_detalles_producto(self, fila, columna):
        codigo_item = self.tabla.item(fila, 0)
        if not codigo_item:
            return
        codigo = codigo_item.text()
        detalles = obtener_detalles_producto(codigo)
        if detalles:
            campos = ["Proveedor", "Tipo", "Max/Min", "Categoría", "Puesto", "Observación"]
            # Asegurar que no excedamos el número de campos disponibles
            for i, campo in enumerate(campos):
                if i < len(detalles) and campo in self.detalles_campos:
                    valor = detalles[i] if detalles[i] is not None else "N/A"
                    self.detalles_campos[campo].setText(f"<b>{campo}:</b> {valor}")

    def agregar_producto(self):
        from tabs.dialogs import ProductFormDialog
        
        dialog = ProductFormDialog(self)
        if dialog.exec() == ProductFormDialog.DialogCode.Accepted:
            self.actualizar_tabla_productos()

    def modificar_producto(self):
        fila_actual = self.tabla.currentRow()
        if fila_actual < 0:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Advertencia", "Selecciona un producto para modificar")
            return
            
        codigo_item = self.tabla.item(fila_actual, 0)
        if not codigo_item:
            return
            
        codigo = codigo_item.text()
        
        # Obtener datos actuales del producto
        from data.database import conectar_db
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
        producto_row = cursor.fetchone()
        conn.close()
        
        if not producto_row:
            return
        
        # Convertir a diccionario
        product_data = {
            'codigo': producto_row[0],
            'descripcion': producto_row[1],
            'categoria': producto_row[2],
            'proveedor': producto_row[3],
            'puesto_trabajo': producto_row[4],
            'stock_actual': producto_row[5],
            'unidad_medida': producto_row[6],
            'tipo_control': producto_row[7],
            'stock_minimo': producto_row[8],
            'stock_maximo': producto_row[9],
            'observacion': producto_row[10]
        }
        
        from tabs.dialogs import ProductFormDialog
        
        dialog = ProductFormDialog(self, product_data)
        if dialog.exec() == ProductFormDialog.DialogCode.Accepted:
            self.actualizar_tabla_productos()

    def eliminar_producto(self):
        fila_actual = self.tabla.currentRow()
        if fila_actual < 0:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Advertencia", "Selecciona un producto para eliminar")
            return
            
        codigo_item = self.tabla.item(fila_actual, 0)
        if not codigo_item:
            return
            
        codigo = codigo_item.text()
        
        from PyQt6.QtWidgets import QMessageBox
        respuesta = QMessageBox.question(self, "Confirmar eliminación", 
                                       f"¿Estás seguro de eliminar el producto {codigo}?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if respuesta == QMessageBox.StandardButton.Yes:
            from data.database import conectar_db
            conn = conectar_db()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
                conn.commit()
                self.actualizar_tabla_productos()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo eliminar el producto: {e}")
            finally:
                conn.close()

    def actualizar_tabla_productos(self):
        datos = obtener_productos_con_ubicacion()
        actualizar_tabla(self.tabla, datos)
                

def actualizar_tabla(tabla, datos):
    tabla.setRowCount(0)
    tabla.setRowCount(len(datos))

    for fila_idx, fila in enumerate(datos):
        for col_idx, valor in enumerate(fila):
            item = QTableWidgetItem(str(valor))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(fila_idx, col_idx, item)



