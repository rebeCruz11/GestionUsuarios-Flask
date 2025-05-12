from flask import request
from models.nota import Nota
from extensions import db



def add_nota_function(data):
    if request.method == 'POST':
        id_Usuario = data.id
        materia = request.form['materia']
        nota1 = request.form['nota1']
        nota2 = request.form['nota2']
        nota3 = request.form['nota3']
        nota= Nota(
            id_Usuario=id_Usuario, 
            materia=materia, 
            nota1=nota1, 
            nota2=nota2,
            nota3=nota3
        )
        nota.save()
        data = {
            'id_Nota': nota.id_Nota,
            'id_Usuario': id_Usuario,
            'materia': materia,
            'nota1': float(nota1),
            'nota2': float(nota2),
            'nota3': float(nota3),
            'promedio': nota.promedio
        }
        return data
    
def edit_nota_function(data):
    if request.method == 'POST':
        data.materia = request.form['materia']
        data.nota1 = request.form['nota1']
        data.nota2 = request.form['nota2']
        data.nota3 = request.form['nota3']
        # Guardar los cambios en la base de datos
        db.session.commit()
        return data
    
def delete_nota_function(nota):
    db.session.delete(nota)
    db.session.commit()