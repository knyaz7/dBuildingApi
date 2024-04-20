from flask import jsonify, request
from Models.Theme import Theme, db

def get_themes():
    themes = Theme.query.all()
    output = {
        'status': True if len(themes) > 0 else False,
        'message': "OK" if len(themes) > 0 else "Empty table",
        'data': []
    }
    for theme in themes:
        user_data = {'id': theme.id, 'user_id': theme.user_id, 'theme_name': theme.theme_name, 'rating': theme.rating}
        output['data'].append(user_data)
    return jsonify(output)

def get_theme(item_id):
    theme = Theme.query.get(item_id)
    if theme:
        user_data = {'id': theme.id, 'user_id': theme.user_id, 'theme_name': theme.theme_name, 'rating': theme.rating}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'Theme not found'}), 404
    
def add_theme():
    user_id = request.form.get('user_id')
    theme_name = request.form.get('theme_name')

    if not user_id or not theme_name:
        return jsonify({'status': False, 'error': 'Missing required fields'}), 400

    rating = request.form.get('rating', -1)  # По умолчанию -1, если значение не передано

    new_theme = Theme(user_id=user_id, theme_name=theme_name, rating=rating)
    db.session.add(new_theme)
    db.session.commit()

    inserted_theme_id = new_theme.id

    return jsonify({'status': True, 'message': 'Theme added successfully', 'theme_id': inserted_theme_id}), 201


def update_theme(item_id):
    theme = Theme.query.get(item_id)
    if not theme:
        return jsonify({'status': False, 'message': 'Theme not found'}), 404

    user_id = request.form.get('user_id')
    theme_name = request.form.get('theme_name')
    rating = request.form.get('rating')

    if user_id:
        theme.user_id = user_id
    if theme_name:
        theme.theme_name = theme_name
    if rating:
        theme.rating = rating

    db.session.commit()
    return jsonify({'status': True, 'message': 'Theme updated successfully'})
