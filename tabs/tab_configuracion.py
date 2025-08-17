
# tab_configuracion.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
    QLineEdit, QPushButton, QFileDialog, QMessageBox, QGroupBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from data.database import exportar_a_excel, importar_desde_excel, obtener_productos_con_ubicacion
from tabs.tab_productos import actualizar_tabla

class TabConfiguracion(QWidget):
    def __init__(self, tabla_productos=None):
        super().__init__()
        self.tabla_productos = tabla_productos
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título
        title_label = QLabel("Configuración del Sistema")
        title_label.setObjectName("sectionTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Grupo de importación/exportación
        io_group = QGroupBox("Importación y Exportación de Datos")
        io_group.setObjectName("configGroup")
        io_layout = QVBoxLayout(io_group)
        io_layout.setSpacing(15)

        # Descripción
        desc_label = QLabel("Gestiona la importación y exportación de datos del inventario en formato Excel.")
        desc_label.setObjectName("descriptionLabel")
        desc_label.setWordWrap(True)
        io_layout.addWidget(desc_label)

        # Botones de importar/exportar
        buttons_layout = QHBoxLayout()
        
        self.boton_importar = QPushButton("📥 Importar desde Excel")
        self.boton_importar.setObjectName("importButton")
        self.boton_importar.clicked.connect(self.importar_excel)
        buttons_layout.addWidget(self.boton_importar)
        
        self.boton_exportar = QPushButton("📤 Exportar a Excel")
        self.boton_exportar.setObjectName("exportButton")
        self.boton_exportar.clicked.connect(self.exportar_excel)
        buttons_layout.addWidget(self.boton_exportar)
        
        buttons_layout.addStretch()
        io_layout.addLayout(buttons_layout)

        layout.addWidget(io_group)

        # Grupo de estadísticas
        stats_group = QGroupBox("Estadísticas del Sistema")
        stats_group.setObjectName("configGroup")
        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(15)

        # Etiquetas de estadísticas
        self.stats_productos = QLabel("Productos: Cargando...")
        self.stats_productos.setObjectName("statLabel")
        stats_layout.addWidget(self.stats_productos)

        self.stats_ubicaciones = QLabel("Ubicaciones: Cargando...")
        self.stats_ubicaciones.setObjectName("statLabel")
        stats_layout.addWidget(self.stats_ubicaciones)

        self.stats_alertas = QLabel("Alertas activas: Cargando...")
        self.stats_alertas.setObjectName("statLabel")
        stats_layout.addWidget(self.stats_alertas)

        self.stats_stock_bajo = QLabel("Productos con stock bajo: Cargando...")
        self.stats_stock_bajo.setObjectName("statLabel")
        stats_layout.addWidget(self.stats_stock_bajo)

        # Botón actualizar estadísticas
        refresh_button = QPushButton("🔄 Actualizar Estadísticas")
        refresh_button.setObjectName("refreshButton")
        refresh_button.clicked.connect(self.actualizar_estadisticas)
        stats_layout.addWidget(refresh_button)

        layout.addWidget(stats_group)

        # Grupo de mantenimiento
        maintenance_group = QGroupBox("Mantenimiento de la Base de Datos")
        maintenance_group.setObjectName("configGroup")
        maintenance_layout = QVBoxLayout(maintenance_group)
        maintenance_layout.setSpacing(15)

        maintenance_desc = QLabel("Herramientas para el mantenimiento y optimización de la base de datos.")
        maintenance_desc.setObjectName("descriptionLabel")
        maintenance_desc.setWordWrap(True)
        maintenance_layout.addWidget(maintenance_desc)

        maintenance_buttons = QHBoxLayout()
        
        backup_button = QPushButton("💾 Crear Respaldo")
        backup_button.setObjectName("backupButton")
        backup_button.clicked.connect(self.crear_respaldo)
        maintenance_buttons.addWidget(backup_button)

        optimize_button = QPushButton("⚡ Optimizar BD")
        optimize_button.setObjectName("optimizeButton")
        optimize_button.clicked.connect(self.optimizar_bd)
        maintenance_buttons.addWidget(optimize_button)

        maintenance_buttons.addStretch()
        maintenance_layout.addLayout(maintenance_buttons)

        layout.addWidget(maintenance_group)
        layout.addStretch()

        # Cargar estadísticas iniciales
        self.actualizar_estadisticas()
    
    def importar_excel(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Importar Excel", "", "Archivos Excel (*.xlsx)")
        if ruta:
            try:
                importar_desde_excel(ruta)
                QMessageBox.information(self, "Importación", "Datos importados correctamente.")
                # Recargar los datos desde la BD para mostrar en la tabla
                datos = obtener_productos_con_ubicacion()
                actualizar_tabla(self.tabla_productos, datos)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo importar el archivo:\n{e}")


    def exportar_excel(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Exportar Excel", "", "Archivos Excel (*.xlsx)")
        if ruta:
            try:
                exportar_a_excel(ruta)
                QMessageBox.information(self, "Exportación", "Datos exportados correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo:\n{e}")

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas del sistema."""
        try:
            from data.database import conectar_db
            conn = conectar_db()
            cursor = conn.cursor()

            # Contar productos
            cursor.execute("SELECT COUNT(*) FROM productos")
            total_productos = cursor.fetchone()[0]
            self.stats_productos.setText(f"📦 Productos registrados: {total_productos}")

            # Contar ubicaciones
            cursor.execute("SELECT COUNT(*) FROM ubicaciones")
            total_ubicaciones = cursor.fetchone()[0]
            self.stats_ubicaciones.setText(f"📍 Ubicaciones disponibles: {total_ubicaciones}")

            # Contar alertas activas
            cursor.execute("SELECT COUNT(*) FROM alertas WHERE estado != 'completada'")
            alertas_activas = cursor.fetchone()[0]
            self.stats_alertas.setText(f"⚠️ Alertas activas: {alertas_activas}")

            # Productos con stock bajo
            cursor.execute("""
                SELECT COUNT(*) FROM productos 
                WHERE stock_actual > 0 AND stock_minimo > 0 AND stock_actual < stock_minimo
            """)
            stock_bajo = cursor.fetchone()[0]
            self.stats_stock_bajo.setText(f"📉 Productos con stock bajo: {stock_bajo}")

            conn.close()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar las estadísticas:\n{e}")

    def crear_respaldo(self):
        """Crea un respaldo de la base de datos."""
        try:
            from utils import crear_backup_db
            import os
            
            db_path = "data/inventario.db"
            if not os.path.exists(db_path):
                QMessageBox.warning(self, "Error", "No se encontró la base de datos.")
                return

            backup_path = crear_backup_db(db_path)
            QMessageBox.information(
                self, 
                "Respaldo Creado", 
                f"El respaldo se ha creado correctamente en:\n{backup_path}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear el respaldo:\n{e}")

    def optimizar_bd(self):
        """Optimiza la base de datos."""
        try:
            from data.database import conectar_db
            
            respuesta = QMessageBox.question(
                self,
                "Optimizar Base de Datos",
                "¿Deseas optimizar la base de datos? Este proceso puede tomar unos minutos.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                conn = conectar_db()
                cursor = conn.cursor()
                
                # Ejecutar comandos de optimización
                cursor.execute("VACUUM")
                cursor.execute("ANALYZE")
                
                conn.close()
                
                QMessageBox.information(
                    self,
                    "Optimización Completada",
                    "La base de datos ha sido optimizada correctamente."
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo optimizar la base de datos:\n{e}")
