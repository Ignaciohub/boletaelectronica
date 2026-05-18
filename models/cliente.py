"""Modelo de Cliente"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    """Representa un cliente del negocio de informática"""
    id: Optional[int] = None
    rut: str = ""
    nombre: str = ""
    email: str = ""
    telefono: str = ""
    direccion: str = ""
    
    def __str__(self):
        return f"{self.nombre} ({self.rut})"
    
    def to_dict(self):
        """Convierte el cliente a diccionario"""
        return {
            'id': self.id,
            'rut': self.rut,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'direccion': self.direccion
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un cliente desde un diccionario"""
        return cls(**data)
