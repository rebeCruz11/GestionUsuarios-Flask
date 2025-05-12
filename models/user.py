from extensions import db
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    carnet = db.Column(db.String(80), nullable=False, unique=True)
    nombre = db.Column(db.String(80), nullable=False, unique=False)
    apellido = db.Column(db.String(80), nullable=False, unique=False)
    correo = db.Column(db.String(200), unique=True, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    tipo_usuario = db.Column(db.String(80), nullable=False, unique=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    estado = db.Column(db.Boolean, default=True)

    @property
    def data(self):
        return {
            'id': self.id,
            'carnet': self.carnet,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'contrasena': self.contrasena,
            'fecha_nacimiento': str(self.fecha_nacimiento),
            'tipo_usuario': self.tipo_usuario,
            'estado': self.estado
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def obtener_usuarios(cls):
        r = cls.query.filter_by(tipo_usuario='alumno').all()
        # r = cls.query.all()
        result = []

        for i in r:
            result.append(i.data)

        return result
    
    
    @classmethod
    def obtener_id(cls, id):
        return cls.query.filter(cls.id == id).first()

    def verificar_contrasena(self, contrasena_enviada):
        return check_password_hash(self.contrasena, contrasena_enviada)

    
    @classmethod
    def obtener_id(cls, id):
        return cls.query.filter(cls.id == id).first()
    

    
