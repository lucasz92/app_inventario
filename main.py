import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QTabWidget
from PyQt6.QtCore import Qt
from tabs.tab_productos import TabProductos
from tabs.tab_busqueda_avanzada import TabBusquedaAvanzada
from tabs.tab_alertas import TabAlertas
from tabs.tab_configuracion import TabConfiguracion
from data.database import inicializar_db
from config import WINDOW_TITLE, STYLES_PATH


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        inicializar_db()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, 1400, 800)
        self.setMinimumSize(1200, 700)

        # Layout principal sin márgenes
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Header
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

        # Contenido principal
        contenido_widget = QWidget()
        contenido_widget.setStyleSheet("background: #F5F5F5;")
        contenido_layout = QVBoxLayout(contenido_widget)
        contenido_layout.setContentsMargins(0, 0, 0, 0)
        contenido_layout.setSpacing(0)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setObjectName("tabs")

        self.tab_productos = TabProductos()
        self.tab_configuracion = TabConfiguracion(self.tab_productos.tabla)
        self.tab_busqueda_avanzada = TabBusquedaAvanzada()
        self.tab_alertas = TabAlertas()

        self.tabs.addTab(self.tab_productos, "📦 Productos")
        self.tabs.addTab(self.tab_busqueda_avanzada, "🔍 Búsqueda Avanzada")
        self.tabs.addTab(self.tab_alertas, "⚠️ Alertas")
        self.tabs.addTab(self.tab_configuracion, "⚙️ Configuración")

        self.tabs.setCurrentIndex(0)

        contenido_layout.addWidget(self.tabs)
        layout_principal.addWidget(contenido_widget)

        # Central widget
        widget_central = QWidget()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)


def crear_aplicacion():
    app = QApplication(sys.argv)

    # Cargar QSS desde STYLES_PATH
    qss_path = Path(STYLES_PATH)
    if qss_path.exists():
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Archivo de estilos no encontrado: {qss_path}")

    ventana = VentanaPrincipal()
    ventana.show()
    return app


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargar estilos
    from pathlib import Path
    from config import STYLES_PATH
    qss_path = Path(STYLES_PATH)
    if qss_path.exists():
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(app.exec())
