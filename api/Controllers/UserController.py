from flask import jsonify, request
from Models.User import User, db

def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'id': user.id, 'login' : user.login, 'first_name': user.first_name, 'first_name': user.last_name, 'password': user.password}
        output.append(user_data)
    return jsonify(output)

def get_user(item_id):
    user = User.query.get(item_id)
    if user:
        user_data = {'id': user.id, 'login': user.login, 'first_name': user.first_name, 'first_name': user.last_name, 'password': user.password}
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'}), 404
    
def add_user():
    login = request.form.get('login')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    if not login or not first_name or not last_name or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    existing_user = User.query.filter_by(login=login).first()
    if existing_user:
        return jsonify({'error': 'User with this login already exists'}), 409

    new_user = User(login=login, first_name=first_name, last_name=last_name, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

def update_user(item_id):
    user = User.query.get(item_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    login = request.form.get('login')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    if login:
        user.login = login
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        user.password = password

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})
