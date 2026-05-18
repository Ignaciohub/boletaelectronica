#!/bin/bash
# Script de instalación y ejecución rápida

echo "=========================================="
echo "Sistema de Boleta Electrónica - Instalador"
echo "=========================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

echo ""

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Instalación completada"
echo "=========================================="
echo ""
echo "Para ejecutar la aplicación:"
echo "  1. Activa el entorno virtual: source venv/bin/activate"
echo "  2. Ejecuta: python main.py"
echo ""
echo "O simplemente ejecuta: ./run.sh"
echo ""
