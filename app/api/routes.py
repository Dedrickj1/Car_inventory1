from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Cars, car_schema, cars_schema
api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

# @api.route('/data')
# def viewdata():
#     data = get_contact()
#     response = jsonify(data)
#     print(response)
#     return render_template('index.html', data = data)

@api.route('/cars', methods = ['POST'])
@token_required
def create_cars(current_user_token):
    model = request.json['model']
    make = request.json['make']
    year = request.json['year']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    cars = Cars(year, make, model, user_token = user_token )

    db.session.add(cars)
    db.session.commit()

    response = car_schema.dump(cars)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_car(current_user_token):
    print(current_user_token)
    a_user = current_user_token.token
    car = Cars.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(car)
    print(a_user)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    a_user = current_user_token.token
    if a_user == current_user_token.token:
        car = Cars.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token):
    car = Cars.query.get(id) 
    car.year = request.json['year']
    car.make = request.json['make']
    car.model = request.json['model']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_single_car(current_user_token, id):
    car = Cars.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)