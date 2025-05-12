from extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func

class Nota(db.Model):
    __tablename__ = 'notas'
    
    id_Nota = db.Column(db.Integer, primary_key=True)
    id_Usuario = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    nota1 = db.Column(db.Numeric(5, 2), nullable=False)
    nota2 = db.Column(db.Numeric(5, 2), nullable=False)
    nota3 = db.Column(db.Numeric(5, 2), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    usuario = db.relationship('User', backref=db.backref('notas', lazy=True))

    @hybrid_property
    def promedio(self):
        return round((float(self.nota1) + float(self.nota2) + float(self.nota3)) / 3, 2)
    
    @property
    def data(self):
        return {
            'id_Nota': self.id_Nota,
            'id_Usuario': self.id_Usuario,
            'materia': self.materia,
            'nota1': float(self.nota1),
            'nota2': float(self.nota2),
            'nota3': float(self.nota3),
            'promedio': self.promedio,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
