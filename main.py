#!/usr/bin/env python3
"""
Sistema de Boleta Electrónica para Negocio de Informática
Aplicación de escritorio con PyQt6 para gestión de boletas electrónicas
"""
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Función principal de la aplicación"""
    app = QApplication(sys.argv)
    
    # Configurar el estilo de la aplicación
    app.setStyle('Fusion')
    
    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar el loop de la aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
