# 🧠 Diseño modular: Pestaña "Gestión de Inventario"

## 🎯 Propósito del módulo
Esta pestaña mostrará todos los productos cargados. Incluye:
- Un buscador por nombre/código/proveedor
- Botones para importar y exportar datos
- Una tabla con los resultados
- Posible integración futura con alertas, filtros avanzados y wiki

---

## 🧱 Estructura de clase: `TabProductos`

### 1. Constructor `__init__`
- Instancia la clase
- Llama a `init_ui()` para construir la interfaz

### 2. `init_ui()`
Responsable de ensamblar visualmente los componentes. Llama a:
- `crear_titulo()`
- `crear_buscador()`
- `crear_tabla()`

### 3. `crear_titulo()`
- Devuelve `QLabel` con estilo, fuente y centrado

### 4. `crear_buscador()`
- Devuelve `QHBoxLayout` con:
  - `QLineEdit` para búsqueda
  - Botón "Importar"
  - Botón "Exportar"
- Conecta el evento `textChanged` al método `filtrar_productos(texto)`

### 5. `crear_tabla()`
- Devuelve `QTableWidget` con los productos obtenidos desde `database.py`
- Guarda la tabla como `self.tabla` para poder modificarla luego

### 6. `filtrar_productos(texto)`
- Filtra dinámicamente los productos en la tabla según el texto ingresado

---

## 🔗 Conexión con módulos externos

- **`database.py`**: Proporciona la función `obtener_productos()` que retorna una lista de tuplas con los datos
- **`inject_test_data.py`**: Script para precargar productos en la base `inventario.db`

---

## 🧪 Posibles mejoras

- Agregar validación de entrada en el buscador
- Implementar importación desde archivo CSV
- Estilizar la tabla con íconos y tooltips
- Agregar un botón "Agregar producto nuevo"