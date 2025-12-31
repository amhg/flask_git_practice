from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Sequence
from sqlalchemy.orm import relationship
from app.model.config import Base

class Login(Base):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    user_type = Column(Integer)

    admins = relationship('Admin', back_populates="login", uselist=False)
    customer = relationship('Customer', back_populates="login", uselist=False)

    def __init__(self, username, password, user_type, id=None):
        self.id = id
        self.username = username
        self.password = password
        self.user_type = user_type 

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "user_type": self.user_type
        }

    def __repr__(self):
        return f"<Login {self.id} {self.username}>"
    
class Customer(Base):
   __tablename__ = 'customer'
   id = Column(Integer, ForeignKey('login.id'), primary_key = True)
   firstname = Column(String(45))
   lastname = Column(String(45))  
   middlename = Column(String(45))
   email = Column(String(45))
   mobile = Column(String(20))
   address = Column(String(100))
   status = Column(String(45))
      
   login = relationship('Login', back_populates="customer")
   
   def __init__(self, id, firstname, lastname, middlename, email, mobile, address, status):
      self.id = id
      self.firstname = firstname
      self.lastname = lastname
      self.middlename = middlename
      self.email = email
      self.mobile = mobile
      self.address = address
      self.status = status
      
   def __repr__(self):
        return f"<Customer {self.id} {self.firstname} {self.middlename} {self.lastname}>"

class Admin(Base):
   __tablename__ = 'admin'
   id = Column(Integer, ForeignKey('login.id'), primary_key = True)
   firstname = Column(String(45))
   lastname = Column(String(45))  
   middlename = Column(String(45))
   email = Column(String(45))
   mobile = Column(String(45))
   
   login = relationship('Login', back_populates="admins")
   
   def __init__(self, id, firstname, lastname, middlename, email, mobile):
      self.id = id
      self.firstname = firstname
      self.lastname = lastname
      self.middlename = middlename
      self.email = email
      self.mobile = mobile
      
   def __repr__(self):
        return f"<Admin {self.id} {self.firstname} {self.middlename} {self.lastname}>"





""""""""""
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login_id = Column(Integer, ForeignKey('login.id'), unique=True, nullable=False)
    fname = Column(String(45), nullable=False)
    lname = Column(String(45), nullable=False)
    age = Column(Integer, nullable=False)
    date_registered = Column(Date, nullable=False)

    login = relationship('Login', back_populates="user")

    def __init__(self, login_id, fname, lname, age, date_registered, id=None):
        self.id = id
        self.login_id = login_id
        self.fname = fname
        self.lname = lname
        self.age = age
        self.date_registered = date_registered

    def to_json(self):
        return {
            "id": self.id,
            "login_id": self.login_id,
            "fname": self.fname,
            "lname": self.lname,
            "age": self.age,
            "date_registered": str(self.date_registered)
        }

    def __repr__(self):
        return f"<User {self.id} {self.fname} {self.lname}>"
"""""""""

