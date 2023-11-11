from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from Models.UserVO import UserVO
from Services.UserDAO import UserDAO
from utils.setup import db, loginManagerApp
from flask_login import login_user, logout_user, login_required, current_user

authMain = Blueprint('authBlueprint', __name__)

def status401(error):
    return redirect(url_for('authBlueprint.login'))

def status404(error): 
    return "<h1>404<br>Not found page :(</h1>", 404

@authMain.route('/home/')
def home():
    print("ya en el home, bienvenido")
    if isinstance(current_user, UserVO):
        print(current_user.is_authenticated)
    else:
        print("current_user is not a User object")
    return render_template('home.html')

@authMain.route('/ver/')
def verification():
    if current_user.is_authenticated:
        return f"Página de inicio. Usuario autenticado: {current_user.id}"
    else:
        return "Página de inicio. No hay usuario autenticado."

@loginManagerApp.user_loader
def loadUser(id):
    user = UserDAO.getUserByID(id)
    if isinstance(user, UserVO):
        print(user.name)
    else:
        print("No esta retornando un objeto")
    return user

@authMain.route('/create/', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        # Captura los datos del formulario
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        idDocument = request.form.get('idDocument')
        documentType = request.form.get('documentType')

        print("Nombre:", name)
        print("Correo electrónico:", email)
        print("Contraseña:", password)
        print("Número de identificación:", idDocument)
        print("Tipo de identificación:", documentType)

        # Crea un arreglo para almacenar los datos
        data = []

        # Agrega los datos del formulario al arreglo
        data = {
            'name': name,
            'password': password,
            'email': email,
            'idDocument': idDocument,
            'documentType': documentType
        }


        # Aquí puedes procesar los datos, por ejemplo, guardarlos en una base de datos
        # o realizar cualquier otra acción necesaria.
        print(data)
        affectedRows = UserDAO.createUser(data)
        print(affectedRows)
        if (affectedRows == 0):
            return jsonify({'message': 'Operación POST exitosa'}), 201
        else:
            return jsonify({'message': 'Error on insert'})
    elif request.method == 'GET':
        return render_template('auth/create.html')
    return render_template('auth/create.html')   
    

@authMain.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  
        password = request.form.get('password') 
        loggedUser = UserDAO.login(email, password)
        if loggedUser is not None:
            if loggedUser.password is True:
                login_user(loggedUser)
                print("Contraseña correcta, usuario autenticado")
                return redirect(url_for("authBlueprint.home"))
            else: 
                flash("Contraseña incorrecta, no se pudo autenticar")
                print("Contraseña incorrecta, no se pudo autenticar")
                
        else:
            flash("Usuario no encontrado...")
            print("El usuario no existe")
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@authMain.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authBlueprint.login'))

@authMain.route('/protected/')
@login_required
def protected():
    return "<h1>Esta en una vista protegida, unicamente para usuarios autenticados</h1>"