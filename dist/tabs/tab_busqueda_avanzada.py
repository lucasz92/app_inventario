# tab_busqueda_avanzada.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QGroupBox,
    QGridLayout, QMessageBox, QTextEdit, QSpinBox
)
from PyQt6.QtCore import Qt
import sqlite3

class TabBusquedaAvanzada(QWidget):
    def __init__(self):
        super().__init__()
        self.db_path = "data/inventario.db"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título
        title_label = QLabel("Búsqueda Avanzada de Productos")
        title_label.setObjectName("sectionTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Grupo de filtros
        filtros_group = QGroupBox("Criterios de Búsqueda")
        filtros_group.setObjectName("searchGroup")
        filtros_layout = QGridLayout(filtros_group)
        filtros_layout.setSpacing(15)

        # Primera fila
        filtros_layout.addWidget(QLabel("Código:"), 0, 0)
        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Parte del código...")
        self.input_codigo.setObjectName("searchInput")
        filtros_layout.addWidget(self.input_codigo, 0, 1)

        filtros_layout.addWidget(QLabel("Descripción:"), 0, 2)
        self.input_desc = QLineEdit()
        self.input_desc.setPlaceholderText("Parte de la descripción...")
        self.input_desc.setObjectName("searchInput")
        filtros_layout.addWidget(self.input_desc, 0, 3)

        # Segunda fila
        filtros_layout.addWidget(QLabel("Proveedor:"), 1, 0)
        self.input_proveedor = QLineEdit()
        self.input_proveedor.setPlaceholderText("Nombre del proveedor...")
        self.input_proveedor.setObjectName("searchInput")
        filtros_layout.addWidget(self.input_proveedor, 1, 1)

        filtros_layout.addWidget(QLabel("Tipo Control:"), 1, 2)
        self.input_tipo = QComboBox()
        self.input_tipo.setObjectName("searchCombo")
        self.input_tipo.setEditable(True)
        self.input_tipo.addItems(["", "manual", "automático", "semiautomático"])
        filtros_layout.addWidget(self.input_tipo, 1, 3)

        # Tercera fila - Categoría y Stock
        filtros_layout.addWidget(QLabel("Categoría:"), 2, 0)
        self.input_categoria = QComboBox()
        self.input_categoria.setObjectName("searchCombo")
        self.input_categoria.setEditable(True)
        self.load_categories()
        filtros_layout.addWidget(self.input_categoria, 2, 1)

        filtros_layout.addWidget(QLabel("Estado Stock:"), 2, 2)
        self.stock_filter = QComboBox()
        self.stock_filter.setObjectName("searchCombo")
        self.stock_filter.addItems(["Todos", "Con stock", "Sin stock", "Stock bajo"])
        filtros_layout.addWidget(self.stock_filter, 2, 3)

        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.setObjectName("clearButton")
        self.btn_limpiar.clicked.connect(self.limpiar_filtros)
        buttons_layout.addWidget(self.btn_limpiar)

        self.btn_buscar = QPushButton("Buscar Productos")
        self.btn_buscar.setObjectName("searchButton")
        self.btn_buscar.clicked.connect(self.buscar_productos)
        buttons_layout.addWidget(self.btn_buscar)

        filtros_layout.addLayout(buttons_layout, 3, 0, 1, 4)

        layout.addWidget(filtros_group)

        # Etiqueta de resultados
        self.results_label = QLabel("Resultados de la búsqueda")
        self.results_label.setObjectName("resultsLabel")
        layout.addWidget(self.results_label)

        # Tabla de resultados
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setObjectName("tabla_resultados")
        self.tabla_resultados.setColumnCount(7)
        self.tabla_resultados.setHorizontalHeaderLabels([
            "Código", "Descripción", "Categoría", "Proveedor", "Tipo Control", "Stock", "Ubicación"
        ])
        
        # Configurar tabla
        self.tabla_resultados.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_resultados.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabla_resultados.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_resultados.setAlternatingRowColors(True)
        self.tabla_resultados.verticalHeader().setVisible(False)
        
        # Configurar anchos de columna
        header = self.tabla_resultados.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # Código
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Descripción
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Categoría
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Proveedor
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Tipo
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Stock
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)  # Ubicación
        
        self.tabla_resultados.setColumnWidth(0, 100)
        self.tabla_resultados.setColumnWidth(5, 80)
        
        # Conectar doble clic
        self.tabla_resultados.cellDoubleClicked.connect(self.ver_detalles_producto)
        
        layout.addWidget(self.tabla_resultados)

        # Botones de acción
        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.btn_ver_detalles = QPushButton("Ver Detalles")
        self.btn_ver_detalles.setObjectName("detailsButton")
        self.btn_ver_detalles.clicked.connect(self.ver_detalles_producto)
        action_layout.addWidget(self.btn_ver_detalles)

        self.btn_editar = QPushButton("Editar Producto")
        self.btn_editar.setObjectName("editButton")
        self.btn_editar.clicked.connect(self.editar_producto)
        action_layout.addWidget(self.btn_editar)

        layout.addLayout(action_layout)

    def buscar_productos(self):
        codigo = self.input_codigo.text().strip()
        desc = self.input_desc.text().strip()
        proveedor = self.input_proveedor.text().strip()
        tipo = self.input_tipo.currentText().strip()
        categoria = self.input_categoria.currentText().strip()
        stock_estado = self.stock_filter.currentText()

        query = """
        SELECT p.codigo, p.descripcion, p.categoria, p.proveedor, p.tipo_control, p.stock_actual,
               CASE 
                   WHEN u.fila IS NOT NULL THEN 
                       'Fila ' || u.fila || ', Col ' || COALESCE(u.columna, '') || 
                       ', Est ' || COALESCE(u.estante, '') || ', Pos ' || COALESCE(u.posicion, '')
                   ELSE 'Sin ubicación'
               END as ubicacion
        FROM productos p
        LEFT JOIN producto_ubicacion pu ON p.codigo = pu.codigo_producto
        LEFT JOIN ubicaciones u ON pu.id_ubicacion = u.id_ubicacion
        WHERE 1=1
        """
        params = []

        if codigo:
            query += " AND p.codigo LIKE ?"
            params.append(f"%{codigo}%")
        if desc:
            query += " AND p.descripcion LIKE ?"
            params.append(f"%{desc}%")
        if proveedor:
            query += " AND p.proveedor LIKE ?"
            params.append(f"%{proveedor}%")
        if tipo:
            query += " AND p.tipo_control LIKE ?"
            params.append(f"%{tipo}%")
        if categoria:
            query += " AND p.categoria LIKE ?"
            params.append(f"%{categoria}%")
        
        # Filtros de stock
        if stock_estado == "Con stock":
            query += " AND p.stock_actual > 0"
        elif stock_estado == "Sin stock":
            query += " AND (p.stock_actual = 0 OR p.stock_actual IS NULL)"
        elif stock_estado == "Stock bajo":
            query += " AND p.stock_actual > 0 AND p.stock_minimo > 0 AND p.stock_actual < p.stock_minimo"

        query += " ORDER BY p.codigo"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()

        self.tabla_resultados.setRowCount(0)
        # Actualizar etiqueta de resultados
        self.results_label.setText(f"Resultados de la búsqueda ({len(resultados)} productos encontrados)")
        
        for fila_data in resultados:
            row_pos = self.tabla_resultados.rowCount()
            self.tabla_resultados.insertRow(row_pos)
            for col, valor in enumerate(fila_data):
                item = QTableWidgetItem(str(valor) if valor is not None else "")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_resultados.setItem(row_pos, col, item)

    def load_categories(self):
        """Carga las categorías existentes."""
        self.input_categoria.addItem("")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT categoria FROM productos WHERE categoria IS NOT NULL AND categoria != '' ORDER BY categoria")
        categories = cursor.fetchall()
        conn.close()
        
        for category in categories:
            self.input_categoria.addItem(category[0])

    def limpiar_filtros(self):
        """Limpia todos los filtros de búsqueda."""
        self.input_codigo.clear()
        self.input_desc.clear()
        self.input_proveedor.clear()
        self.input_tipo.setCurrentIndex(0)
        self.input_categoria.setCurrentIndex(0)
        self.stock_filter.setCurrentIndex(0)
        
        # Limpiar resultados
        self.tabla_resultados.setRowCount(0)
        self.results_label.setText("Resultados de la búsqueda")

    def ver_detalles_producto(self):
        """Muestra los detalles del producto seleccionado."""
        fila_actual = self.tabla_resultados.currentRow()
        if fila_actual < 0:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Selección Requerida", "Selecciona un producto para ver sus detalles.")
            return
        
        codigo_item = self.tabla_resultados.item(fila_actual, 0)
        if not codigo_item:
            return
        
        codigo = codigo_item.text()
        
        # Obtener datos del producto
        conn = sqlite3.connect(self.db_path)
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
        
        # Crear diálogo en modo solo lectura (sin permitir edición)
        dialog = ProductFormDialog(self, product_data)
        dialog.setWindowTitle(f"Detalles del Producto: {codigo}")
        
        # Hacer todos los campos de solo lectura
        for widget in dialog.findChildren(QLineEdit):
            widget.setReadOnly(True)
        for widget in dialog.findChildren(QComboBox):
            widget.setEnabled(False)
        for widget in dialog.findChildren(QSpinBox):
            widget.setReadOnly(True)
        for widget in dialog.findChildren(QTextEdit):
            widget.setReadOnly(True)
        
        dialog.exec()

    def editar_producto(self):
        """Edita el producto seleccionado."""
        fila_actual = self.tabla_resultados.currentRow()
        if fila_actual < 0:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Selección Requerida", "Selecciona un producto para editar.")
            return
        
        codigo_item = self.tabla_resultados.item(fila_actual, 0)
        if not codigo_item:
            return
        
        codigo = codigo_item.text()
        
        # Obtener datos del producto
        conn = sqlite3.connect(self.db_path)
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
            # Actualizar resultados de búsqueda
            self.buscar_productos()
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Producto Actualizado", "El producto ha sido actualizado correctamente.")
