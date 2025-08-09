Ventana Principal (main.py)
    crea la ventana 
    crea las pestañas necesarias

    -logica para mostrar la primer pestaña-

    pestaña 1 
        funcion que llama al widget_herramienta_productos 
            "Muestra una ventana con las siguientes caracteristicas y funciones para buscar y mostrar 
             información sobre el producto, ubicaciones, etc, --- crea registros en la base de datos, sistema CRUD"

             Elementos, caracteristicas y disposición del layout:

             [Productos] - Busqueda Avanzada - Alertas - Información

             1. Caja para buscar - /* Por código o descripcion */ - [Importar] - [Exportar] |----------------------|
             2. Tabla
                [codigo][descripción][fila][columna][estante][ubicacion][deposito][sector]  |  más infor del prod. |


                        /* función que llama a la funcion correspondite para la carga de datos en database.py */
            
            4. Botones [Agregar][Modificar][Eliminar]

    pestaña 2 
        funcion que llama al widget_herramienta_busqueda avanzada
        "Muestra una ventana con una herramienta más especifica para encontrar productos
    pestaña 3
        funcion que llama al widget_herramienta_alertas
    pestaña 4
        funcion que llama a widget_herramienta_información(kpi's)

#En PROCESO
