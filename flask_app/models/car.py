from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Car:
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.seller = ''
        
    @staticmethod
    def validate_Car(form_data):
        is_valid = True
        print(form_data)
        if form_data['year']=="":
            flash("year must be given!","year")
            is_valid=False
        if form_data['price']=="":
            flash("price must be given!","price")
            is_valid=False
        return is_valid


    @classmethod
    def save(cls,data):
        query = "INSERT INTO cars (year, model,user_id,make,price,description) VALUES ( %(year)s, %(model)s,%(user_id)s,%(make)s,%(price)s,%(description)s);"

        new_car_id = connectToMySQL('cardealz_db').query_db(query, data)

        return new_car_id


    @classmethod
    def get_one (cls,data):
        query="SELECT * FROM cars where id =%(id)s;"
        result = connectToMySQL('cardealz_db').query_db(query,data)
        car = cls(result[0])

        return car
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars;"
        results = connectToMySQL('cardealz_db').query_db(query)
        all_cars = []
        for row in results:
            # instantiating an instance of a car object (Python object)
            car = cls(row)

            # creating a data dictionary to set key 'id' equal to the user_id(the seller's id) from each row in our database
            data = {
                'id' : row['user_id']
            }

            # calling on the get_one function in our User class in onrder for our car object's seller attribute to hold the seller's information(first_name, last_name, email)
            car.seller = User.get_one(data)

            # adding this instance of a car object to our all_cars list
            all_cars.append(car)
        
        return all_cars


    @classmethod
    def update(cls,data):
        query="UPDATE cars SET model=%(model)s,year=%(year)s,user_id=%(user_id)s,make=%(make)s,price=%(price)s,description=%(description)s WHERE id=%(id)s;"
        result=connectToMySQL('cardealz_db').query_db(query,data)
        return data['id']
        

    @classmethod
    def delete(cls,data):
        query ="DELETE FROM cars WHERE id = %(id)s;"
        connectToMySQL('cardealz_db').query_db(query,data)