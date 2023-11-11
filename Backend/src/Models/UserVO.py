import utils.setup 
from werkzeug.security import check_password_hash, generate_password_hash
from utils.setup import db
from datetime import datetime
from flask_login import UserMixin


class UserVO(db.Model, UserMixin):
    _tablename_ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    idDocument = db.Column(db.Integer, nullable=False)
    documentType = db.Column(db.String(80), nullable=False)

    #Relacion uno a uno con ClientVO
    #client = db.relationship('ClientVO', backref='user', lazy=True, uselist=False)
    #Relacion uno a uno con EmployeeVO
    #employees = db.relationship('EmployeeVO', backref='user', lazy=True)

    def _init_(self, name, email, password, idDocument, documentType):
        self.name = name
        self.documentType = documentType
        self.idDocument = idDocument
        self.email = email
        self.password = password

    @classmethod
    def checkPassword(self, hashedPassword, password):
        return check_password_hash(hashedPassword, password)
    
    @classmethod
    def convertPassword(self, password):
        return generate_password_hash(password)
    
    def hashPassword(self):
        passw = self.convertPassword(self.password)
        self.password = passw  

    def to_JSON(self):
        return {
            'id':self.id,
            'name':self.name, 
            'documentType':self.documentType,
            'idDocument': self.idDocument,
            'email': self.email,
            'password': self.password
        }
    
    def from_JSON(self, data):
        for field in ['name', 'email', 'password', 'documentType', 'idDocument']:
            if field in data:
                setattr(self, field, data[field])
    
class ClientVO(db.Model):
    
    _tablename_ = 'Client'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    direction = db.Column(db.String(80), nullable=False)
    credit_card = db.Column(db.String(32))
    web_page = db.Column(db.String(200))
    pay_mode = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('UserVO.id'))
    # Relaciones
    #tickets = db.relationship('TicketVO', backref='client', lazy=True)
    #domains = db.relationship('DomainVO', backref='client', lazy=True)

    def _init_(self, direction, credit_card, web_page, pay_mode, is_active=True):
        self.direction = direction
        self.credit_card = credit_card
        self.web_page = web_page
        self.pay_mode = pay_mode
        self.is_active = is_active
        #self.user_id = user_id /up: user_id=None
        

    def to_JSON(self):
        return {
            'id': self.id,
            'direction': self.direction,
            'credit_card': self.credit_card,
            'web_page': self.web_page,
            'pay_mode': self.pay_mode,
            'is_active': self.is_active,
            #'user_id': self.user_id
        }

    def from_JSON(self, data):
        for field in ['direction', 'credit_card', 'web_page', 'pay_mode', 'is_active']:
            if field in data:
                setattr(self, field, data[field])

class EmployeeVO(db.Model):

    _tablename_ = 'Employee'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rol = db.Column(db.String(20), nullable=False)
    #hire_date = db.Column(db.DateTime, default=datetime.utcnow())
    is_hire = db.Column(db.Boolean, default=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('UserVO.id'))

    def _init_(self, rol, is_hire=True):
        #self.hire_date = hire_date if hire_date is not None else datetime.utcnow()
        self.rol = rol
        self.is_hire = is_hire

    def to_JSON(self):
        return {
            'id': self.id,
            'rol': self.rol,
            'is_hire': self.is_hire
        }

    def from_JSON(self, data):
        for field in ['rol','is_hire']:
            if field in data:
                setattr(self, field, data[field])