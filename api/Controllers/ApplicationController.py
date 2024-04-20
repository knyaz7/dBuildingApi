from flask import jsonify, request
from Models.Application import Application, db

def get_applications():
    applications = Application.query.all()
    output = {
        'status': True if len(applications) > 0 else False,
        'message': "OK" if len(applications) > 0 else "Empty table",
        'data': []
    }
    for application in applications:
        user_data = {'id': application.id, 'user_id' : application.user_id, 'status': application.status}
        output['data'].append(user_data)
    return jsonify(output)

def get_application(item_id):
    application = Application.query.get(item_id)
    if application:
        user_data = {'id': application.id, 'user_id' : application.user_id, 'status': application.status}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'Application not found'}), 404

    
def add_application():
    user_id = request.form.get('user_id')
    status = False

    if not user_id:
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400

    new_application = Application(user_id=user_id, status=status)
    db.session.add(new_application)
    db.session.commit()

    # Получаем ID вставленной записи
    inserted_user_id = new_application.id

    return jsonify({'status': True, 'message': 'Application added successfully', 'application_id': inserted_user_id}), 201

def update_application(item_id):
    application = Application.query.get(item_id)
    if not application:
        return jsonify({'status': False, 'message': 'Application not found'}), 404

    status = request.form.get('status')

    if status:
        application.status = bool(status)

    db.session.commit()
    return jsonify({'status': True, 'message': 'Application updated successfully'})
