"""Diálogo para crear una nueva boleta"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QTextEdit, QHeaderView, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QDoubleValidator, QIntValidator
from datetime import datetime
from database.db_manager import DatabaseManager
from models.boleta import Boleta, ItemBoleta
from models.cliente import Cliente


class NuevaBoletaDialog(QDialog):
    """Diálogo para crear una nueva boleta"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.items = []
        self.init_ui()
        self.cargar_numero_boleta()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Nueva Boleta Electrónica")
        self.setModal(True)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Crear Nueva Boleta")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Información de la boleta
        info_group = QGroupBox("Información de Boleta")
        info_layout = QFormLayout()
        
        self.numero_input = QLineEdit()
        self.numero_input.setReadOnly(True)
        info_layout.addRow("N° Boleta:", self.numero_input)
        
        self.fecha_label = QLabel(datetime.now().strftime("%d/%m/%Y %H:%M"))
        info_layout.addRow("Fecha:", self.fecha_label)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Información del cliente
        cliente_group = QGroupBox("Información del Cliente")
        cliente_layout = QFormLayout()
        
        # RUT del cliente
        rut_layout = QHBoxLayout()
        self.rut_input = QLineEdit()
        self.rut_input.setPlaceholderText("Ej: 12345678-9")
        btn_buscar_cliente = QPushButton("Buscar")
        btn_buscar_cliente.clicked.connect(self.buscar_cliente)
        rut_layout.addWidget(self.rut_input)
        rut_layout.addWidget(btn_buscar_cliente)
        cliente_layout.addRow("RUT:", rut_layout)
        
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo del cliente")
        cliente_layout.addRow("Nombre:", self.nombre_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("correo@ejemplo.com")
        cliente_layout.addRow("Email:", self.email_input)
        
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("+56 9 1234 5678")
        cliente_layout.addRow("Teléfono:", self.telefono_input)
        
        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText("Dirección del cliente")
        cliente_layout.addRow("Dirección:", self.direccion_input)
        
        cliente_group.setLayout(cliente_layout)
        layout.addWidget(cliente_group)
        
        # Items de la boleta
        items_group = QGroupBox("Productos/Servicios")
        items_layout = QVBoxLayout()
        
        # Formulario para agregar items
        form_layout = QHBoxLayout()
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Descripción del producto/servicio")
        form_layout.addWidget(QLabel("Descripción:"))
        form_layout.addWidget(self.desc_input, 3)
        
        self.cant_input = QLineEdit()
        self.cant_input.setPlaceholderText("1")
        self.cant_input.setValidator(QIntValidator(1, 9999))
        form_layout.addWidget(QLabel("Cant:"))
        form_layout.addWidget(self.cant_input, 1)
        
        self.precio_input = QLineEdit()
        self.precio_input.setPlaceholderText("10000")
        validator = QDoubleValidator(0.0, 999999999.99, 2)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.precio_input.setValidator(validator)
        form_layout.addWidget(QLabel("Precio:"))
        form_layout.addWidget(self.precio_input, 1)
        
        btn_agregar_item = QPushButton("Agregar")
        btn_agregar_item.clicked.connect(self.agregar_item)
        btn_agregar_item.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        form_layout.addWidget(btn_agregar_item)
        
        items_layout.addLayout(form_layout)
        
        # Tabla de items
        self.tabla_items = QTableWidget()
        self.tabla_items.setColumnCount(5)
        self.tabla_items.setHorizontalHeaderLabels([
            "Descripción", "Cantidad", "Precio Unit.", "Subtotal", "Acción"
        ])
        self.tabla_items.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tabla_items.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        items_layout.addWidget(self.tabla_items)
        
        items_group.setLayout(items_layout)
        layout.addWidget(items_group)
        
        # Totales
        totales_layout = QHBoxLayout()
        totales_layout.addStretch()
        
        self.subtotal_label = QLabel("Subtotal: $0")
        self.iva_label = QLabel("IVA (19%): $0")
        self.total_label = QLabel("TOTAL: $0")
        
        total_font = QFont()
        total_font.setPointSize(12)
        total_font.setBold(True)
        self.total_label.setFont(total_font)
        
        totales_layout.addWidget(self.subtotal_label)
        totales_layout.addWidget(QLabel(" | "))
        totales_layout.addWidget(self.iva_label)
        totales_layout.addWidget(QLabel(" | "))
        totales_layout.addWidget(self.total_label)
        
        layout.addLayout(totales_layout)
        
        # Observaciones
        obs_layout = QVBoxLayout()
        obs_layout.addWidget(QLabel("Observaciones (opcional):"))
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMaximumHeight(80)
        self.observaciones_input.setPlaceholderText("Notas adicionales sobre la boleta...")
        obs_layout.addWidget(self.observaciones_input)
        layout.addLayout(obs_layout)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        btn_guardar = QPushButton("Guardar Boleta")
        btn_guardar.clicked.connect(self.guardar_boleta)
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        
        buttons_layout.addWidget(btn_cancelar)
        buttons_layout.addWidget(btn_guardar)
        
        layout.addLayout(buttons_layout)
    
    def cargar_numero_boleta(self):
        """Carga el siguiente número de boleta disponible"""
        numero = self.db_manager.obtener_siguiente_numero_boleta()
        self.numero_input.setText(numero)
    
    def buscar_cliente(self):
        """Busca un cliente por RUT y llena los campos"""
        rut = self.rut_input.text().strip()
        if not rut:
            QMessageBox.warning(self, "Advertencia", "Ingrese un RUT")
            return
        
        cliente = self.db_manager.buscar_cliente_por_rut(rut)
        if cliente:
            self.nombre_input.setText(cliente.nombre)
            self.email_input.setText(cliente.email)
            self.telefono_input.setText(cliente.telefono)
            self.direccion_input.setText(cliente.direccion)
            QMessageBox.information(self, "Cliente encontrado", 
                                   f"Cliente {cliente.nombre} cargado")
        else:
            respuesta = QMessageBox.question(
                self,
                "Cliente no encontrado",
                "El cliente no existe. ¿Desea registrarlo?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta == QMessageBox.StandardButton.Yes:
                self.nombre_input.setFocus()
    
    def agregar_item(self):
        """Agrega un item a la tabla"""
        descripcion = self.desc_input.text().strip()
        cantidad_str = self.cant_input.text().strip()
        precio_str = self.precio_input.text().strip()
        
        if not descripcion or not cantidad_str or not precio_str:
            QMessageBox.warning(self, "Advertencia", 
                              "Complete todos los campos del item")
            return
        
        try:
            cantidad = int(cantidad_str)
            precio = float(precio_str)
            
            if cantidad <= 0 or precio <= 0:
                raise ValueError("Los valores deben ser positivos")
            
            item = ItemBoleta(descripcion, cantidad, precio)
            self.items.append(item)
            
            # Agregar a la tabla
            row = self.tabla_items.rowCount()
            self.tabla_items.insertRow(row)
            
            self.tabla_items.setItem(row, 0, QTableWidgetItem(item.descripcion))
            self.tabla_items.setItem(row, 1, QTableWidgetItem(str(item.cantidad)))
            self.tabla_items.setItem(row, 2, QTableWidgetItem(f"${item.precio_unitario:,.0f}"))
            self.tabla_items.setItem(row, 3, QTableWidgetItem(f"${item.subtotal:,.0f}"))
            
            # Botón eliminar
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.clicked.connect(lambda: self.eliminar_item(row))
            btn_eliminar.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    padding: 3px 10px;
                    border-radius: 3px;
                }
            """)
            self.tabla_items.setCellWidget(row, 4, btn_eliminar)
            
            # Limpiar campos
            self.desc_input.clear()
            self.cant_input.clear()
            self.precio_input.clear()
            self.desc_input.setFocus()
            
            # Actualizar totales
            self.actualizar_totales()
            
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Error en los valores: {str(e)}")
    
    def eliminar_item(self, row):
        """Elimina un item de la tabla"""
        if row < len(self.items):
            self.items.pop(row)
            self.tabla_items.removeRow(row)
            self.actualizar_totales()
    
    def actualizar_totales(self):
        """Actualiza los totales mostrados"""
        subtotal = sum(item.subtotal for item in self.items)
        iva = subtotal * 0.19
        total = subtotal + iva
        
        self.subtotal_label.setText(f"Subtotal: ${subtotal:,.0f}")
        self.iva_label.setText(f"IVA (19%): ${iva:,.0f}")
        self.total_label.setText(f"TOTAL: ${total:,.0f}")
    
    def guardar_boleta(self):
        """Guarda la boleta en la base de datos"""
        # Validar campos
        rut = self.rut_input.text().strip()
        nombre = self.nombre_input.text().strip()
        
        if not rut or not nombre:
            QMessageBox.warning(self, "Advertencia", 
                              "Complete RUT y Nombre del cliente")
            return
        
        if not self.items:
            QMessageBox.warning(self, "Advertencia", 
                              "Agregue al menos un producto/servicio")
            return
        
        try:
            # Buscar o crear cliente
            cliente = self.db_manager.buscar_cliente_por_rut(rut)
            if not cliente:
                cliente = Cliente(
                    rut=rut,
                    nombre=nombre,
                    email=self.email_input.text().strip(),
                    telefono=self.telefono_input.text().strip(),
                    direccion=self.direccion_input.text().strip()
                )
                cliente.id = self.db_manager.guardar_cliente(cliente)
            
            # Crear boleta
            boleta = Boleta(
                numero=self.numero_input.text(),
                fecha=datetime.now(),
                cliente_id=cliente.id,
                cliente_nombre=nombre,
                cliente_rut=rut,
                items=self.items.copy(),
                observaciones=self.observaciones_input.toPlainText().strip()
            )
            
            # Guardar boleta
            self.db_manager.guardar_boleta(boleta)
            
            QMessageBox.information(self, "Éxito", 
                                  f"Boleta N° {boleta.numero} guardada correctamente")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar boleta: {str(e)}")
