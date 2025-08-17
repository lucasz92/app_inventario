"""
Utilidades comunes para la aplicación Gestor de Inventario
"""

import os
import shutil
from datetime import datetime

def crear_backup_db(ruta_db, carpeta_backup="backups"):
    """
    Crea un backup de la base de datos
    
    Args:
        ruta_db: Ruta de la base de datos
        carpeta_backup: Carpeta donde guardar el backup
    
    Returns:
        str: Ruta del archivo de backup creado
    """
    if not os.path.exists(carpeta_backup):
        os.makedirs(carpeta_backup)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_backup = f"inventario_backup_{timestamp}.db"
    ruta_backup = os.path.join(carpeta_backup, nombre_backup)
    
    shutil.copy2(ruta_db, ruta_backup)
    return ruta_backup