# tab_productos.py
import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QLineEdit,
    QPushButton, QHBoxLayout, QGraphicsDropShadowEffect, QGroupBox, QFrame
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView

from data.database import obtener_productos_con_ubicacion, obtener_detalles_producto, buscar_productos

class TabProductos(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("tabProductos")
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setObjectName("layout_principal")
        layout_principal.setContentsMargins(8, 8, 8, 8)
        layout_principal.setSpacing(8)

        # Título
        titulo = QLabel("Listado de Productos")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_principal.addWidget(titulo)

        # Buscador (card)
        layout_principal.addLayout(self.buscador())

        # Header compacto sobre la tabla (contador / hint)
        header_tabla = QHBoxLayout()
        self.results_label = QLabel("Mostrando 0 productos")
        self.results_label.setObjectName("resultsLabel")
        header_tabla.addWidget(self.results_label)
        header_tabla.addStretch(1)
        layout_principal.addLayout(header_tabla)

        # Panel contenido: tabla + detalles
        panel_contenido = QHBoxLayout()
        panel_contenido.setObjectName("panel_contenido")
        panel_contenido.setSpacing(12)

        # Izquierda: tabla (card visual)
        tabla_card = QFrame()
        tabla_card.setObjectName("tabla_card")
        tabla_card.setProperty("class", "QCard")
        tabla_card_lay = QVBoxLayout(tabla_card)
        tabla_card_lay.setContentsMargins(8, 8, 8, 8)
        tabla_card_lay.setSpacing(6)

        tabla_title = QLabel("Productos")
        tabla_title.setObjectName("subsectionTitle")
        tabla_card_lay.addWidget(tabla_title)

        tabla = self.crear_tabla()
        tabla_card_lay.addWidget(tabla)

        # Derecha: detalles (card)
        self.panel_derecho_widget = QFrame()
        self.panel_derecho_widget.setObjectName("panel_derecho_widget")  # ya estilizado en QSS
        panel_derecho_lay = QVBoxLayout(self.panel_derecho_widget)
        panel_derecho_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        panel_derecho_lay.setContentsMargins(12, 12, 12, 12)
        panel_derecho_lay.setSpacing(4)

        detalles_title = QLabel("Más información del producto")
        detalles_title.setObjectName("detalles_label")
        panel_derecho_lay.addWidget(detalles_title)

        self.detalles_campos = {}
        for campo in ["Proveedor", "Tipo", "Max/Min", "Categoría", "Puesto", "Observación"]:
            label = QLabel(f"<b>{campo}:</b> —")
            label.setFont(QFont("Segoe UI", 11))
            label.setContentsMargins(6, 8, 6, 8)
            panel_derecho_lay.addWidget(label)
            self.detalles_campos[campo] = label

        # Agregar ambos
        panel_contenido.addWidget(tabla_card, 5)
        panel_contenido.addWidget(self.panel_derecho_widget, 3)
        layout_principal.addLayout(panel_contenido)

        # Panel inferior: acciones
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

        # Carga inicial
        datos_iniciales = obtener_productos_con_ubicacion()
        self.actualizar_resultados_label(datos_iniciales)
        actualizar_tabla(self.tabla, datos_iniciales)

    def buscador(self):
        contenedor_buscador = QWidget()
        contenedor_buscador.setObjectName("buscador_container")

        layout = QHBoxLayout(contenedor_buscador)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        buscador_label = QLabel("<b>Buscar producto:</b>")
        buscador_label.setFont(QFont("Segoe UI", 12))

        self.buscador_textbox = QLineEdit()
        self.buscador_textbox.setFixedWidth(480)
        self.buscador_textbox.setObjectName("buscador")
        self.buscador_textbox.setPlaceholderText("Escribe el nombre o código...")

        self.buscador_textbox.textChanged.connect(self.filtrar_tabla)

        layout.addWidget(buscador_label)
        layout.addWidget(self.buscador_textbox, 0)
        layout.addStretch(1)

        cont = QVBoxLayout()
        cont.setContentsMargins(0, 0, 0, 0)
        cont.addWidget(contenedor_buscador)
        return cont

    def crear_tabla(self):
        self.tabla = QTableWidget()
        self.tabla.setObjectName("tabla")
        self.tabla.setColumnCount(9)
        self.tabla.setHorizontalHeaderLabels([
            "Código", "Descripción", "Fila", "Columna", "Estante",
            "Posición", "Orientación", "Depósito", "Sector"
        ])

        # Anchos + resize policy
        anchos = [110, 260, 70, 80, 80, 90, 110, 110, 110]
        for i, ancho in enumerate(anchos):
            self.tabla.setColumnWidth(i, ancho)

        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)

        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSortingEnabled(True)
        self.tabla.setWordWrap(False)
        self.tabla.setShowGrid(False)
        self.tabla.cellClicked.connect(self.mostrar_detalles_producto)

        actualizar_tabla(self.tabla, [])
        return self.tabla

    def filtrar_tabla(self, texto):
        texto = str(texto).strip()
        if texto:
            datos_filtrados = buscar_productos(texto)
        else:
            datos_filtrados = obtener_productos_con_ubicacion()
        self.actualizar_resultados_label(datos_filtrados)
        actualizar_tabla(self.tabla, datos_filtrados)

    def actualizar_resultados_label(self, datos):
        n = len(datos) if datos else 0
        self.results_label.setText(f"Mostrando {n} producto{'s' if n!=1 else ''}")

    def cargar_tabla_productos_con_ubicacion(self):
        datos = obtener_productos_con_ubicacion()
        self.actualizar_resultados_label(datos)
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
        from data.database import conectar_db
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
        producto_row = cursor.fetchone()
        conn.close()
        if not producto_row:
            return

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
        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Estás seguro de eliminar el producto {codigo}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
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
        self.actualizar_resultados_label(datos)
        actualizar_tabla(self.tabla, datos)

def actualizar_tabla(tabla, datos):
    tabla.setRowCount(0)
    if not datos:
        return
    tabla.setRowCount(len(datos))
    for fila_idx, fila in enumerate(datos):
        for col_idx, valor in enumerate(fila):
            item = QTableWidgetItem(str(valor))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(fila_idx, col_idx, item)
