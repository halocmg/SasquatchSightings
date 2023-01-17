from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Sighting:
    db = "sighting_schema"

    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.time = data['time']
        self.description = data['description']
        self.amount = data['amount']
        self.account_id = data['account_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO sightings (location,time,description,amount,account_id) VALUES(%(location)s,%(time)s,%(description)s,%(amount)s,%(account_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM sightings WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def replace(cls, data):
        query = "UPDATE sightings SET location=%(location)s,time=%(time)s,description=%(description)s,amount=%(amount)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(cls.db).query_db(query)
        sightings = []
        for row in results:
            sightings.append(cls(row))
        return sightings

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_register(sighting):
        if len(sighting['location']) < 1:
            is_valid = True
            flash("Location requires input!", "saw")
            is_valid = False
        if len(sighting['time']) < 1:
            flash("Date requires input!", "saw")
            is_valid = False
        if len(sighting['description']) < 1:
            flash("Description requires input!", "saw")
            is_valid = False
        if len(sighting['amount']) < 1:
            flash("Amount requires input!", "saw")
            is_valid = False
        if len(sighting) > 0:
            try:
                j = int(sighting['amount'])
            except:
                if sighting['amount'] == "":
                    j = 0
            if j < 1:
                flash(
                    "It's not a sasquatch sighting if you saw none or negative!", "saw")
                is_valid = False
        return is_valid
