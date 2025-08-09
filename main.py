import sys
import os
from PyQt6.QtWidgets import QLabel, QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTabWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from tabs.tab_productos import TabProductos
from tabs.tab_configuracion import TabConfiguracion
from data.database import inicializar_db

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        inicializar_db()
        self.aplicar_estilos()
        self.setWindowTitle("Gestor de Productos")
        self.setGeometry(100, 100, 1200, 750)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        titulo = QLabel("Gestor de Productos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont("Sego UI", 16, weight=QFont.Weight.Bold))
        titulo.setStyleSheet("color: #333; padding: 5px;")
        layout.addWidget(titulo)

        # Configurar el layoutu

        self.tabs = QTabWidget()
        self.tab_productos = TabProductos()
        self.tab_configuracion = TabConfiguracion(self.tab_productos.tabla)
        self.tabs.addTab(self.tab_productos, "Productos")
        self.tabs.addTab(self.crear_pestaña("busqueda_avanzada"), "Búsqueda avanzada")
        self.tabs.addTab(self.crear_pestaña("alertas"), "Alertas")
        self.tabs.addTab(self.tab_configuracion, "Configuración")
        layout.addWidget(self.tabs)
        # Crear un widget central y establecer el layout
        widget_central = QWidget()
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)


    def aplicar_estilos(self):
        try:
                with open("ui/styles.qss", "r") as archivo_estilos:
                        estilo = archivo_estilos.read()
                        self.setStyleSheet(estilo)
        except FileNotFoundError:
                print("Archivo de estilos no encontrado.")

        
    def crear_pestaña(self, tipo: str) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        contenido = {
                "busqueda_avanzada": QPushButton("Búsqueda avanzada"),
                "alertas": QPushButton("Alertas"),
                "configuracion": QPushButton("Configuración")
        }

        if tipo == "productos":
                return TabProductos()
        elif tipo in contenido:
                layout.addWidget(contenido[tipo])
                return widget
        else:
                layout.addWidget(QLabel("Pestaña no definida"))
                return widget

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())