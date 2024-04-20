from flask import jsonify, request
from Models.User import User, db

def get_users():
    users = User.query.all()
    output = {
        'status': True if len(users) > 0 else False,
        'message': "OK" if len(users) > 0 else "Empty table",
        'data': []
    }
    for user in users:
        user_data = {'id': user.id, 'login' : user.login, 'first_name': user.first_name, 'last_name': user.last_name, 'password': user.password}
        output['data'].append(user_data)
    return jsonify(output)

def get_user(item_id):
    user = User.query.get(item_id)
    if user:
        user_data = {'id': user.id, 'login': user.login, 'first_name': user.first_name, 'last_name': user.last_name, 'password': user.password}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'User not found'}), 404

    
def add_user():
    login = request.form.get('login')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    if not login or not first_name or not last_name or not password:
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400

    existing_user = User.query.filter_by(login=login).first()
    if existing_user:
        return jsonify({'status': False, 'message': 'User with this login already exists'}), 409

    new_user = User(login=login, first_name=first_name, last_name=last_name, password=password)
    db.session.add(new_user)
    db.session.commit()

    # Получаем ID вставленной записи
    inserted_user_id = new_user.id

    return jsonify({'status': True, 'message': 'User added successfully', 'user_id': inserted_user_id}), 201

def update_user(item_id):
    user = User.query.get(item_id)
    if not user:
        return jsonify({'status': False, 'message': 'User not found'}), 404

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
    return jsonify({'status': True, 'message': 'User updated successfully'})
