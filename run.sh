#!/bin/bash
# Script para ejecutar la aplicación

# Activar entorno virtual
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Entorno virtual no encontrado"
    echo "Ejecuta primero: ./install.sh"
    exit 1
fi

# Ejecutar aplicación
echo "🚀 Iniciando Sistema de Boleta Electrónica..."
python main.py
