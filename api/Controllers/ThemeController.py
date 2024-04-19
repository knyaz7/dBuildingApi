from flask import jsonify, request
from Models.Theme import Theme, db

def get_themes():
    themes = Theme.query.all()
    output = []
    for theme in themes:
        user_data = {'id': theme.id, 'user_id': theme.user_id, 'theme_name': theme.theme_name, 'rating': theme.rating}
        output.append(user_data)
    return jsonify(output)

def get_theme(item_id):
    theme = Theme.query.get(item_id)
    if theme:
        user_data = {'id': theme.id, 'user_id': theme.user_id, 'theme_name': theme.theme_name, 'rating': theme.rating}
        return jsonify(user_data)
    else:
        return jsonify({'message': 'Theme not found'}), 404
    
def add_theme():
    user_id = request.form.get('user_id')
    theme_name = request.form.get('theme_name')
    rating = request.form.get('rating')

    if not user_id or not theme_name or not rating:
        return jsonify({'error': 'Missing required fields'}), 400

    new_theme = Theme(user_id=user_id, theme_name=theme_name, rating=rating)
    db.session.add(new_theme)
    db.session.commit()
    return jsonify({'message': 'Theme added successfully'}), 201

def update_theme(item_id):
    theme = Theme.query.get(item_id)
    if not theme:
        return jsonify({'message': 'Theme not found'}), 404

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
    return jsonify({'message': 'Theme updated successfully'})
