from utils.DatabaseSql import getConnection
from Models.UserVO import UserVO
from utils.setup import db


class UserDAO():

    # Obtener la lista de usuarios
    @classmethod
    def getUsers(self):
        try:
            connection = getConnection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM user_vo")
                usuarios = cursor.fetchall()

            users = []
            for row in usuarios:
                user = UserVO(
                    name=row[1],
                    password=row[2],
                    email=row[3],
                    idDocument=row[4],
                    documentType=row[5]
                )
                user.id = row[0]
                user_json = user.to_JSON()
                users.append(user_json)

            connection.close()
            return users
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getUserByID(self, id):
        try:
            user = UserVO.query.filter_by(id=id).first()
            if user is not None:
                #userJson = user.to_JSON()
                return user
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)

    @classmethod
    def getUserByEmail(self, email):
        try:
            user = UserVO.query.filter_by(email=email).first()
            if user is not None:
                userJson = user.to_JSON()
                return userJson
            else:
                print('error en la busqueda')
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)

    # Crear User sin el hash 
    @classmethod
    def create_User(self, data):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:
                affectedRows = cursor.rowcount

            nuevoUser = UserVO(**data)

            db.session.add(nuevoUser)
            db.session.commit()
            connection.close()
            return affectedRows
        except Exception as ex:
            print("error")
            return Exception(ex)

    #Clase que actualiza el usuario
    @classmethod
    def uptadeUser(self, id, data):
        try:
            user = UserVO.query.filter_by(id=id).first()
            if user is not None:
                user.from_JSON(data)
                if 'password' in data:
                    user.hashPassword()
                db.session.commit()
                user_json = user.to_JSON()
                return user_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)

    #Clase que elimina el usuario 
    @classmethod
    def deleteUser(self, id):
        try:
            user = UserVO.query.filter_by(id=id).first()
            db.session.delete(user)
            db.session.commit()
            return user
        except Exception as ex:
            print("error")
            return Exception(ex)
        

    #Clase que se encarga de la verificacion mediante el email 
    @classmethod  
    def login(self, email, password):
        try:
            user = UserVO.query.filter_by(email=email).first()
            if user is not None:
                isPasswordCorrect = UserVO.checkPassword(user.password, password)
                user.password = isPasswordCorrect
                return user
            else: 
                return None
        except Exception as ex:
            raise Exception(ex)

    #Crearte user con el hash 
    @classmethod
    def createUser(self, data):        
        try:
            connection = getConnection()
            nuevoUser = UserVO(**data)
            nuevoUser.hashPassword()
            with connection.cursor() as cursor:
                affectedRows = cursor.rowcount

            db.session.add(nuevoUser)
            db.session.commit()
            connection.close()
            return affectedRows
        except Exception as ex:
            print("error")
            return Exception(ex)

    #Esta solo sirve para utilizar como guia en el hasheo del password 
    @classmethod
    def createUserHP(self, data):
        nuevoUser = UserVO(**data)
        password = nuevoUser.password
        #print('bandera1')
        print(password)
        nuevoUser.hashPassword()
        print(nuevoUser.password)
        pss=nuevoUser.password
        #print(nuevoUser.checkPassword(pss, nuevoUser.password))
        #isValid = nuevoUser.checkPassword(pss, password)
        #print('Encontraste tu solucion? ')
        #print("La contraseña es válida:", isValid)
        #print("Ahora verificaremos que hace cuando no es la contraseña: ")
        #otraPss='123.abc'
        #isValid = nuevoUser.checkPassword(pss, otraPss)
        #print("La contraseña es válida:", isValid)

        return nuevoUser