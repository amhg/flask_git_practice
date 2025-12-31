from typing import List, Any, Dict
from app.model.db import Login
from sqlalchemy.orm import Session
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

users = {
    'johndoe': {
        'username': 'johndoe',
        'password': '123',
        'user_type': 1
    }
}

class LoginRepository:
    def __init__(self, sess:Session):
        self.sess = sess
        current_app.logger.info('LoginRepository instance created')

    def insert(self, login:Login) -> bool:
        try:
            self.sess.add(login)
            current_app.logger.info('LoginRepository inserted record')
            return True
        except Exception as e:
            current_app.logger.error(f'LoginRepository insert error: {e}') 
        return False
    
    def select_one_username_unsafe(self, username:str) -> Any: # not sure if is correct
        sql = self.sess.query(Login).where(Login.username == username)
        #sql = text("SELECT * FROM login WHERE username = :username")
        result = self.sess.execute(sql)
        return result.fetchone()

    
    def select_one_username(self, username:str) -> Any:
        user =  self.sess.query(Login).filter(Login.username == username).one_or_none()
        return user
    
    def get_user_by_username(self,username):
        return users.get(username)
    

    def update(self, username:str, details:Dict[str, Any]) -> bool:
        try:
            self.sess.query(Login).filter( Login.username == username).update(details)     
            self.sess.commit() 
            current_app.logger.info('LoginRepository updated record')
            return True
        except Exception as e:
            current_app.logger.error(f'LoginRepository insert error: {e}') 
        return False 
    
    def select_all(self) -> List[Any]:
        users = self.sess.query(Login).all()
        return users 


