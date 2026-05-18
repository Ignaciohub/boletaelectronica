"""Ventana principal del sistema de boleta electrónica"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QLineEdit, QMessageBox, QHeaderView, QFileDialog, QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from database.db_manager import DatabaseManager
from models.boleta import Boleta
from models.cliente import Cliente
from utils.pdf_generator import PDFGenerator
from ui.nueva_boleta_dialog import NuevaBoletaDialog


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.pdf_generator = PDFGenerator()
        self.init_ui()
        self.cargar_boletas()
        self.cargar_clientes()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Sistema de Boleta Electrónica - Negocio de Informática")
        self.setGeometry(100, 100, 1200, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Título
        title_label = QLabel("Sistema de Boleta Electrónica")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Tabs para boletas y clientes
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Tab de boletas
        boletas_widget = QWidget()
        boletas_layout = QVBoxLayout(boletas_widget)
        
        # Botones de acción para boletas
        buttons_layout = QHBoxLayout()
        
        self.btn_nueva_boleta = QPushButton("Nueva Boleta")
        self.btn_nueva_boleta.clicked.connect(self.nueva_boleta)
        self.btn_nueva_boleta.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.btn_ver_pdf = QPushButton("Ver PDF")
        self.btn_ver_pdf.clicked.connect(self.ver_pdf_boleta)
        self.btn_ver_pdf.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        
        self.btn_actualizar = QPushButton("Actualizar Lista")
        self.btn_actualizar.clicked.connect(self.cargar_boletas)
        self.btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        
        buttons_layout.addWidget(self.btn_nueva_boleta)
        buttons_layout.addWidget(self.btn_ver_pdf)
        buttons_layout.addWidget(self.btn_actualizar)
        buttons_layout.addStretch()
        
        boletas_layout.addLayout(buttons_layout)
        
        # Buscador de boletas
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar por RUT cliente:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ej: 12345678-9")
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_boletas)
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.clicked.connect(self.cargar_boletas)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.btn_buscar)
        search_layout.addWidget(self.btn_limpiar)
        search_layout.addStretch()
        
        boletas_layout.addLayout(search_layout)
        
        # Tabla de boletas
        self.tabla_boletas = QTableWidget()
        self.tabla_boletas.setColumnCount(6)
        self.tabla_boletas.setHorizontalHeaderLabels([
            "N° Boleta", "Fecha", "Cliente", "RUT", "Total", "ID"
        ])
        self.tabla_boletas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_boletas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_boletas.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        boletas_layout.addWidget(self.tabla_boletas)
        
        self.tabs.addTab(boletas_widget, "Boletas")
        
        # Tab de clientes
        clientes_widget = QWidget()
        clientes_layout = QVBoxLayout(clientes_widget)
        
        # Botones para clientes
        clientes_buttons = QHBoxLayout()
        self.btn_actualizar_clientes = QPushButton("Actualizar Lista")
        self.btn_actualizar_clientes.clicked.connect(self.cargar_clientes)
        clientes_buttons.addWidget(self.btn_actualizar_clientes)
        clientes_buttons.addStretch()
        clientes_layout.addLayout(clientes_buttons)
        
        # Tabla de clientes
        self.tabla_clientes = QTableWidget()
        self.tabla_clientes.setColumnCount(5)
        self.tabla_clientes.setHorizontalHeaderLabels([
            "RUT", "Nombre", "Email", "Teléfono", "Dirección"
        ])
        self.tabla_clientes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_clientes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_clientes.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        clientes_layout.addWidget(self.tabla_clientes)
        
        self.tabs.addTab(clientes_widget, "Clientes")
        
        # Barra de estado
        self.statusBar().showMessage("Sistema listo")
    
    def cargar_boletas(self):
        """Carga las boletas desde la base de datos"""
        try:
            boletas = self.db_manager.obtener_boletas()
            self.mostrar_boletas(boletas)
            self.statusBar().showMessage(f"{len(boletas)} boletas cargadas")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar boletas: {str(e)}")
    
    def mostrar_boletas(self, boletas):
        """Muestra las boletas en la tabla"""
        self.tabla_boletas.setRowCount(len(boletas))
        
        for row, boleta in enumerate(boletas):
            self.tabla_boletas.setItem(row, 0, QTableWidgetItem(boleta.numero))
            self.tabla_boletas.setItem(row, 1, QTableWidgetItem(
                boleta.fecha.strftime("%d/%m/%Y %H:%M")
            ))
            self.tabla_boletas.setItem(row, 2, QTableWidgetItem(boleta.cliente_nombre))
            self.tabla_boletas.setItem(row, 3, QTableWidgetItem(boleta.cliente_rut))
            self.tabla_boletas.setItem(row, 4, QTableWidgetItem(f"${boleta.total:,.0f}"))
            self.tabla_boletas.setItem(row, 5, QTableWidgetItem(str(boleta.id)))
        
        # Ocultar columna de ID
        self.tabla_boletas.setColumnHidden(5, True)
    
    def cargar_clientes(self):
        """Carga los clientes desde la base de datos"""
        try:
            clientes = self.db_manager.obtener_clientes()
            self.mostrar_clientes(clientes)
            self.statusBar().showMessage(f"{len(clientes)} clientes cargados")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar clientes: {str(e)}")
    
    def mostrar_clientes(self, clientes):
        """Muestra los clientes en la tabla"""
        self.tabla_clientes.setRowCount(len(clientes))
        
        for row, cliente in enumerate(clientes):
            self.tabla_clientes.setItem(row, 0, QTableWidgetItem(cliente.rut))
            self.tabla_clientes.setItem(row, 1, QTableWidgetItem(cliente.nombre))
            self.tabla_clientes.setItem(row, 2, QTableWidgetItem(cliente.email))
            self.tabla_clientes.setItem(row, 3, QTableWidgetItem(cliente.telefono))
            self.tabla_clientes.setItem(row, 4, QTableWidgetItem(cliente.direccion))
    
    def nueva_boleta(self):
        """Abre el diálogo para crear una nueva boleta"""
        dialog = NuevaBoletaDialog(self.db_manager, self)
        if dialog.exec():
            self.cargar_boletas()
            self.cargar_clientes()
            self.statusBar().showMessage("Boleta creada exitosamente")
    
    def buscar_boletas(self):
        """Busca boletas por RUT de cliente"""
        rut = self.search_input.text().strip()
        if not rut:
            QMessageBox.warning(self, "Advertencia", "Ingrese un RUT para buscar")
            return
        
        try:
            boletas = self.db_manager.buscar_boletas_por_cliente(rut)
            self.mostrar_boletas(boletas)
            self.statusBar().showMessage(f"{len(boletas)} boletas encontradas para RUT {rut}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar boletas: {str(e)}")
    
    def ver_pdf_boleta(self):
        """Genera y abre el PDF de la boleta seleccionada"""
        selected_rows = self.tabla_boletas.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Advertencia", "Seleccione una boleta")
            return
        
        try:
            # Obtener el ID de la boleta seleccionada
            row = self.tabla_boletas.currentRow()
            boleta_id = int(self.tabla_boletas.item(row, 5).text())
            
            # Buscar la boleta en la lista
            boletas = self.db_manager.obtener_boletas()
            boleta = next((b for b in boletas if b.id == boleta_id), None)
            
            if not boleta:
                QMessageBox.warning(self, "Advertencia", "Boleta no encontrada")
                return
            
            # Generar nombre de archivo
            filename = f"boleta_{boleta.numero}.pdf"
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Boleta PDF",
                filename,
                "PDF Files (*.pdf)"
            )
            
            if filepath:
                self.pdf_generator.generar_boleta_pdf(boleta, filepath)
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"PDF generado correctamente:\n{filepath}"
                )
                self.statusBar().showMessage(f"PDF generado: {filepath}")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar PDF: {str(e)}")
