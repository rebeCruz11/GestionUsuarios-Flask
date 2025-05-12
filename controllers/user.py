from flask import request
from models.user import User
from extensions import db
from werkzeug.security import generate_password_hash

# Esta es la funcion que se encarga de agregar un usuario a la base de datos
# y de retornar los datos del usuario


def agregar_User_function():
    if request.method == 'POST':    
        carnet = request.form['carnet']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contrasena = generate_password_hash(request.form['contrasena'])
        fecha_nacimiento = request.form['fecha_nacimiento']
        tipo_usuario = request.form['tipo_usuario']
        estado = True
        user= User(
            carnet=carnet, 
            nombre=nombre, 
            apellido=apellido, 
            correo=correo,
            contrasena=contrasena,
            fecha_nacimiento=fecha_nacimiento,
            tipo_usuario=tipo_usuario,
            estado=estado
        )
        user.save()
        data = {
            'id': user.id,
            'carnet': carnet,
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            'contrasena': contrasena,
            'fecha_nacimiento': fecha_nacimiento,
            'tipo_usuario': tipo_usuario,
            'estado': estado
        }
        return data
    
def edit_usuario_function(data):
    if request.method == 'POST':
        data.carnet = request.form['carnet']
        data.nombre = request.form['nombre']
        data.apellido = request.form['apellido']
        data.correo = request.form['correo']    
        data.contrasena = generate_password_hash(request.form['contrasena'])
        data.fecha_nacimiento = request.form['fecha_nacimiento']
        data.tipo_usuario = request.form['tipo_usuario']
        data.estado = request.form['estado'] == '1'  # Esto convierte '1' a True y '0' a False
        # Guardar los cambios en la base de datos
        db.session.commit()
        return data

def delete_usuario_function(user):
    db.session.delete(user)
    db.session.commit()




        



