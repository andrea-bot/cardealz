from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.car import Car
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    data = {
        'id' : session['logged_user']
    }
    logged_user = User.get_one(data)

    # getting all the cars
    all_cars = Car.get_all()
    return render_template('dashboard.html', user = logged_user, cars = all_cars)

@app.route('/cars/add')
def add_car():
    return render_template('add_car.html')

@app.route('/cars/create',methods=['post'])
def create_car():

    if not Car.validate_Car(request.form):
        return redirect('/cars/add')  

    data= {
        'price': request.form['price'],
        'make': request.form['make'],
        'model': request.form['model'],
        'year': request.form['year'],
        'user_id': session['logged_user'],
        'description': request.form['description']
    }

    new_car_id = Car.save(data)
    return redirect('/dashboard')

@app.route('/cars/<int:id>/edit')
def edit_car(id):
    data ={
        'id':id
    }
    car =Car.get_one(data)
    return render_template('edit_car.html',car = car)

@app.route('/cars/<int:id>/update',methods=['post'])
def update_car(id):

    if not Car.validate_Car(request.form):
        return redirect(f'/cars/{id}/edit')  
    
    data= {
        'price': request.form['price'],
        'make': request.form['make'],
        'model': request.form['model'],
        'year': request.form['year'],
        'user_id': session['logged_user'],
        'description': request.form['description'],
        'id':id
        
    }

    car_id=Car.update(data)
    print(car_id)
    return redirect('/dashboard')

@app.route('/cars/<int:id>/delete')
def delete_car(id):
    data = {
        'id':id
    }
    Car.delete(data)
    return redirect('/dashboard')

@app.route('/cars/<int:id>/view')
def view_car(id):
    data ={
        'id':id
    }
    one_car = Car.get_one(data)
    
    return render_template('view.html', cars = one_car)