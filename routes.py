from flask import Blueprint, render_template,request, redirect, url_for
from controllers.user import agregar_User_function, edit_usuario_function, delete_usuario_function
import sys
from models.user import User

main = Blueprint('main', __name__) #Esta sera la ruta main

# Esta es la ruta principal de la aplicacion
# y se encarga de mostrar la lista de usuarios
@main.route('/', methods=['GET'])
def home():
    data= User.obtener_usuarios()
    return render_template('index.html', data=data)

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
