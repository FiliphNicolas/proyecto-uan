from datetime import datetime
from factory import db

class Puesto(db.Model):
    __tablename__ = 'puestos'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    estado = db.Column(db.String(10), nullable=False, default='libre')
    
    def __repr__(self):
        return f'<Puesto {self.numero}>'

class Carro(db.Model):
    __tablename__ = 'carros'
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), nullable=False)
    hora_entrada = db.Column(db.DateTime, nullable=False)
    puesto_id = db.Column(db.Integer, db.ForeignKey('puestos.id'))
    estado = db.Column(db.String(10), nullable=False, default='activo')
    
    puesto = db.relationship('Puesto', 
                            backref=db.backref('carro_actual', uselist=False),
                            foreign_keys=[puesto_id],
                            lazy=True)
    
    def __repr__(self):
        return f'<Carro {self.placa}>'

class RegistroMovimiento(db.Model):
    __tablename__ = 'registro_movimientos'
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), nullable=False)
    hora_entrada = db.Column(db.DateTime, nullable=False)
    hora_salida = db.Column(db.DateTime)
    valor_pagado = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Registro {self.placa}>'

class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    id = db.Column(db.Integer, primary_key=True)
    tarifa_actual = db.Column(db.Float, nullable=False, default=2000)
    hora_simulada = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
    def __repr__(self):
        return f'<Configuracion {self.tarifa_actual}>'
