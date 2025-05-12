from flask import Blueprint, render_template,request, redirect, url_for, session
from controllers.user import agregar_User_function, edit_usuario_function, delete_usuario_function
from controllers.nota import add_nota_function, edit_nota_function, delete_nota_function
import sys
from models.user import User
from models.nota import Nota
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__) #Esta sera la ruta main

# Esta es la ruta principal de la aplicacion
# y se encarga de mostrar la lista de usuarios
@main.route('/', methods=['GET'])
def home():
    # Redirigir al login si no hay sesión activa
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))
    
    # Validar que el usuario sea docente o admin
    user = User.obtener_id(session['usuario_id'])
    if user.tipo_usuario not in ['docente', 'admin']:
        session.pop('usuario_id', None)  # Cerrar sesión si no tiene permisos
        return redirect(url_for('main.login'))

    # Mostrar la página principal si tiene permisos
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
            # Validar que el usuario sea docente o admin
            if user.tipo_usuario not in ['docente', 'admin']:
                error = 'Acceso denegado. Solo docentes o administradores pueden ingresar.'
                return render_template('login.html', error=error)
            
            # Guardar el ID del usuario en la sesión
            session['usuario_id'] = user.id
            return redirect(url_for('main.home'))  # Redirigir a la página principal
        else:
            error = 'Correo o contraseña incorrectos'
            return render_template('login.html', error=error)

    return render_template('login.html')



# Esta es la ruta que se encarga de mostrar el formulario para agregar un usuario
# y de agregar el usuario a la base de datos
@main.route('/agregarUser', methods=['GET', 'POST'])
def agregar_User():
    if request.method == 'POST':
        agregar_User_function()
        return redirect(url_for('main.home'))  # Redirige a la página principal después de agregar

    return render_template('agregarUser.html')

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
        return redirect(url_for('main.details_usuario', id= user.id))   # Redirige después de editar

    # Si es GET, muestra el formulario con los datos actuales
    return render_template('agregarnota.html', user=user)

@main.route('/editnota/<int:id>', methods=['GET', 'POST'])
def edit_nota(id):
    # Obtener la nota por su ID
    nota = Nota.query.get_or_404(id)

    if request.method == 'POST':
        # Llamar a la función para editar la nota
        edit_nota_function(nota)
        return redirect(url_for('main.details_usuario', id=nota.id_Usuario))  # Redirigir a los detalles del usuario

    # Si es GET, mostrar el formulario con los datos actuales
    return render_template('editnota.html', nota=nota)


@main.route('/deletenota/<int:id>', methods=['POST'])
def delete_nota(id):
    # Obtener la nota por su ID
    nota = Nota.query.get_or_404(id)
    
    # Eliminar la nota de la base de datos
    delete_nota_function(nota)
    
    # Redirigir a los detalles del usuario asociado
    return redirect(url_for('main.details_usuario', id=nota.id_Usuario))


