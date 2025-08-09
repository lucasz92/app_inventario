# tab_productos.py
import re

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import Qt


from data.database import obtener_productos_con_ubicacion, obtener_detalles_producto, buscar_productos

class TabProductos(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

# --- [crear_buscador]: layout con QLineEdit y botones

    def init_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setObjectName("layout_principal")  # Este es el layout vertical principal

        # Panel superior: tabla + detalles
        panel_superior = QHBoxLayout()
        panel_superior.setObjectName("panel_superior")  # Este es el layout horizontal superior
        # Panel izquierdo: tabla y buscador
        panel_izquierdo = QVBoxLayout()
        panel_izquierdo.setObjectName("panel_izquierdo")  # Este es el layout vertical izquierdo
        titulo = QLabel("Listado de Productos")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_izquierdo.addWidget(titulo)
        panel_izquierdo.addLayout(self.buscador())
        panel_izquierdo.addWidget(self.crear_tabla())

        # Panel derecho: detalles
        self.panel_derecho = QVBoxLayout()
        self.panel_derecho.setObjectName("panel_derecho")
        self.detalles_label = QLabel("Más información del producto")
        self.detalles_label.setObjectName("detalles_label")
        self.panel_derecho.addWidget(self.detalles_label)
        self.detalles_campos = {}

        for campo in ["Proveedor", "Tipo", "Max/Min", "Categoría", "Puesto", "Observación"]:
            label = QLabel(f"{campo}:")
            label.setFont(QFont("Sego UI", 11))
            self.panel_derecho.addWidget(label)
            self.detalles_campos[campo] = label

        # Agregar paneles izquierdo y derecho al panel superior
        panel_superior.addLayout(panel_izquierdo, 3)
        panel_superior.addLayout(self.panel_derecho, 2)

        # Panel inferior: botones
        self.panel_inferior = QHBoxLayout()
        self.panel_inferior.addStretch(1)
        self.panel_inferior.addStretch(1)

        # Agregar todo al layout principal
        layout_principal.addLayout(panel_superior)
        btnEliminar = QPushButton("Eliminar Producto")
        btnEliminar.setObjectName("btnEliminar")
        btnModificar = QPushButton("Modificar Producto")
        btnModificar.setObjectName("btnModificar")
        btnAgregar = QPushButton("Agregar Producto")
        btnAgregar.setObjectName("btnAgregar")
        
        self.panel_inferior.addWidget(btnAgregar)
        self.panel_inferior.addWidget(btnModificar)
        self.panel_inferior.addWidget(btnEliminar)
        
        layout_principal.addLayout(self.panel_inferior)
        datos_iniciales = obtener_productos_con_ubicacion()
        actualizar_tabla(self.tabla, datos_iniciales)


    def buscador(self):
        layout = QHBoxLayout()
        buscador_label = QLabel("Buscar producto:")
        buscador_label.setFont(QFont("Segoe UI", 12))

        self.buscador_textbox = QLineEdit()
        self.buscador_textbox.setObjectName("buscador")
        self.buscador_textbox.setPlaceholderText("Escribe el nombre del producto...")

        self.buscador_textbox.textChanged.connect(self.filtrar_tabla)

        layout.addWidget(buscador_label)
        layout.addWidget(self.buscador_textbox)
        layout.addStretch(1)
        return layout
    

    def filtrar_tabla(self, texto):
        texto = str(texto).strip()
        if texto:
            datos_filtrados = buscar_productos(texto)
        else:
            datos_filtrados = obtener_productos_con_ubicacion()
        actualizar_tabla(self.tabla, datos_filtrados)



    def crear_tabla(self):
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(8)
        anchos = [100, 200, 80, 80, 80, 80, 80, 80]
        for i, ancho in enumerate(anchos):
            self.tabla.setColumnWidth(i, ancho)

        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setObjectName("tabla")
        self.tabla.setHorizontalHeaderLabels([
            "Código", "Descripción", "Fila", "Columna", "Estante",
            "Ubicación", "Depósito", "Sector"
        ])
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.cellClicked.connect(self.mostrar_detalles_producto)
        actualizar_tabla(self.tabla, [])  # ← ahora es función externa
        return self.tabla


    def cargar_tabla_productos_con_ubicacion(self):
        datos = obtener_productos_con_ubicacion()
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
            for i, valor in enumerate(detalles):
                self.detalles_campos[campos[i]].setText(f"{campos[i]}: {valor}")
                

def actualizar_tabla(tabla, datos):
    tabla.setRowCount(0)
    tabla.setRowCount(len(datos))

    for fila_idx, fila in enumerate(datos):
        for col_idx, valor in enumerate(fila):
            item = QTableWidgetItem(str(valor))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tabla.setItem(fila_idx, col_idx, item)
