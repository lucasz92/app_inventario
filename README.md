# 📦 Gestor de Inventario

Una aplicación de escritorio desarrollada en Python con PyQt6 para la gestión completa de inventarios de productos.

## 🚀 Características

### ✨ **Nuevas Mejoras UI/UX**
- **Diálogos Modernos**: Formularios con pestañas para productos y alertas
- **Validación en Tiempo Real**: Indicadores visuales de estado y errores
- **Búsqueda Inteligente**: Filtros avanzados con autocompletado
- **Panel de Estadísticas**: Métricas del sistema en tiempo real
- **Herramientas de Mantenimiento**: Respaldos y optimización integrados

### 📦 **Gestión de Productos**
- Agregar, modificar, eliminar y buscar productos
- Formulario con pestañas (Información Básica, Ubicación, Stock)
- Validación inteligente de campos obligatorios
- Indicadores visuales de estado de stock

### 📍 **Sistema de Ubicaciones**
- Ubicación por filas, columnas, estantes y posiciones
- Selector de ubicaciones existentes
- Información contextual de ubicación

### 🔍 **Búsqueda Avanzada**
- Filtros múltiples por código, descripción, proveedor, categoría
- Estados de stock (Con stock, Sin stock, Stock bajo)
- Tabla de resultados con acciones contextuales
- Contador dinámico de resultados

### ⚠️ **Sistema de Alertas**
- Gestión de alertas por producto con diferentes prioridades
- Diálogo especializado para crear alertas
- Búsqueda integrada de productos
- Información contextual del producto seleccionado

### 📊 **Importación/Exportación**
- Soporte completo para archivos Excel (.xlsx)
- Interfaz mejorada con iconos y descripciones
- Validación de archivos antes de importar

### 🎨 **Interfaz Moderna**
- Diseño limpio y profesional con estilos personalizados
- Sistema de colores coherente
- Efectos hover y estados interactivos
- Tipografía y espaciado optimizados

## 📋 Requisitos

- Python 3.8+
- PyQt6
- openpyxl
- sqlite3 (incluido en Python)

## 🛠️ Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd app_inventario
```

2. Instala las dependencias:
```bash
pip install PyQt6 openpyxl
```

3. Ejecuta la aplicación:
```bash
python main.py
```

## 📊 Estructura del Proyecto

```
app_inventario/
├── main.py                    # Archivo principal de la aplicación
├── data/
│   ├── database.py           # Gestión de base de datos SQLite
│   └── inventario.db         # Base de datos (se crea automáticamente)
├── tabs/
│   ├── tab_productos.py      # Pestaña de gestión de productos
│   ├── tab_busqueda_avanzada.py  # Pestaña de búsqueda avanzada
│   ├── tab_alertas.py        # Pestaña de gestión de alertas
│   └── tab_configuracion.py  # Pestaña de configuración e importación/exportación
├── ui/
│   └── styles.qss           # Estilos CSS para la interfaz
└── insertar_datos_ejemplo.py # Script para datos de prueba
```

## 🎯 Uso

### Pestaña Productos
- **Ver productos**: Lista todos los productos con sus ubicaciones
- **Buscar**: Filtro en tiempo real por código, descripción o ubicación
- **Agregar**: Diálogo moderno con pestañas para crear nuevos productos
  - Información básica con validación
  - Configuración de ubicación con selector
  - Gestión de stock con indicadores visuales
- **Modificar**: Edición completa con formulario prellenado
- **Eliminar**: Eliminación segura con confirmación
- **Detalles**: Panel lateral que muestra información detallada del producto seleccionado

### Pestaña Búsqueda Avanzada
- **Filtros Inteligentes**: Código, descripción, categoría, proveedor, tipo de control
- **Estados de Stock**: Filtrar por productos con stock, sin stock, o stock bajo
- **Resultados Detallados**: Tabla con información completa y ubicación
- **Acciones Directas**: Ver detalles y editar productos desde los resultados
- **Contador Dinámico**: Muestra el número de productos encontrados

### Pestaña Alertas
- **Nueva Alerta**: Diálogo moderno con búsqueda integrada de productos
- **Información Contextual**: Muestra detalles del producto y ubicación
- **Niveles de Prioridad**: Alta, Media, Baja con colores distintivos
- **Seguimiento Completo**: Estado de las alertas y fechas programadas
- **Vista Unificada**: Tabla con todas las alertas activas y su información

### Pestaña Configuración
- **Importación/Exportación**: Interfaz mejorada con iconos y descripciones
  - Importar datos desde archivos Excel con validación
  - Exportar todos los datos en formato Excel
- **Estadísticas del Sistema**: Métricas en tiempo real
  - Contador de productos, ubicaciones y alertas
  - Productos con stock bajo
  - Actualización manual de estadísticas
- **Mantenimiento de BD**: Herramientas integradas
  - Crear respaldos automáticos
  - Optimizar base de datos
  - Operaciones seguras con confirmación

## 🗄️ Base de Datos

La aplicación utiliza SQLite con las siguientes tablas:

- **productos**: Información básica de productos
- **ubicaciones**: Sistema de ubicación física
- **producto_ubicacion**: Relación productos-ubicaciones
- **alertas**: Sistema de alertas y seguimiento

## 🎨 Personalización

Los estilos se encuentran en `ui/styles.qss` y pueden modificarse para cambiar:
- Colores de la interfaz
- Fuentes y tamaños
- Espaciado y márgenes
- Efectos hover y focus

## 📝 Datos de Ejemplo

Para probar la aplicación con datos de ejemplo, ejecuta:
```bash
python insertar_datos_ejemplo.py
```

Esto creará productos, ubicaciones y alertas de prueba.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
