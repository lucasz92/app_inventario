# 📋 Instrucciones de Uso - Gestor de Inventario

## 🚀 Inicio Rápido

### Opción 1: Inicio Simple
```bash
python main.py
```

### Opción 2: Inicio con Verificaciones
```bash
python iniciar_aplicacion.py
```

### Opción 3: Con Datos de Ejemplo
```bash
python insertar_datos_ejemplo.py
python main.py
```

## 📖 Guía de Uso por Pestañas

### 🏷️ Pestaña "Productos"

**Funciones principales:**
- **Ver productos**: La tabla muestra todos los productos con sus ubicaciones
- **Buscar**: Usa el campo de búsqueda para filtrar en tiempo real
- **Seleccionar**: Haz clic en una fila para ver detalles en el panel derecho

**Botones de acción:**
- **🟢 Agregar Producto**: Abre formulario para crear nuevo producto
- **🟡 Modificar Producto**: Edita el producto seleccionado
- **🔴 Eliminar Producto**: Elimina el producto seleccionado (con confirmación)

**Campos del formulario:**
- Código (obligatorio, máx. 20 caracteres)
- Descripción (obligatorio)
- Categoría, Proveedor, Puesto (opcionales)
- Stock actual, mínimo, máximo (números)
- Unidad de medida, Tipo de control
- Observaciones

### 🔍 Pestaña "Búsqueda Avanzada"

**Filtros disponibles:**
- **Código**: Busca por parte del código
- **Descripción**: Busca en la descripción del producto
- **Proveedor**: Filtra por proveedor
- **Tipo de Control**: Filtra por tipo de control

**Uso:**
1. Completa uno o más campos de filtro
2. Haz clic en "Buscar"
3. Los resultados aparecen en la tabla inferior

### 🚨 Pestaña "Alertas"

**Crear nueva alerta:**
1. Ingresa el código del producto
2. Haz clic en "Buscar producto" para verificar
3. Selecciona el tipo de prioridad (Alta, Media, Baja)
4. Escribe la razón de la alerta
5. Agrega detalles adicionales
6. Haz clic en "Guardar alerta"

**Ver alertas:**
- La tabla inferior muestra todas las alertas activas
- Incluye información del producto y ubicación
- Estados: sin iniciar, en progreso, completada, cancelada

### ⚙️ Pestaña "Configuración"

**Importar datos:**
1. Haz clic en "Importar"
2. Selecciona un archivo Excel (.xlsx)
3. El archivo debe tener hojas: productos, ubicaciones, alertas
4. Los datos se cargan automáticamente

**Exportar datos:**
1. Haz clic en "Exportar"
2. Elige la ubicación y nombre del archivo
3. Se crea un Excel con todas las tablas

## 🗂️ Formato de Archivos Excel

### Hoja "productos"
| codigo | descripcion | categoria | proveedor | puesto_trabajo | stock_actual | unidad_medida | tipo_control | stock_minimo | stock_maximo | observacion |

### Hoja "ubicaciones"
| id_ubicacion | fila | columna | estante | posicion | orientacion |

### Hoja "alertas"
| id_alerta | codigo_producto | id_ubicacion | tipo_alerta | razon | detalles | estado | fecha_inicio | fecha_fin |

## 🔧 Solución de Problemas

### Error: "Archivo de estilos no encontrado"
- Verifica que existe el archivo `ui/styles.qss`
- Ejecuta desde el directorio raíz del proyecto

### Error: "Base de datos no encontrada"
- La aplicación crea automáticamente la BD en `data/inventario.db`
- Verifica permisos de escritura en la carpeta `data/`

### Error: "Dependencias faltantes"
```bash
pip install -r requirements.txt
```

### Error al importar Excel
- Verifica que el archivo tenga las hojas correctas
- Revisa que las columnas coincidan con la estructura esperada
- Usa el archivo `ejemplo_importacion.xlsx` como referencia

## 🧪 Ejecutar Pruebas

```bash
python test_aplicacion.py
```

## 📊 Datos de Ejemplo

Para cargar datos de prueba:
```bash
python insertar_datos_ejemplo.py
```

Esto crea:
- 8 productos de ejemplo
- 8 ubicaciones
- 3 alertas de prueba

## 🎨 Personalización

### Cambiar estilos
Edita el archivo `ui/styles.qss` para modificar:
- Colores de la interfaz
- Fuentes y tamaños
- Espaciado y bordes

### Configuración
Modifica `config.py` para cambiar:
- Tamaño de ventana
- Rutas de archivos
- Mensajes de la aplicación
- Validaciones

## 📝 Notas Importantes

1. **Códigos únicos**: Cada producto debe tener un código único
2. **Backup automático**: Se recomienda hacer backups regulares de `data/inventario.db`
3. **Formato de fechas**: Las fechas se muestran en formato DD/MM/YYYY HH:MM
4. **Búsqueda**: La búsqueda no distingue mayúsculas/minúsculas
5. **Eliminación**: La eliminación de productos es permanente (con confirmación)

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs de error en la consola
2. Ejecuta las pruebas para verificar la integridad
3. Verifica que todos los archivos estén presentes
4. Consulta la documentación en `README.md`