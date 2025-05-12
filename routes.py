from flask import Blueprint, render_template,request, redirect, url_for, session
from controllers.user import agregar_User_function, edit_usuario_function, delete_usuario_function
from controllers.nota import add_nota_function
import sys
from models.user import User
from models.nota import Nota
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__) #Esta sera la ruta main

# Esta es la ruta principal de la aplicacion
# y se encarga de mostrar la lista de usuarios
@main.route('/', methods=['GET'])
def home():
    if 'usuario_id' not in session:
            return redirect(url_for('main.login'))  # Redirigir al login si no hay sesión
        
    data = User.obtener_usuarios()
    return render_template('index.html', data=data)


@main.route('/perfil')
def perfil():
    # Aquí podrías recuperar datos del usuario actual si estás usando sesiones
    # usuario = session.get('usuario')
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    user = User.obtener_id(session['usuario_id'])
    return render_template('perfil.html', user=user) # crea perfil.html si no existe


@main.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('main.login')) # crea perfil.html si no existe


#Este es para el login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        # Buscar al usuario por correo
        user = User.query.filter_by(correo=correo).first()
        
        if user and user.verificar_contrasena(contrasena):
            # Guardar el ID del usuario en la sesión
            session['usuario_id'] = user.id
            if user.tipo_usuario == 'docente':
                # Redirigir a index si es docente
                return redirect(url_for('main.home'))
            else:
                # Redirigir al perfil o cualquier otra página para alumnos
                return redirect(url_for('main.perfil'))
        else:
            error = 'Correo o contraseña incorrectos'
            return render_template('login.html', error=error)

    return render_template('login.html')



# Esta es la ruta que se encarga de mostrar el formulario para agregar un usuario
# y de agregar el usuario a la base de datos
@main.route('/agregarUser', methods=['GET', 'POST'])

def agregar_User():
    data = agregar_User_function()
    print(data, file=sys.stderr)
    return render_template('agregarUser.html', data=data)

# Esta es la ruta que se encarga de mostrar el formulario para editar un usuario
# y de editar el usuario en la base de datos
@main.route('/editusuario/<int:id>', methods=['GET', 'POST'])
def edit_usuario(id):
    user = User.obtener_id(id)

    if request.method == 'POST':
        data = edit_usuario_function(user)
        return redirect(url_for('main.home'))  # Redirige después de editar

    # Si es GET, muestra el formulario con los datos actuales
    return render_template('editusuario.html', user=user)

# Esta es la ruta que se encarga de eliminar un usuario
@main.route('/deleteusuario/<int:id>', methods=['POST'])
def delete_usuario(id):
    user = User.obtener_id(id)
    print(user, file=sys.stderr)
    delete_usuario_function(user)
    return redirect(url_for('main.home'))


# Este sera para las notas de los usuarios alumnos

@main.route('/detalles/<int:id>', methods=['GET'])
def details_usuario(id):
    user = User.obtener_id(id)

    return render_template('detalles.html', user=user)

@main.route('/agregarnota/<int:id>', methods=['GET', 'POST'])
def agregar_nota(id):
    user = User.obtener_id(id)

    if request.method == 'POST':
        data = add_nota_function(user)
        return redirect(url_for('main.home'))  # Redirige después de editar

    # Si es GET, muestra el formulario con los datos actuales
    return render_template('agregarnota.html', user=user)


