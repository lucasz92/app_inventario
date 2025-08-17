import sys
import os
from PyQt6.QtWidgets import QLabel, QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTabWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from tabs.tab_productos import TabProductos
from tabs.tab_busqueda_avanzada import TabBusquedaAvanzada
from tabs.tab_alertas import TabAlertas
from tabs.tab_configuracion import TabConfiguracion
from data.database import inicializar_db
from config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, STYLES_PATH

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        inicializar_db()
        self.aplicar_estilos()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, 1250, 400)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        titulo = QLabel("Gestor de Productos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont("Sego UI", 16, weight=QFont.Weight.Bold))
        titulo.setStyleSheet("color: #333; padding: 5px;")
        layout.addWidget(titulo)

        # Configurar las pestañas
        self.tabs = QTabWidget()

        # Instanciar las pestañas
        self.tab_productos = TabProductos()
        self.tab_configuracion = TabConfiguracion(self.tab_productos.tabla)
        self.tab_busqueda_avanzada = TabBusquedaAvanzada()
        self.tab_alertas = TabAlertas()

        # Añadir las pestañas al QTabWidget en el orden solicitado
        self.tabs.addTab(self.tab_productos, "Productos")
        self.tabs.addTab(self.tab_busqueda_avanzada, "Búsqueda Avanzada")
        self.tabs.addTab(self.tab_alertas, "Alertas")
        self.tabs.addTab(self.tab_configuracion, "Configuración")

        # Agregar las pestañas al layout principal
        layout.addWidget(self.tabs)

        # Crear un widget central y establecer el layout
        widget_central = QWidget()
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)


    def aplicar_estilos(self):
        try:
                with open(STYLES_PATH, "r", encoding="utf-8") as archivo_estilos:
                        estilo = archivo_estilos.read()
                        self.setStyleSheet(estilo)
        except FileNotFoundError:
                print(f"Archivo de estilos no encontrado: {STYLES_PATH}")

        


    


def crear_aplicacion():
    """Función para crear la aplicación y ventana principal"""
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    return app, ventana

if __name__ == "__main__":
    app, ventana = crear_aplicacion()
    ventana.show()
    sys.exit(app.exec())