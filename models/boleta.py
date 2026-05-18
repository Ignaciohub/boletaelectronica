"""Modelo de Boleta"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class ItemBoleta:
    """Representa un item/producto en una boleta"""
    descripcion: str
    cantidad: int
    precio_unitario: float
    
    @property
    def subtotal(self) -> float:
        """Calcula el subtotal del item"""
        return self.cantidad * self.precio_unitario
    
    def to_dict(self):
        """Convierte el item a diccionario"""
        return {
            'descripcion': self.descripcion,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal
        }


@dataclass
class Boleta:
    """Representa una boleta electrónica"""
    id: Optional[int] = None
    numero: str = ""
    fecha: datetime = field(default_factory=datetime.now)
    cliente_id: Optional[int] = None
    cliente_nombre: str = ""
    cliente_rut: str = ""
    items: List[ItemBoleta] = field(default_factory=list)
    observaciones: str = ""
    
    @property
    def subtotal(self) -> float:
        """Calcula el subtotal de todos los items"""
        return sum(item.subtotal for item in self.items)
    
    @property
    def iva(self) -> float:
        """Calcula el IVA (19%)"""
        return self.subtotal * 0.19
    
    @property
    def total(self) -> float:
        """Calcula el total de la boleta"""
        return self.subtotal + self.iva
    
    def agregar_item(self, descripcion: str, cantidad: int, precio_unitario: float):
        """Agrega un item a la boleta"""
        item = ItemBoleta(descripcion, cantidad, precio_unitario)
        self.items.append(item)
    
    def to_dict(self):
        """Convierte la boleta a diccionario"""
        return {
            'id': self.id,
            'numero': self.numero,
            'fecha': self.fecha.isoformat(),
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente_nombre,
            'cliente_rut': self.cliente_rut,
            'items': [item.to_dict() for item in self.items],
            'observaciones': self.observaciones,
            'subtotal': self.subtotal,
            'iva': self.iva,
            'total': self.total
        }
