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
        self.setGeometry(100, 100, 1400, 800)
        self.setMinimumSize(1200, 700)

        # Layout principal sin márgenes para diseño limpio
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Header con título principal
        header_widget = QWidget()
        header_widget.setObjectName("header_widget")
        header_widget.setStyleSheet("""
            QWidget#header_widget {
                background: #FFFFFF;
                border-bottom: 1px solid #E1E7EC;
                min-height: 80px;
                max-height: 80px;
            }
        """)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(32, 0, 32, 0)
        
        titulo = QLabel("Gestor de Productos")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(titulo)
        header_layout.addStretch()
        
        layout_principal.addWidget(header_widget)

        # Área de contenido principal
        contenido_widget = QWidget()
        contenido_widget.setStyleSheet("background: #F5F5F5;")
        contenido_layout = QVBoxLayout(contenido_widget)
        contenido_layout.setContentsMargins(0, 0, 0, 0)
        contenido_layout.setSpacing(0)

        # Configurar las pestañas con estilo mejorado
        self.tabs = QTabWidget()
      

        # Instanciar las pestañas
        self.tab_productos = TabProductos()
        self.tab_configuracion = TabConfiguracion(self.tab_productos.tabla)
        self.tab_busqueda_avanzada = TabBusquedaAvanzada()
        self.tab_alertas = TabAlertas()

        # Añadir las pestañas al QTabWidget con iconos
        self.tabs.addTab(self.tab_productos, "📦 Productos")
        self.tabs.addTab(self.tab_busqueda_avanzada, "🔍 Búsqueda Avanzada")
        self.tabs.addTab(self.tab_alertas, "⚠️ Alertas")
        self.tabs.addTab(self.tab_configuracion, "⚙️ Configuración")
        
        # Establecer la primera pestaña como activa
        self.tabs.setCurrentIndex(0)

        contenido_layout.addWidget(self.tabs)
        layout_principal.addWidget(contenido_widget)

        # Crear widget central
        widget_central = QWidget()
        widget_central.setLayout(layout_principal)
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