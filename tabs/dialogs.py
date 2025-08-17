#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diálogos modales para el Sistema de Gestión de Inventario.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QFormLayout, QTextEdit, QComboBox, QSpinBox, QTabWidget, QWidget,
    QMessageBox, QGroupBox, QGridLayout, QCheckBox, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from data.database import conectar_db, obtener_productos_con_ubicacion

class ProductFormDialog(QDialog):
    """Diálogo moderno para agregar o editar un producto."""
    
    def __init__(self, parent=None, product_data=None):
        """
        Inicializa el diálogo de formulario de producto.
        
        Args:
            parent: Widget padre
            product_data: Datos del producto para edición (None para nuevo producto)
        """
        super().__init__(parent)
        
        self.product_data = product_data
        self.is_editing = product_data is not None
        
        # Configurar diálogo
        self.setWindowTitle("Editar Producto" if self.is_editing else "Nuevo Producto")
        self.setMinimumSize(800, 650)
        self.setMaximumSize(1000, 800)
        self.resize(850, 700)
        self.setModal(True)
        
        # Crear interfaz
        self.init_ui()
        
        # Cargar datos si es edición
        if self.is_editing:
            self.load_product_data()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Título
        title_label = QLabel("Editar Producto" if self.is_editing else "Nuevo Producto")
        title_label.setObjectName("dialogTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Pestañas
        self.tabs = QTabWidget()
        self.tabs.setObjectName("dialogTabs")
        
        # Pestaña de información básica
        self.create_basic_tab()
        
        # Pestaña de ubicación
        self.create_location_tab()
        
        # Pestaña de stock
        self.create_stock_tab()
        
        layout.addWidget(self.tabs)
        
        # Botones
        self.create_buttons(layout)
    
    def create_basic_tab(self):
        """Crea la pestaña de información básica."""
        basic_tab = QWidget()
        layout = QVBoxLayout(basic_tab)
        layout.setSpacing(12)
        
        # Grupo de información principal
        main_group = QGroupBox("Información Principal")
        main_group.setObjectName("formGroup")
        main_layout = QFormLayout(main_group)
        main_layout.setSpacing(8)
        
        # Código (solo lectura si es edición)
        self.code_input = QLineEdit()
        self.code_input.setObjectName("formInput")
        if self.is_editing:
            self.code_input.setReadOnly(True)
            self.code_input.setStyleSheet("background-color: #f5f5f5;")
        main_layout.addRow("Código *:", self.code_input)
        
        # Descripción
        self.description_input = QLineEdit()
        self.description_input.setObjectName("formInput")
        main_layout.addRow("Descripción *:", self.description_input)
        
        # Categoría
        self.category_input = QComboBox()
        self.category_input.setObjectName("formCombo")
        self.category_input.setEditable(True)
        self.load_categories()
        main_layout.addRow("Categoría:", self.category_input)
        
        # Proveedor
        self.provider_input = QLineEdit()
        self.provider_input.setObjectName("formInput")
        main_layout.addRow("Proveedor:", self.provider_input)
        
        # Puesto de trabajo
        self.position_input = QLineEdit()
        self.position_input.setObjectName("formInput")
        main_layout.addRow("Puesto de Trabajo:", self.position_input)
        
        # Unidad de medida
        self.unit_input = QComboBox()
        self.unit_input.setObjectName("formCombo")
        self.unit_input.setEditable(True)
        self.unit_input.addItems(["", "unidad", "metro", "litro", "kilogramo", "caja", "paquete"])
        main_layout.addRow("Unidad de Medida:", self.unit_input)
        
        # Tipo de control
        self.control_type_input = QComboBox()
        self.control_type_input.setObjectName("formCombo")
        self.control_type_input.addItems(["", "manual", "automático", "semiautomático"])
        main_layout.addRow("Tipo de Control:", self.control_type_input)
        
        layout.addWidget(main_group)
        
        # Grupo de observaciones
        obs_group = QGroupBox("Observaciones")
        obs_group.setObjectName("formGroup")
        obs_layout = QVBoxLayout(obs_group)
        
        self.observation_input = QTextEdit()
        self.observation_input.setObjectName("formTextArea")
        self.observation_input.setMaximumHeight(100)
        self.observation_input.setPlaceholderText("Observaciones adicionales sobre el producto...")
        obs_layout.addWidget(self.observation_input)
        
        layout.addWidget(obs_group)
        layout.addStretch()
        
        self.tabs.addTab(basic_tab, "Información Básica")
    
    def create_location_tab(self):
        """Crea la pestaña de ubicación."""
        location_tab = QWidget()
        layout = QVBoxLayout(location_tab)
        layout.setSpacing(12)
        
        # Grupo de ubicación física
        location_group = QGroupBox("Ubicación Física")
        location_group.setObjectName("formGroup")
        location_layout = QGridLayout(location_group)
        location_layout.setSpacing(8)
        
        # Fila
        location_layout.addWidget(QLabel("Fila:"), 0, 0)
        self.row_input = QSpinBox()
        self.row_input.setObjectName("formSpinBox")
        self.row_input.setRange(1, 15)
        self.row_input.setValue(1)
        location_layout.addWidget(self.row_input, 0, 1)
        
        # Columna
        location_layout.addWidget(QLabel("Columna:"), 0, 2)
        self.column_input = QComboBox()
        self.column_input.setObjectName("formCombo")
        self.column_input.setEditable(True)
        self.column_input.addItems(["", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"])
        location_layout.addWidget(self.column_input, 0, 3)
        
        # Estante
        location_layout.addWidget(QLabel("Estante:"), 1, 0)
        self.shelf_input = QSpinBox()
        self.shelf_input.setObjectName("formSpinBox")
        self.shelf_input.setRange(1, 10)
        self.shelf_input.setValue(1)
        location_layout.addWidget(self.shelf_input, 1, 1)
        
        # Posición
        location_layout.addWidget(QLabel("Posición:"), 1, 2)
        self.position_shelf_input = QSpinBox()
        self.position_shelf_input.setObjectName("formSpinBox")
        self.position_shelf_input.setRange(1, 999)
        self.position_shelf_input.setValue(1)
        location_layout.addWidget(self.position_shelf_input, 1, 3)
        
        # Orientación
        location_layout.addWidget(QLabel("Orientación:"), 2, 0)
        self.orientation_input = QComboBox()
        self.orientation_input.setObjectName("formCombo")
        self.orientation_input.addItems(["", "NORTE", "SUR", "ESTE", "OESTE"])
        location_layout.addWidget(self.orientation_input, 2, 1)
        
        # Depósito
        location_layout.addWidget(QLabel("Depósito:"), 2, 2)
        self.deposito_input = QComboBox()
        self.deposito_input.setObjectName("formCombo")
        self.deposito_input.setEditable(True)
        self.deposito_input.addItems(["", "DEP01", "DEP02"])
        location_layout.addWidget(self.deposito_input, 2, 3)
        
        # Sector
        location_layout.addWidget(QLabel("Sector:"), 3, 0)
        self.sector_input = QComboBox()
        self.sector_input.setObjectName("formCombo")
        self.sector_input.setEditable(True)
        self.sector_input.addItems(["", "PAÑOL 1", "PAÑOL 2"])
        location_layout.addWidget(self.sector_input, 3, 1)
        
        layout.addWidget(location_group)
        
        # Selector de ubicaciones existentes
        existing_group = QGroupBox("Ubicaciones Existentes")
        existing_group.setObjectName("formGroup")
        existing_layout = QVBoxLayout(existing_group)
        
        info_label = QLabel("Selecciona una ubicación existente para copiar sus datos:")
        info_label.setObjectName("infoLabel")
        existing_layout.addWidget(info_label)
        
        self.location_selector = QComboBox()
        self.location_selector.setObjectName("formCombo")
        self.location_selector.currentIndexChanged.connect(self.on_location_selected)
        self.load_existing_locations()
        existing_layout.addWidget(self.location_selector)
        
        layout.addWidget(existing_group)
        layout.addStretch()
        
        self.tabs.addTab(location_tab, "Ubicación")
    
    def create_stock_tab(self):
        """Crea la pestaña de stock."""
        stock_tab = QWidget()
        layout = QVBoxLayout(stock_tab)
        layout.setSpacing(12)
        
        # Grupo de stock actual
        current_group = QGroupBox("Stock Actual")
        current_group.setObjectName("formGroup")
        current_layout = QFormLayout(current_group)
        current_layout.setSpacing(8)
        
        self.stock_input = QSpinBox()
        self.stock_input.setObjectName("formSpinBox")
        self.stock_input.setRange(0, 999999)
        self.stock_input.setSuffix(" unidades")
        current_layout.addRow("Cantidad Actual:", self.stock_input)
        
        layout.addWidget(current_group)
        
        # Grupo de límites de stock
        limits_group = QGroupBox("Límites de Stock")
        limits_group.setObjectName("formGroup")
        limits_layout = QGridLayout(limits_group)
        limits_layout.setSpacing(8)
        
        # Stock mínimo
        limits_layout.addWidget(QLabel("Stock Mínimo:"), 0, 0)
        self.min_stock_input = QSpinBox()
        self.min_stock_input.setObjectName("formSpinBox")
        self.min_stock_input.setRange(0, 999999)
        self.min_stock_input.setSuffix(" unidades")
        limits_layout.addWidget(self.min_stock_input, 0, 1)
        
        # Stock máximo
        limits_layout.addWidget(QLabel("Stock Máximo:"), 0, 2)
        self.max_stock_input = QSpinBox()
        self.max_stock_input.setObjectName("formSpinBox")
        self.max_stock_input.setRange(0, 999999)
        self.max_stock_input.setSuffix(" unidades")
        limits_layout.addWidget(self.max_stock_input, 0, 3)
        
        # Indicador de estado
        self.stock_status_label = QLabel()
        self.stock_status_label.setObjectName("stockStatus")
        limits_layout.addWidget(self.stock_status_label, 1, 0, 1, 4)
        
        # Conectar cambios para actualizar estado
        self.stock_input.valueChanged.connect(self.update_stock_status)
        self.min_stock_input.valueChanged.connect(self.update_stock_status)
        self.max_stock_input.valueChanged.connect(self.update_stock_status)
        
        layout.addWidget(limits_group)
        layout.addStretch()
        
        self.tabs.addTab(stock_tab, "Stock")
    
    def create_buttons(self, layout):
        """Crea los botones del diálogo."""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Botón cancelar
        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # Botón guardar
        save_text = "Actualizar" if self.is_editing else "Crear Producto"
        save_button = QPushButton(save_text)
        save_button.setObjectName("saveButton")
        save_button.clicked.connect(self.save_product)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
    
    def load_categories(self):
        """Carga las categorías existentes."""
        self.category_input.addItem("")
        
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT categoria FROM productos WHERE categoria IS NOT NULL AND categoria != '' ORDER BY categoria")
        categories = cursor.fetchall()
        conn.close()
        
        for category in categories:
            self.category_input.addItem(category[0])
    
    def load_existing_locations(self):
        """Carga las ubicaciones existentes."""
        self.location_selector.addItem("Seleccionar ubicación...", None)
        
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT fila, columna, estante, posicion, orientacion, deposito, sector 
            FROM ubicaciones 
            ORDER BY fila, columna, estante, posicion
        """)
        locations = cursor.fetchall()
        conn.close()
        
        for location in locations:
            fila, columna, estante, posicion, orientacion, deposito, sector = location
            text = f"Fila {fila}, Columna {columna}, Estante {estante}, Pos {posicion}"
            if orientacion:
                text += f" ({orientacion})"
            if deposito:
                text += f" - {deposito}"
            if sector:
                text += f" [{sector}]"
            self.location_selector.addItem(text, location)
    
    def on_location_selected(self, index):
        """Maneja la selección de una ubicación existente."""
        if index <= 0:
            return
        
        location_data = self.location_selector.currentData()
        if location_data:
            fila, columna, estante, posicion, orientacion, deposito, sector = location_data
            self.row_input.setValue(fila or 1)
            if columna:
                self.column_input.setCurrentText(columna)
            self.shelf_input.setValue(estante or 1)
            self.position_shelf_input.setValue(posicion or 1)
            
            if orientacion:
                index = self.orientation_input.findText(orientacion)
                if index >= 0:
                    self.orientation_input.setCurrentIndex(index)
            
            if deposito:
                self.deposito_input.setCurrentText(deposito)
            if sector:
                self.sector_input.setCurrentText(sector)
    
    def load_product_data(self):
        """Carga los datos del producto para edición."""
        if not self.product_data:
            return
        
        # Información básica
        self.code_input.setText(self.product_data.get('codigo', ''))
        self.description_input.setText(self.product_data.get('descripcion', ''))
        
        # Categoría
        categoria = self.product_data.get('categoria', '')
        if categoria:
            index = self.category_input.findText(categoria)
            if index >= 0:
                self.category_input.setCurrentIndex(index)
            else:
                self.category_input.setCurrentText(categoria)
        
        self.provider_input.setText(self.product_data.get('proveedor', ''))
        self.position_input.setText(self.product_data.get('puesto_trabajo', ''))
        self.unit_input.setCurrentText(self.product_data.get('unidad_medida', ''))
        self.control_type_input.setCurrentText(self.product_data.get('tipo_control', ''))
        self.observation_input.setText(self.product_data.get('observacion', ''))
        
        # Stock
        self.stock_input.setValue(self.product_data.get('stock_actual', 0))
        self.min_stock_input.setValue(self.product_data.get('stock_minimo', 0))
        self.max_stock_input.setValue(self.product_data.get('stock_maximo', 0))
        
        # Ubicación - obtener de la tabla de ubicaciones relacionada
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.fila, u.columna, u.estante, u.posicion, u.orientacion, u.deposito, u.sector
            FROM ubicaciones u
            JOIN producto_ubicacion pu ON u.id_ubicacion = pu.id_ubicacion
            WHERE pu.codigo_producto = ?
            LIMIT 1
        """, (self.product_data.get('codigo', ''),))
        location = cursor.fetchone()
        conn.close()
        
        if location:
            self.row_input.setValue(location[0] or 1)
            if location[1]:
                self.column_input.setCurrentText(location[1])
            self.shelf_input.setValue(location[2] or 1)
            self.position_shelf_input.setValue(location[3] or 1)
            if location[4]:
                index = self.orientation_input.findText(location[4])
                if index >= 0:
                    self.orientation_input.setCurrentIndex(index)
            if location[5]:
                self.deposito_input.setCurrentText(location[5])
            if location[6]:
                self.sector_input.setCurrentText(location[6])
        
        self.update_stock_status()
    
    def update_stock_status(self):
        """Actualiza el indicador de estado del stock."""
        current = self.stock_input.value()
        minimum = self.min_stock_input.value()
        maximum = self.max_stock_input.value()
        
        if minimum > 0 and current < minimum:
            self.stock_status_label.setText("⚠️ Stock por debajo del mínimo")
            self.stock_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        elif maximum > 0 and current > maximum:
            self.stock_status_label.setText("⚠️ Stock por encima del máximo")
            self.stock_status_label.setStyleSheet("color: #f39c12; font-weight: bold;")
        elif current == 0:
            self.stock_status_label.setText("❌ Sin stock")
            self.stock_status_label.setStyleSheet("color: #c0392b; font-weight: bold;")
        else:
            self.stock_status_label.setText("✅ Stock normal")
            self.stock_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
    
    def validate_form(self):
        """Valida el formulario."""
        # Código obligatorio
        if not self.code_input.text().strip():
            QMessageBox.warning(self, "Campo Obligatorio", "El código del producto es obligatorio.")
            self.tabs.setCurrentIndex(0)
            self.code_input.setFocus()
            return False
        
        # Descripción obligatoria
        if not self.description_input.text().strip():
            QMessageBox.warning(self, "Campo Obligatorio", "La descripción del producto es obligatoria.")
            self.tabs.setCurrentIndex(0)
            self.description_input.setFocus()
            return False
        
        # Validar que el stock máximo sea mayor al mínimo
        if self.max_stock_input.value() > 0 and self.min_stock_input.value() > 0:
            if self.max_stock_input.value() < self.min_stock_input.value():
                QMessageBox.warning(self, "Error de Validación", "El stock máximo debe ser mayor al stock mínimo.")
                self.tabs.setCurrentIndex(2)
                return False
        
        return True
    
    def save_product(self):
        """Guarda el producto."""
        if not self.validate_form():
            return
        
        conn = conectar_db()
        cursor = conn.cursor()
        
        try:
            # Datos del producto
            product_data = {
                'codigo': self.code_input.text().strip(),
                'descripcion': self.description_input.text().strip(),
                'categoria': self.category_input.currentText().strip() or None,
                'proveedor': self.provider_input.text().strip() or None,
                'puesto_trabajo': self.position_input.text().strip() or None,
                'stock_actual': self.stock_input.value(),
                'unidad_medida': self.unit_input.currentText().strip() or None,
                'tipo_control': self.control_type_input.currentText().strip() or None,
                'stock_minimo': self.min_stock_input.value(),
                'stock_maximo': self.max_stock_input.value(),
                'observacion': self.observation_input.toPlainText().strip() or None
            }
            
            if self.is_editing:
                # Actualizar producto existente
                cursor.execute("""
                    UPDATE productos SET 
                    descripcion=?, categoria=?, proveedor=?, puesto_trabajo=?,
                    stock_actual=?, unidad_medida=?, tipo_control=?, 
                    stock_minimo=?, stock_maximo=?, observacion=?
                    WHERE codigo=?
                """, (
                    product_data['descripcion'], product_data['categoria'], 
                    product_data['proveedor'], product_data['puesto_trabajo'],
                    product_data['stock_actual'], product_data['unidad_medida'],
                    product_data['tipo_control'], product_data['stock_minimo'],
                    product_data['stock_maximo'], product_data['observacion'],
                    product_data['codigo']
                ))
            else:
                # Crear nuevo producto
                cursor.execute("""
                    INSERT INTO productos (
                        codigo, descripcion, categoria, proveedor, puesto_trabajo,
                        stock_actual, unidad_medida, tipo_control, stock_minimo, 
                        stock_maximo, observacion
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    product_data['codigo'], product_data['descripcion'],
                    product_data['categoria'], product_data['proveedor'],
                    product_data['puesto_trabajo'], product_data['stock_actual'],
                    product_data['unidad_medida'], product_data['tipo_control'],
                    product_data['stock_minimo'], product_data['stock_maximo'],
                    product_data['observacion']
                ))
            
            # Manejar ubicación
            self.save_location(cursor, product_data['codigo'])
            
            conn.commit()
            
            # Mostrar mensaje de éxito
            action = "actualizado" if self.is_editing else "creado"
            QMessageBox.information(
                self, 
                "Éxito", 
                f"El producto ha sido {action} correctamente."
            )
            
            self.accept()
            
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo guardar el producto:\n{str(e)}"
            )
        finally:
            conn.close()
    
    def save_location(self, cursor, codigo_producto):
        """Guarda la ubicación del producto."""
        # Datos de ubicación
        fila = self.row_input.value()
        columna = self.column_input.currentText().strip() or None
        estante = self.shelf_input.value()
        posicion = self.position_shelf_input.value()
        orientacion = self.orientation_input.currentText().strip() or None
        deposito = self.deposito_input.currentText().strip() or None
        sector = self.sector_input.currentText().strip() or None
        
        # Buscar si ya existe una ubicación igual
        cursor.execute("""
            SELECT id_ubicacion FROM ubicaciones 
            WHERE fila=? AND columna=? AND estante=? AND posicion=? AND orientacion=? AND deposito=? AND sector=?
        """, (fila, columna, estante, posicion, orientacion, deposito, sector))
        
        existing_location = cursor.fetchone()
        
        if existing_location:
            location_id = existing_location[0]
        else:
            # Crear nueva ubicación
            cursor.execute("""
                INSERT INTO ubicaciones (fila, columna, estante, posicion, orientacion, deposito, sector)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (fila, columna, estante, posicion, orientacion, deposito, sector))
            location_id = cursor.lastrowid
        
        # Eliminar relación existente si es edición
        if self.is_editing:
            cursor.execute("DELETE FROM producto_ubicacion WHERE codigo_producto=?", (codigo_producto,))
        
        # Crear nueva relación
        cursor.execute("""
            INSERT INTO producto_ubicacion (codigo_producto, id_ubicacion, cantidad)
            VALUES (?, ?, ?)
        """, (codigo_producto, location_id, self.stock_input.value()))


class AlertFormDialog(QDialog):
    """Diálogo moderno para crear alertas."""
    
    def __init__(self, parent=None, product_code=None):
        """
        Inicializa el diálogo de formulario de alerta.
        
        Args:
            parent: Widget padre
            product_code: Código del producto (opcional)
        """
        super().__init__(parent)
        
        self.product_code = product_code
        
        # Configurar diálogo
        self.setWindowTitle("Nueva Alerta")
        self.setMinimumSize(500, 400)
        self.setMaximumSize(700, 550)
        self.resize(550, 450)
        self.setModal(True)
        
        # Crear interfaz
        self.init_ui()
        
        # Si se proporcionó un código, buscarlo
        if product_code:
            self.product_input.setText(product_code)
            self.search_product()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Título
        title_label = QLabel("Nueva Alerta")
        title_label.setObjectName("dialogTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Grupo de producto
        product_group = QGroupBox("Producto")
        product_group.setObjectName("formGroup")
        product_layout = QVBoxLayout(product_group)
        
        # Búsqueda de producto
        search_layout = QHBoxLayout()
        self.product_input = QLineEdit()
        self.product_input.setObjectName("formInput")
        self.product_input.setPlaceholderText("Código del producto...")
        search_layout.addWidget(self.product_input)
        
        search_button = QPushButton("Buscar")
        search_button.setObjectName("searchButton")
        search_button.clicked.connect(self.search_product)
        search_layout.addWidget(search_button)
        
        product_layout.addLayout(search_layout)
        
        # Información del producto
        self.product_info_label = QLabel("Selecciona un producto para continuar")
        self.product_info_label.setObjectName("productInfo")
        self.product_info_label.setWordWrap(True)
        product_layout.addWidget(self.product_info_label)
        
        # Información de ubicación
        self.location_info_label = QLabel("")
        self.location_info_label.setObjectName("locationInfo")
        self.location_info_label.setWordWrap(True)
        product_layout.addWidget(self.location_info_label)
        
        layout.addWidget(product_group)
        
        # Grupo de alerta
        alert_group = QGroupBox("Información de la Alerta")
        alert_group.setObjectName("formGroup")
        alert_layout = QFormLayout(alert_group)
        alert_layout.setSpacing(15)
        
        # Tipo de alerta
        self.priority_combo = QComboBox()
        self.priority_combo.setObjectName("formCombo")
        self.priority_combo.addItems(["Alta prioridad", "Media", "Baja"])
        alert_layout.addRow("Prioridad:", self.priority_combo)
        
        # Razón
        self.reason_input = QLineEdit()
        self.reason_input.setObjectName("formInput")
        self.reason_input.setPlaceholderText("Motivo de la alerta...")
        alert_layout.addRow("Razón:", self.reason_input)
        
        # Detalles
        self.details_input = QTextEdit()
        self.details_input.setObjectName("formTextArea")
        self.details_input.setMaximumHeight(120)
        self.details_input.setPlaceholderText("Descripción detallada del problema o situación...")
        alert_layout.addRow("Detalles:", self.details_input)
        
        # Fecha programada
        self.date_input = QDateEdit()
        self.date_input.setObjectName("formDateEdit")
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        alert_layout.addRow("Fecha Programada:", self.date_input)
        
        layout.addWidget(alert_group)
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Crear Alerta")
        save_button.setObjectName("saveButton")
        save_button.clicked.connect(self.save_alert)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
        
        # Variables para almacenar datos del producto
        self.current_product = None
        self.current_location_id = None
    
    def search_product(self):
        """Busca el producto por código."""
        code = self.product_input.text().strip()
        if not code:
            return
        
        conn = conectar_db()
        cursor = conn.cursor()
        
        # Buscar producto
        cursor.execute("SELECT * FROM productos WHERE codigo = ?", (code,))
        product = cursor.fetchone()
        
        if product:
            self.current_product = {
                'codigo': product[0],
                'descripcion': product[1],
                'categoria': product[2],
                'proveedor': product[3],
                'stock_actual': product[5]
            }
            
            # Mostrar información del producto
            info_text = f"<b>{product[0]}</b> - {product[1]}"
            if product[2]:
                info_text += f"<br><i>Categoría: {product[2]}</i>"
            if product[3]:
                info_text += f"<br><i>Proveedor: {product[3]}</i>"
            info_text += f"<br><i>Stock actual: {product[5]} unidades</i>"
            
            self.product_info_label.setText(info_text)
            
            # Buscar ubicación
            cursor.execute("""
                SELECT u.*, pu.cantidad
                FROM ubicaciones u
                JOIN producto_ubicacion pu ON u.id_ubicacion = pu.id_ubicacion
                WHERE pu.codigo_producto = ?
                LIMIT 1
            """, (code,))
            location = cursor.fetchone()
            
            if location:
                self.current_location_id = location[0]
                location_text = f"<b>Ubicación:</b> Fila {location[1]}, Columna {location[2]}, Estante {location[3]}, Posición {location[4]}"
                if location[5]:
                    location_text += f" ({location[5]})"
                self.location_info_label.setText(location_text)
            else:
                self.location_info_label.setText("<i>Sin ubicación asignada</i>")
                self.current_location_id = None
        else:
            self.product_info_label.setText("❌ Producto no encontrado")
            self.location_info_label.setText("")
            self.current_product = None
            self.current_location_id = None
        
        conn.close()
    
    def save_alert(self):
        """Guarda la alerta."""
        # Validaciones
        if not self.current_product:
            QMessageBox.warning(self, "Producto Requerido", "Debe seleccionar un producto válido.")
            return
        
        if not self.reason_input.text().strip():
            QMessageBox.warning(self, "Razón Requerida", "Debe especificar la razón de la alerta.")
            return
        
        conn = conectar_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO alertas (
                    codigo_producto, id_ubicacion, tipo_alerta, razon, 
                    detalles, estado, fecha_inicio
                ) VALUES (?, ?, ?, ?, ?, 'sin iniciar', CURRENT_TIMESTAMP)
            """, (
                self.current_product['codigo'],
                self.current_location_id,
                self.priority_combo.currentText(),
                self.reason_input.text().strip(),
                self.details_input.toPlainText().strip()
            ))
            
            conn.commit()
            
            QMessageBox.information(
                self,
                "Alerta Creada",
                "La alerta ha sido creada correctamente."
            )
            
            self.accept()
            
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo crear la alerta:\n{str(e)}"
            )
        finally:
            conn.close()


class AlertDetailDialog(QDialog):
    """Diálogo para ver y editar detalles de una alerta."""
    
    def __init__(self, parent=None, alert_data=None):
        """
        Inicializa el diálogo de detalle de alerta.
        
        Args:
            parent: Widget padre
            alert_data: Tupla con datos de la alerta
        """
        super().__init__(parent)
        
        self.alert_data = alert_data
        self.alert_id = alert_data[0] if alert_data else None
        
        # Configurar diálogo
        self.setWindowTitle(f"Detalle de Alerta #{self.alert_id}")
        self.setMinimumSize(700, 600)
        self.setModal(True)
        
        # Crear interfaz
        self.init_ui()
        
        # Cargar datos
        if alert_data:
            self.load_alert_data()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Título
        title_label = QLabel(f"Alerta #{self.alert_id}")
        title_label.setObjectName("dialogTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Pestañas
        self.tabs = QTabWidget()
        self.tabs.setObjectName("dialogTabs")
        
        # Pestaña de información general
        self.create_general_tab()
        
        # Pestaña de seguimiento
        self.create_tracking_tab()
        
        # Pestaña de acciones
        self.create_actions_tab()
        
        layout.addWidget(self.tabs)
        
        # Botones
        self.create_buttons(layout)
    
    def create_general_tab(self):
        """Crea la pestaña de información general."""
        general_tab = QWidget()
        layout = QVBoxLayout(general_tab)
        layout.setSpacing(20)
        
        # Información del producto
        product_group = QGroupBox("Información del Producto")
        product_group.setObjectName("formGroup")
        product_layout = QFormLayout(product_group)
        product_layout.setSpacing(15)
        
        self.product_code_label = QLabel()
        self.product_code_label.setObjectName("infoDisplay")
        product_layout.addRow("Código:", self.product_code_label)
        
        self.product_name_label = QLabel()
        self.product_name_label.setObjectName("infoDisplay")
        self.product_name_label.setWordWrap(True)
        product_layout.addRow("Descripción:", self.product_name_label)
        
        self.location_label = QLabel()
        self.location_label.setObjectName("infoDisplay")
        self.location_label.setWordWrap(True)
        product_layout.addRow("Ubicación:", self.location_label)
        
        layout.addWidget(product_group)
        
        # Información de la alerta
        alert_group = QGroupBox("Información de la Alerta")
        alert_group.setObjectName("formGroup")
        alert_layout = QFormLayout(alert_group)
        alert_layout.setSpacing(15)
        
        self.priority_combo = QComboBox()
        self.priority_combo.setObjectName("formCombo")
        self.priority_combo.addItems(["Alta prioridad", "Media", "Baja"])
        alert_layout.addRow("Prioridad:", self.priority_combo)
        
        self.reason_input = QLineEdit()
        self.reason_input.setObjectName("formInput")
        alert_layout.addRow("Razón:", self.reason_input)
        
        self.details_input = QTextEdit()
        self.details_input.setObjectName("formTextArea")
        self.details_input.setMaximumHeight(120)
        alert_layout.addRow("Detalles:", self.details_input)
        
        self.creation_date_label = QLabel()
        self.creation_date_label.setObjectName("infoDisplay")
        alert_layout.addRow("Fecha de Creación:", self.creation_date_label)
        
        layout.addWidget(alert_group)
        layout.addStretch()
        
        self.tabs.addTab(general_tab, "Información General")
    
    def create_tracking_tab(self):
        """Crea la pestaña de seguimiento."""
        tracking_tab = QWidget()
        layout = QVBoxLayout(tracking_tab)
        layout.setSpacing(20)
        
        # Estado actual
        status_group = QGroupBox("Estado Actual")
        status_group.setObjectName("formGroup")
        status_layout = QFormLayout(status_group)
        status_layout.setSpacing(15)
        
        self.status_combo = QComboBox()
        self.status_combo.setObjectName("formCombo")
        self.status_combo.addItems([
            "sin iniciar", "en progreso", "esperando material", 
            "completada", "cancelada"
        ])
        status_layout.addRow("Estado:", self.status_combo)
        
        self.assigned_to_input = QLineEdit()
        self.assigned_to_input.setObjectName("formInput")
        self.assigned_to_input.setPlaceholderText("Nombre del responsable...")
        status_layout.addRow("Asignado a:", self.assigned_to_input)
        
        self.estimated_date_input = QDateEdit()
        self.estimated_date_input.setObjectName("formDateEdit")
        self.estimated_date_input.setDate(QDate.currentDate())
        self.estimated_date_input.setCalendarPopup(True)
        status_layout.addRow("Fecha Estimada:", self.estimated_date_input)
        
        layout.addWidget(status_group)
        
        # Notas de seguimiento
        notes_group = QGroupBox("Notas de Seguimiento")
        notes_group.setObjectName("formGroup")
        notes_layout = QVBoxLayout(notes_group)
        
        self.tracking_notes = QTextEdit()
        self.tracking_notes.setObjectName("formTextArea")
        self.tracking_notes.setPlaceholderText(
            "Registra aquí las acciones tomadas, comunicaciones con proveedores, "
            "actualizaciones de estado, etc..."
        )
        notes_layout.addWidget(self.tracking_notes)
        
        layout.addWidget(notes_group)
        layout.addStretch()
        
        self.tabs.addTab(tracking_tab, "Seguimiento")
    
    def create_actions_tab(self):
        """Crea la pestaña de acciones."""
        actions_tab = QWidget()
        layout = QVBoxLayout(actions_tab)
        layout.setSpacing(20)
        
        # Acciones rápidas
        quick_actions_group = QGroupBox("Acciones Rápidas")
        quick_actions_group.setObjectName("formGroup")
        quick_layout = QVBoxLayout(quick_actions_group)
        
        # Botones de cambio de estado rápido
        status_buttons_layout = QGridLayout()
        
        self.btn_en_progreso = QPushButton("🔄 Marcar En Progreso")
        self.btn_en_progreso.setObjectName("statusButton")
        self.btn_en_progreso.clicked.connect(lambda: self.cambiar_estado_rapido("en progreso"))
        status_buttons_layout.addWidget(self.btn_en_progreso, 0, 0)
        
        self.btn_esperando = QPushButton("⏳ Esperando Material")
        self.btn_esperando.setObjectName("statusButton")
        self.btn_esperando.clicked.connect(lambda: self.cambiar_estado_rapido("esperando material"))
        status_buttons_layout.addWidget(self.btn_esperando, 0, 1)
        
        self.btn_completar = QPushButton("✅ Completar")
        self.btn_completar.setObjectName("statusButton")
        self.btn_completar.clicked.connect(lambda: self.cambiar_estado_rapido("completada"))
        status_buttons_layout.addWidget(self.btn_completar, 1, 0)
        
        self.btn_cancelar_alerta = QPushButton("❌ Cancelar Alerta")
        self.btn_cancelar_alerta.setObjectName("statusButton")
        self.btn_cancelar_alerta.clicked.connect(lambda: self.cambiar_estado_rapido("cancelada"))
        status_buttons_layout.addWidget(self.btn_cancelar_alerta, 1, 1)
        
        quick_layout.addLayout(status_buttons_layout)
        layout.addWidget(quick_actions_group)
        
        # Historial de cambios (placeholder)
        history_group = QGroupBox("Historial de Cambios")
        history_group.setObjectName("formGroup")
        history_layout = QVBoxLayout(history_group)
        
        self.history_display = QTextEdit()
        self.history_display.setObjectName("historyDisplay")
        self.history_display.setReadOnly(True)
        self.history_display.setMaximumHeight(200)
        history_layout.addWidget(self.history_display)
        
        layout.addWidget(history_group)
        layout.addStretch()
        
        self.tabs.addTab(actions_tab, "Acciones")
    
    def create_buttons(self, layout):
        """Crea los botones del diálogo."""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Botón cerrar
        close_button = QPushButton("Cerrar")
        close_button.setObjectName("cancelButton")
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)
        
        # Botón guardar cambios
        save_button = QPushButton("Guardar Cambios")
        save_button.setObjectName("saveButton")
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
    
    def load_alert_data(self):
        """Carga los datos de la alerta en el formulario."""
        if not self.alert_data:
            return
        
        # Datos: id, tipo_alerta, codigo_producto, descripcion, razon, estado, fecha_inicio, ubicacion, detalles
        self.product_code_label.setText(self.alert_data[2] or "N/A")
        self.product_name_label.setText(self.alert_data[3] or "N/A")
        self.location_label.setText(self.alert_data[7] or "Sin ubicación")
        
        # Prioridad
        if self.alert_data[1]:
            index = self.priority_combo.findText(self.alert_data[1])
            if index >= 0:
                self.priority_combo.setCurrentIndex(index)
        
        self.reason_input.setText(self.alert_data[4] or "")
        self.details_input.setText(self.alert_data[8] or "")
        self.creation_date_label.setText(self.alert_data[6] or "N/A")
        
        # Estado
        if self.alert_data[5]:
            index = self.status_combo.findText(self.alert_data[5])
            if index >= 0:
                self.status_combo.setCurrentIndex(index)
        
        # Cargar historial (placeholder)
        self.history_display.setText(
            f"Alerta creada: {self.alert_data[6]}\n"
            f"Estado actual: {self.alert_data[5]}\n"
            f"Prioridad: {self.alert_data[1]}"
        )
    
    def cambiar_estado_rapido(self, nuevo_estado):
        """Cambia rápidamente el estado de la alerta."""
        respuesta = QMessageBox.question(
            self,
            "Confirmar Cambio",
            f"¿Cambiar el estado de la alerta a '{nuevo_estado}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            self.status_combo.setCurrentText(nuevo_estado)
            self.save_changes()
    
    def save_changes(self):
        """Guarda los cambios realizados."""
        try:
            from data.database import conectar_db
            conn = conectar_db()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE alertas SET 
                    tipo_alerta = ?, razon = ?, detalles = ?, estado = ?
                WHERE id_alerta = ?
            """, (
                self.priority_combo.currentText(),
                self.reason_input.text().strip(),
                self.details_input.toPlainText().strip(),
                self.status_combo.currentText(),
                self.alert_id
            ))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Cambios Guardados", "Los cambios han sido guardados correctamente.")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron guardar los cambios:\n{e}")


class QuickStateChangeDialog(QDialog):
    """Diálogo rápido para cambiar el estado de una alerta."""
    
    def __init__(self, parent=None, alert_id=None):
        """
        Inicializa el diálogo de cambio rápido de estado.
        
        Args:
            parent: Widget padre
            alert_id: ID de la alerta
        """
        super().__init__(parent)
        
        self.alert_id = alert_id
        
        # Configurar diálogo
        self.setWindowTitle("Cambio Rápido de Estado")
        self.setFixedSize(400, 300)
        self.setModal(True)
        
        # Crear interfaz
        self.init_ui()
        
        # Cargar estado actual
        self.load_current_state()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel(f"Cambiar Estado - Alerta #{self.alert_id}")
        title_label.setObjectName("dialogTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Estado actual
        self.current_state_label = QLabel("Estado actual: Cargando...")
        self.current_state_label.setObjectName("infoDisplay")
        layout.addWidget(self.current_state_label)
        
        # Nuevo estado
        form_layout = QFormLayout()
        
        self.new_state_combo = QComboBox()
        self.new_state_combo.setObjectName("formCombo")
        self.new_state_combo.addItems([
            "sin iniciar", "en progreso", "esperando material", 
            "completada", "cancelada"
        ])
        form_layout.addRow("Nuevo Estado:", self.new_state_combo)
        
        # Nota del cambio
        self.change_note_input = QTextEdit()
        self.change_note_input.setObjectName("formTextArea")
        self.change_note_input.setMaximumHeight(80)
        self.change_note_input.setPlaceholderText("Nota sobre el cambio (opcional)...")
        form_layout.addRow("Nota:", self.change_note_input)
        
        layout.addLayout(form_layout)
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Cambiar Estado")
        save_button.setObjectName("saveButton")
        save_button.clicked.connect(self.change_state)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
    
    def load_current_state(self):
        """Carga el estado actual de la alerta."""
        try:
            from data.database import conectar_db
            conn = conectar_db()
            cursor = conn.cursor()
            
            cursor.execute("SELECT estado FROM alertas WHERE id_alerta = ?", (self.alert_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                current_state = result[0]
                self.current_state_label.setText(f"Estado actual: {current_state}")
                
                # Establecer el estado actual como seleccionado
                index = self.new_state_combo.findText(current_state)
                if index >= 0:
                    self.new_state_combo.setCurrentIndex(index)
            
        except Exception as e:
            self.current_state_label.setText("Error al cargar estado actual")
    
    def change_state(self):
        """Cambia el estado de la alerta."""
        try:
            from data.database import conectar_db
            conn = conectar_db()
            cursor = conn.cursor()
            
            nuevo_estado = self.new_state_combo.currentText()
            nota = self.change_note_input.toPlainText().strip()
            
            cursor.execute("""
                UPDATE alertas SET estado = ? WHERE id_alerta = ?
            """, (nuevo_estado, self.alert_id))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(
                self, 
                "Estado Actualizado", 
                f"El estado de la alerta ha sido cambiado a '{nuevo_estado}'"
            )
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cambiar el estado:\n{e}")