from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Account:
    db = "sighting_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO accounts (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM accounts;"
        results = connectToMySQL(cls.db).query_db(query)
        accounts = []
        for row in results:
            accounts.append( cls(row))
        return accounts

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM accounts WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM accounts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(account):
        is_valid = True
        query = "SELECT * FROM accounts WHERE email = %(email)s;"
        results = connectToMySQL(Account.db).query_db(query,account)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(account['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(account['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(account['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(account['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if account['password'] != account['confirm']:
            flash("Passwords don't match","register")
        return is_valid