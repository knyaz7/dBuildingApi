from flask import jsonify, request
from Models.Message import Message, db
from datetime import datetime

# def get_messages():
#     themes = Theme.query.all()
#     output = {
#         'status': True if len(themes) > 0 else False,
#         'message': "OK" if len(themes) > 0 else "Empty table",
#         'data': []
#     }
#     for theme in themes:
#         user_data = {'id': theme.id, 'user_id': theme.user_id, 'theme_name': theme.theme_name, 'rating': theme.rating}
#         output['data'].append(user_data)
#     return jsonify(output)

# def get_theme(item_id):
#     theme = Theme.query.get(item_id)
#     if theme:
#         user_data = {'id': theme.id, 'user_id': theme.user_id, 'theme_name': theme.theme_name, 'rating': theme.rating}
#         return jsonify({'status': True, 'message': 'OK', 'data': user_data})
#     else:
#         return jsonify({'status': False, 'message': 'Theme not found'}), 404
    
def add_message():
    theme_id = request.form.get('theme_id')
    message = request.form.get('message')
    time_str  = request.form.get('time')
    type = request.form.get('type')
    code = request.form.get('code')
    sender = 0

    if not theme_id or not message or not time or not type or not code:
        return jsonify({'status': False, 'error': 'Missing required fields'}), 400
    
    #Обработка аудио

    # Преобразование строки времени в объект datetime
    try:
        time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'status': False, 'error': 'Invalid time format. Use format: YYYY-MM-DD HH:MM:SS'}), 400

    new_message = Message(theme_id=theme_id, message=message, time=time, type=type, sender = sender)
    db.session.add(new_message)
    db.session.commit()

    inserted_message_id = new_message.id

    return jsonify({'status': True, 'message': 'Message added successfully', 'message_id': inserted_message_id}), 201


# def update_theme(item_id):
#     theme = Theme.query.get(item_id)
#     if not theme:
#         return jsonify({'status': False, 'message': 'Theme not found'}), 404

#     user_id = request.form.get('user_id')
#     theme_name = request.form.get('theme_name')
#     rating = request.form.get('rating')

#     if user_id:
#         theme.user_id = user_id
#     if theme_name:
#         theme.theme_name = theme_name
#     if rating:
#         theme.rating = rating

#     db.session.commit()
#     return jsonify({'status': True, 'message': 'Theme updated successfully'})
