# tab_alertas.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt
import sqlite3
from data.database import conectar_db

class TabAlertas(QWidget):
    def __init__(self):
        super().__init__()
        self.db_path = "data/inventario.db"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título
        title_label = QLabel("Sistema de Gestión de Alertas")
        title_label.setObjectName("sectionTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Panel de filtros y acciones
        filter_group = QGroupBox("Filtros y Acciones")
        filter_group.setObjectName("alertFilterGroup")
        filter_layout = QGridLayout(filter_group)
        filter_layout.setSpacing(15)

        # Filtro por texto
        filter_layout.addWidget(QLabel("Buscar:"), 0, 0)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por código, descripción, razón...")
        self.search_input.setObjectName("alertSearchInput")
        self.search_input.textChanged.connect(self.filtrar_alertas)
        filter_layout.addWidget(self.search_input, 0, 1, 1, 2)

        # Filtro por estado
        filter_layout.addWidget(QLabel("Estado:"), 1, 0)
        self.estado_filter = QComboBox()
        self.estado_filter.setObjectName("alertStateFilter")
        self.estado_filter.addItems([
            "Todos los estados", "Sin iniciar", "En progreso", 
            "Esperando material", "Completada", "Cancelada"
        ])
        self.estado_filter.currentTextChanged.connect(self.filtrar_alertas)
        filter_layout.addWidget(self.estado_filter, 1, 1)

        # Filtro por prioridad
        filter_layout.addWidget(QLabel("Prioridad:"), 1, 2)
        self.prioridad_filter = QComboBox()
        self.prioridad_filter.setObjectName("alertPriorityFilter")
        self.prioridad_filter.addItems([
            "Todas las prioridades", "Alta prioridad", "Media", "Baja"
        ])
        self.prioridad_filter.currentTextChanged.connect(self.filtrar_alertas)
        filter_layout.addWidget(self.prioridad_filter, 1, 3)

        # Botones de acción
        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.btn_nueva_alerta = QPushButton("+ Nueva Alerta")
        self.btn_nueva_alerta.setObjectName("newAlertButton")
        self.btn_nueva_alerta.clicked.connect(self.nueva_alerta)
        action_layout.addWidget(self.btn_nueva_alerta)

        self.btn_actualizar = QPushButton("🔄 Actualizar")
        self.btn_actualizar.setObjectName("refreshAlertButton")
        self.btn_actualizar.clicked.connect(self.cargar_alertas)
        action_layout.addWidget(self.btn_actualizar)

        filter_layout.addLayout(action_layout, 2, 0, 1, 4)

        layout.addWidget(filter_group)

        # Estadísticas rápidas
        stats_layout = QHBoxLayout()
        
        self.stats_total = QLabel("Total: 0")
        self.stats_total.setObjectName("alertStat")
        stats_layout.addWidget(self.stats_total)

        self.stats_alta = QLabel("Alta: 0")
        self.stats_alta.setObjectName("alertStatHigh")
        stats_layout.addWidget(self.stats_alta)

        self.stats_pendientes = QLabel("Pendientes: 0")
        self.stats_pendientes.setObjectName("alertStatPending")
        stats_layout.addWidget(self.stats_pendientes)

        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        # Tabla de alertas mejorada
        self.tabla_alertas = QTableWidget()
        self.tabla_alertas.setObjectName("tabla_alertas")
        self.tabla_alertas.setColumnCount(8)
        self.tabla_alertas.setHorizontalHeaderLabels([
            "ID", "Prioridad", "Código", "Producto", "Razón", 
            "Estado", "Fecha Creación", "Ubicación"
        ])
        
        # Configurar tabla
        self.tabla_alertas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_alertas.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabla_alertas.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_alertas.setAlternatingRowColors(True)
        self.tabla_alertas.verticalHeader().setVisible(False)
        
        # Configurar anchos de columna
        header = self.tabla_alertas.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # Prioridad
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # Código
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Producto
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Razón
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Estado
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Fecha
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)  # Ubicación
        
        self.tabla_alertas.setColumnWidth(0, 50)   # ID
        self.tabla_alertas.setColumnWidth(1, 100)  # Prioridad
        self.tabla_alertas.setColumnWidth(2, 100)  # Código

        # Conectar eventos
        self.tabla_alertas.cellDoubleClicked.connect(self.ver_detalle_alerta)
        self.tabla_alertas.keyPressEvent = self.handle_key_press

        layout.addWidget(self.tabla_alertas)

        # Botones de acción para alertas seleccionadas
        table_actions = QHBoxLayout()
        table_actions.addStretch()

        self.btn_ver_detalle = QPushButton("Ver Detalle")
        self.btn_ver_detalle.setObjectName("viewAlertButton")
        self.btn_ver_detalle.clicked.connect(self.ver_detalle_alerta)
        table_actions.addWidget(self.btn_ver_detalle)

        self.btn_cambiar_estado = QPushButton("Cambiar Estado")
        self.btn_cambiar_estado.setObjectName("changeStateButton")
        self.btn_cambiar_estado.clicked.connect(self.cambiar_estado_rapido)
        table_actions.addWidget(self.btn_cambiar_estado)

        layout.addLayout(table_actions)

        # Cargar datos iniciales
        self.alertas_data = []
        self.cargar_alertas()

    def cargar_alertas(self):
        """Carga todas las alertas desde la base de datos."""
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    a.id_alerta,
                    a.tipo_alerta,
                    a.codigo_producto,
                    p.descripcion,
                    a.razon,
                    a.estado,
                    a.fecha_inicio,
                    CASE 
                        WHEN u.fila IS NOT NULL THEN 
                            'Fila ' || u.fila || ', Col ' || COALESCE(u.columna, '') || 
                            ', Est ' || COALESCE(u.estante, '') || ', Pos ' || COALESCE(u.posicion, '')
                        ELSE 'Sin ubicación'
                    END as ubicacion,
                    a.detalles
                FROM alertas a
                LEFT JOIN productos p ON a.codigo_producto = p.codigo
                LEFT JOIN ubicaciones u ON a.id_ubicacion = u.id_ubicacion
                ORDER BY 
                    CASE a.tipo_alerta 
                        WHEN 'Alta prioridad' THEN 1 
                        WHEN 'Media' THEN 2 
                        WHEN 'Baja' THEN 3 
                    END,
                    a.fecha_inicio DESC
            """)
            self.alertas_data = cursor.fetchall()
            conn.close()
            
            self.actualizar_tabla()
            self.actualizar_estadisticas()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las alertas:\n{e}")

    def actualizar_tabla(self):
        """Actualiza la tabla con los datos filtrados."""
        # Aplicar filtros
        alertas_filtradas = self.aplicar_filtros()
        
        self.tabla_alertas.setRowCount(0)
        
        for alerta in alertas_filtradas:
            row_pos = self.tabla_alertas.rowCount()
            self.tabla_alertas.insertRow(row_pos)
            
            # ID
            item = QTableWidgetItem(str(alerta[0]))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_alertas.setItem(row_pos, 0, item)
            
            # Prioridad con color
            prioridad_item = QTableWidgetItem(alerta[1])
            prioridad_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Aplicar colores usando QColor para mayor compatibilidad
            from PyQt6.QtGui import QColor
            if alerta[1] == "Alta prioridad":
                prioridad_item.setBackground(QColor(220, 38, 38))  # Rojo
                prioridad_item.setForeground(QColor(255, 255, 255))  # Blanco
            elif alerta[1] == "Media":
                prioridad_item.setBackground(QColor(251, 191, 36))  # Amarillo
                prioridad_item.setForeground(QColor(0, 0, 0))  # Negro
            else:  # Baja
                prioridad_item.setBackground(QColor(34, 197, 94))  # Verde
                prioridad_item.setForeground(QColor(255, 255, 255))  # Blanco
            
            self.tabla_alertas.setItem(row_pos, 1, prioridad_item)
            
            # Código
            codigo_item = QTableWidgetItem(alerta[2] or "")
            codigo_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_alertas.setItem(row_pos, 2, codigo_item)
            
            # Producto
            self.tabla_alertas.setItem(row_pos, 3, QTableWidgetItem(alerta[3] or ""))
            
            # Razón
            self.tabla_alertas.setItem(row_pos, 4, QTableWidgetItem(alerta[4] or ""))
            
            # Estado con color
            estado_item = QTableWidgetItem(alerta[5] or "")
            estado_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if alerta[5] == "sin iniciar":
                estado_item.setBackground(Qt.GlobalColor.lightGray)
            elif alerta[5] == "en progreso":
                estado_item.setBackground(Qt.GlobalColor.cyan)
            elif alerta[5] == "esperando material":
                estado_item.setBackground(Qt.GlobalColor.yellow)
            elif alerta[5] == "solucionado":
                estado_item.setBackground(Qt.GlobalColor.green)
                estado_item.setForeground(Qt.GlobalColor.white)
            elif alerta[5] == "cancelado":
                estado_item.setBackground(Qt.GlobalColor.darkGray)
                estado_item.setForeground(Qt.GlobalColor.white)
            self.tabla_alertas.setItem(row_pos, 5, estado_item)
            
            # Fecha
            fecha_item = QTableWidgetItem(alerta[6] or "")
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla_alertas.setItem(row_pos, 6, fecha_item)
            
            # Ubicación
            self.tabla_alertas.setItem(row_pos, 7, QTableWidgetItem(alerta[7] or ""))

    def aplicar_filtros(self):
        """Aplica los filtros seleccionados a los datos."""
        if not self.alertas_data:
            return []
        
        alertas_filtradas = self.alertas_data.copy()
        
        # Filtro por texto
        texto_busqueda = self.search_input.text().strip().lower()
        if texto_busqueda:
            alertas_filtradas = [
                alerta for alerta in alertas_filtradas
                if (texto_busqueda in str(alerta[2]).lower() or  # código
                    texto_busqueda in str(alerta[3]).lower() or  # descripción
                    texto_busqueda in str(alerta[4]).lower())    # razón
            ]
        
        # Filtro por estado
        estado_filtro = self.estado_filter.currentText()
        if estado_filtro != "Todos los estados":
            estado_map = {
                "Sin iniciar": "sin iniciar",
                "En progreso": "en progreso",
                "Esperando material": "esperando material",
                "Completada": "completada",
                "Cancelada": "cancelada"
            }
            estado_bd = estado_map.get(estado_filtro, estado_filtro.lower())
            alertas_filtradas = [
                alerta for alerta in alertas_filtradas
                if alerta[5] == estado_bd
            ]
        
        # Filtro por prioridad
        prioridad_filtro = self.prioridad_filter.currentText()
        if prioridad_filtro != "Todas las prioridades":
            alertas_filtradas = [
                alerta for alerta in alertas_filtradas
                if alerta[1] == prioridad_filtro
            ]
        
        return alertas_filtradas

    def filtrar_alertas(self):
        """Actualiza la tabla cuando cambian los filtros."""
        self.actualizar_tabla()
        self.actualizar_estadisticas()

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas mostradas."""
        alertas_filtradas = self.aplicar_filtros()
        
        total = len(alertas_filtradas)
        alta_prioridad = len([a for a in alertas_filtradas if a[1] == "Alta prioridad"])
        pendientes = len([a for a in alertas_filtradas if a[5] in ["sin iniciar", "en progreso"]])
        
        self.stats_total.setText(f"Total: {total}")
        self.stats_alta.setText(f"Alta: {alta_prioridad}")
        self.stats_pendientes.setText(f"Pendientes: {pendientes}")

    def handle_key_press(self, event):
        """Maneja las teclas presionadas en la tabla."""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.ver_detalle_alerta()
        else:
            # Llamar al método original
            QTableWidget.keyPressEvent(self.tabla_alertas, event)

    def ver_detalle_alerta(self):
        """Muestra el detalle de la alerta seleccionada."""
        fila_actual = self.tabla_alertas.currentRow()
        if fila_actual < 0:
            QMessageBox.warning(self, "Selección Requerida", "Selecciona una alerta para ver sus detalles.")
            return
        
        # Obtener ID de la alerta
        id_item = self.tabla_alertas.item(fila_actual, 0)
        if not id_item:
            return
        
        alert_id = int(id_item.text())
        
        # Buscar los datos completos de la alerta
        alerta_data = None
        for alerta in self.alertas_data:
            if alerta[0] == alert_id:
                alerta_data = alerta
                break
        
        if not alerta_data:
            QMessageBox.warning(self, "Error", "No se encontraron los datos de la alerta.")
            return
        
        # Abrir diálogo de detalle
        from tabs.dialogs import AlertDetailDialog
        dialog = AlertDetailDialog(self, alerta_data)
        if dialog.exec() == AlertDetailDialog.DialogCode.Accepted:
            self.cargar_alertas()

    def cambiar_estado_rapido(self):
        """Permite cambiar rápidamente el estado de una alerta."""
        fila_actual = self.tabla_alertas.currentRow()
        if fila_actual < 0:
            QMessageBox.warning(self, "Selección Requerida", "Selecciona una alerta para cambiar su estado.")
            return
        
        # Obtener ID de la alerta
        id_item = self.tabla_alertas.item(fila_actual, 0)
        if not id_item:
            return
        
        alert_id = int(id_item.text())
        
        # Mostrar diálogo de cambio de estado
        from tabs.dialogs import QuickStateChangeDialog
        dialog = QuickStateChangeDialog(self, alert_id)
        if dialog.exec() == QuickStateChangeDialog.DialogCode.Accepted:
            self.cargar_alertas()

    def nueva_alerta(self):
        """Abre el diálogo para crear una nueva alerta."""
        from tabs.dialogs import AlertFormDialog
        
        dialog = AlertFormDialog(self)
        if dialog.exec() == AlertFormDialog.DialogCode.Accepted:
            self.cargar_alertas()