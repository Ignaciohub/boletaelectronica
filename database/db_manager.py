"""Gestor de base de datos SQLite para el sistema de boletas"""
import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from models.boleta import Boleta, ItemBoleta
from models.cliente import Cliente


class DatabaseManager:
    """Gestiona la base de datos SQLite del sistema"""
    
    def __init__(self, db_path: str = "boletas.db"):
        """Inicializa el gestor de base de datos"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializa las tablas de la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rut TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                email TEXT,
                telefono TEXT,
                direccion TEXT
            )
        ''')
        
        # Tabla de boletas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS boletas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                fecha TEXT NOT NULL,
                cliente_id INTEGER,
                cliente_nombre TEXT NOT NULL,
                cliente_rut TEXT NOT NULL,
                items TEXT NOT NULL,
                observaciones TEXT,
                subtotal REAL NOT NULL,
                iva REAL NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Métodos para Clientes
    def guardar_cliente(self, cliente: Cliente) -> int:
        """Guarda o actualiza un cliente en la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if cliente.id:
            cursor.execute('''
                UPDATE clientes
                SET rut=?, nombre=?, email=?, telefono=?, direccion=?
                WHERE id=?
            ''', (cliente.rut, cliente.nombre, cliente.email, 
                  cliente.telefono, cliente.direccion, cliente.id))
        else:
            cursor.execute('''
                INSERT INTO clientes (rut, nombre, email, telefono, direccion)
                VALUES (?, ?, ?, ?, ?)
            ''', (cliente.rut, cliente.nombre, cliente.email, 
                  cliente.telefono, cliente.direccion))
            cliente.id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return cliente.id
    
    def obtener_clientes(self) -> List[Cliente]:
        """Obtiene todos los clientes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, rut, nombre, email, telefono, direccion FROM clientes')
        rows = cursor.fetchall()
        conn.close()
        
        clientes = []
        for row in rows:
            cliente = Cliente(
                id=row[0],
                rut=row[1],
                nombre=row[2],
                email=row[3],
                telefono=row[4],
                direccion=row[5]
            )
            clientes.append(cliente)
        
        return clientes
    
    def buscar_cliente_por_rut(self, rut: str) -> Optional[Cliente]:
        """Busca un cliente por RUT"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, rut, nombre, email, telefono, direccion 
            FROM clientes WHERE rut=?
        ''', (rut,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Cliente(
                id=row[0],
                rut=row[1],
                nombre=row[2],
                email=row[3],
                telefono=row[4],
                direccion=row[5]
            )
        return None
    
    # Métodos para Boletas
    def guardar_boleta(self, boleta: Boleta) -> int:
        """Guarda una boleta en la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        items_json = json.dumps([item.to_dict() for item in boleta.items])
        
        cursor.execute('''
            INSERT INTO boletas 
            (numero, fecha, cliente_id, cliente_nombre, cliente_rut, 
             items, observaciones, subtotal, iva, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (boleta.numero, boleta.fecha.isoformat(), boleta.cliente_id,
              boleta.cliente_nombre, boleta.cliente_rut, items_json,
              boleta.observaciones, boleta.subtotal, boleta.iva, boleta.total))
        
        boleta.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return boleta.id
    
    def obtener_boletas(self, limit: int = 100) -> List[Boleta]:
        """Obtiene las últimas boletas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, numero, fecha, cliente_id, cliente_nombre, cliente_rut,
                   items, observaciones
            FROM boletas
            ORDER BY fecha DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        boletas = []
        for row in rows:
            items_data = json.loads(row[6])
            items = [ItemBoleta(
                descripcion=item['descripcion'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario']
            ) for item in items_data]
            
            boleta = Boleta(
                id=row[0],
                numero=row[1],
                fecha=datetime.fromisoformat(row[2]),
                cliente_id=row[3],
                cliente_nombre=row[4],
                cliente_rut=row[5],
                items=items,
                observaciones=row[7]
            )
            boletas.append(boleta)
        
        return boletas
    
    def obtener_siguiente_numero_boleta(self) -> str:
        """Obtiene el siguiente número de boleta disponible"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT MAX(CAST(numero AS INTEGER)) FROM boletas')
        result = cursor.fetchone()
        conn.close()
        
        if result[0]:
            return str(result[0] + 1).zfill(6)
        return "000001"
    
    def buscar_boletas_por_cliente(self, cliente_rut: str) -> List[Boleta]:
        """Busca boletas de un cliente específico"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, numero, fecha, cliente_id, cliente_nombre, cliente_rut,
                   items, observaciones
            FROM boletas
            WHERE cliente_rut=?
            ORDER BY fecha DESC
        ''', (cliente_rut,))
        rows = cursor.fetchall()
        conn.close()
        
        boletas = []
        for row in rows:
            items_data = json.loads(row[6])
            items = [ItemBoleta(
                descripcion=item['descripcion'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario']
            ) for item in items_data]
            
            boleta = Boleta(
                id=row[0],
                numero=row[1],
                fecha=datetime.fromisoformat(row[2]),
                cliente_id=row[3],
                cliente_nombre=row[4],
                cliente_rut=row[5],
                items=items,
                observaciones=row[7]
            )
            boletas.append(boleta)
        
        return boletas
