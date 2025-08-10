
# tab_configuracion.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QFileDialog, QMessageBox

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import Qt

from data.database import exportar_a_excel, importar_desde_excel
from tabs.tab_productos import actualizar_tabla

class TabConfiguracion(QWidget):
    def __init__(self, tabla_productos=None):
        super().__init__()
        self.tabla_productos = tabla_productos

        layout = QVBoxLayout(self)
        self.label = QLabel("Configuración")
        self.label.setFont(QFont("Arial", 16))
        layout.addWidget(self.label)
        layout.addLayout(self.iniciar_iu())

    def iniciar_iu(self):
        layout = QHBoxLayout()
        
        # Agregar botones de importar y exportar
        self.boton_importar = QPushButton("Importar")
        self.boton_exportar = QPushButton("Exportar")
        self.boton_importar.clicked.connect(self.importar_excel)
        self.boton_exportar.clicked.connect(self.exportar_excel)
        layout.addWidget(self.boton_importar)
        layout.addWidget(self.boton_exportar)
        return layout
    
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
