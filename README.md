# Sistema de Boleta Electrónica

Sistema de escritorio para gestión de boletas electrónicas para negocios de informática, desarrollado con PyQt6.

## 📋 Características

- ✅ Interfaz gráfica moderna y fácil de usar
- ✅ Gestión completa de boletas electrónicas
- ✅ Administración de clientes
- ✅ Generación automática de PDFs profesionales
- ✅ Cálculo automático de IVA (19%)
- ✅ Base de datos SQLite integrada
- ✅ Búsqueda de boletas por cliente
- ✅ Numeración automática de boletas
- ✅ Historial completo de transacciones

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Ignaciohub/boletaelectronica.git
   cd boletaelectronica
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o
   venv\Scripts\activate  # En Windows
   ```

3. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

## 📁 Estructura del Proyecto

```
BOLETA ELECTRONICA/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── boletas.db             # Base de datos SQLite (se crea automáticamente)
│
├── models/                # Modelos de datos
│   ├── __init__.py
│   ├── boleta.py         # Modelo de boleta e items
│   └── cliente.py        # Modelo de cliente
│
├── ui/                    # Interfaz de usuario
│   ├── __init__.py
│   ├── main_window.py    # Ventana principal
│   └── nueva_boleta_dialog.py  # Diálogo para crear boletas
│
├── database/             # Gestión de base de datos
│   ├── __init__.py
│   └── db_manager.py     # Manager de SQLite
│
├── utils/                # Utilidades
│   ├── __init__.py
│   └── pdf_generator.py  # Generador de PDFs
│
└── resources/            # Recursos (imágenes, iconos, etc.)
```

## 💻 Uso de la Aplicación

### Crear una Nueva Boleta

1. Haz clic en el botón **"Nueva Boleta"** en la ventana principal
2. Ingresa el RUT del cliente y haz clic en **"Buscar"**
   - Si el cliente existe, sus datos se cargarán automáticamente
   - Si no existe, puedes registrarlo completando el formulario
3. Agrega productos/servicios:
   - Descripción del producto o servicio
   - Cantidad
   - Precio unitario
   - Haz clic en **"Agregar"**
4. Repite el paso 3 para agregar más items
5. Opcionalmente, agrega observaciones
6. Haz clic en **"Guardar Boleta"**

### Generar PDF de una Boleta

1. Selecciona una boleta de la lista
2. Haz clic en **"Ver PDF"**
3. Elige la ubicación donde guardar el archivo
4. El PDF se generará automáticamente

### Buscar Boletas

1. En el campo de búsqueda, ingresa el RUT del cliente
2. Haz clic en **"Buscar"**
3. Se mostrarán todas las boletas asociadas a ese cliente

### Ver Clientes Registrados

1. Haz clic en la pestaña **"Clientes"**
2. Verás la lista completa de clientes registrados

## 🔧 Configuración

### Personalizar Información del Negocio

Para personalizar la información que aparece en las boletas PDF, edita el archivo `utils/pdf_generator.py` y modifica los parámetros por defecto en el método `generar_boleta_pdf()`:

```python
nombre_negocio = "Tu Negocio de Informática"
rut_negocio = "12.345.678-9"
direccion_negocio = "Tu Dirección"
telefono_negocio = "+56 9 XXXX XXXX"
```

## 📦 Dependencias

- **PyQt6**: Framework de interfaz gráfica
- **reportlab**: Generación de PDFs
- **pillow**: Procesamiento de imágenes
- SQLite3: Base de datos (incluida en Python)

## 🛠️ Desarrollo

### Agregar Nuevas Funcionalidades

El proyecto está estructurado de manera modular:

- **Modelos**: Agrega nuevos modelos en `models/`
- **UI**: Crea nuevas ventanas/diálogos en `ui/`
- **Base de datos**: Extiende `DatabaseManager` en `database/db_manager.py`
- **Utilidades**: Agrega funciones auxiliares en `utils/`

## 🐛 Solución de Problemas

### Error al instalar PyQt6

Si tienes problemas instalando PyQt6:
```bash
pip install --upgrade pip
pip install PyQt6 --no-cache-dir
```

### La aplicación no inicia

Verifica que todas las dependencias estén instaladas:
```bash
pip install -r requirements.txt --force-reinstall
```

### Error con la base de datos

Si hay problemas con la base de datos, elimina el archivo `boletas.db` y ejecuta la aplicación nuevamente. Se creará una nueva base de datos vacía.

## 📝 Características Futuras

- [ ] Exportar boletas a Excel
- [ ] Respaldo automático de base de datos
- [ ] Estadísticas y reportes
- [ ] Envío de boletas por email
- [ ] Múltiples formatos de impresión
- [ ] Gestión de inventario
- [ ] Control de pagos y deudas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Autor

Desarrollado para negocios de informática que necesitan una solución simple y efectiva para gestionar boletas electrónicas.

## 📞 Soporte

Si tienes preguntas o necesitas ayuda, por favor abre un issue en el repositorio de GitHub.

---

**¡Gracias por usar el Sistema de Boleta Electrónica!** 🎉
