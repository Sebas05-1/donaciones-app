# models.py
from app import db
from datetime import datetime

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    usuarios = db.relationship('Usuario', backref='role', lazy=True)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(30))
    cedula = db.Column(db.String(50))
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

class Donante(db.Model):
    __tablename__ = 'donantes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(150))
    telefono = db.Column(db.String(50))
    direccion = db.Column(db.String(255))
    cedula = db.Column(db.String(80))
    estado = db.Column(db.Boolean, default=True, nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    donaciones = db.relationship('Donacion', backref='donante', lazy=True)

class TipoDonacion(db.Model):
    __tablename__ = 'tipo_donacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))
    donaciones = db.relationship('Donacion', backref='tipo', lazy=True)
    asignaciones = db.relationship('Asignacion', backref='tipo_asig', lazy=True)

class Donacion(db.Model):
    __tablename__ = 'donaciones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_donacion.id'), nullable=False)
    donante_id = db.Column(db.Integer, db.ForeignKey('donantes.id'), nullable=True)
    monto = db.Column(db.Numeric(15,2), nullable=True)
    cantidad = db.Column(db.Integer, nullable=True)
    descripcion = db.Column(db.Text)
    estado = db.Column(db.Boolean, default=True, nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    asignaciones = db.relationship('Asignacion', backref='donacion', lazy=True)

class Beneficiario(db.Model):
    __tablename__ = 'beneficiarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    nit = db.Column(db.String(80))
    telefono = db.Column(db.String(50))
    correo = db.Column(db.String(150))
    direccion = db.Column(db.String(255))
    observaciones = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    asignaciones = db.relationship('Asignacion', backref='beneficiario', lazy=True)

class Asignacion(db.Model):
    __tablename__ = 'asignaciones'
    id = db.Column(db.Integer, primary_key=True)
    donacion_id = db.Column(db.Integer, db.ForeignKey('donaciones.id'), nullable=False)
    beneficiario_id = db.Column(db.Integer, db.ForeignKey('beneficiarios.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_donacion.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=True)    # para material
    monto = db.Column(db.Numeric(15,2), nullable=True) # para economico
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)
