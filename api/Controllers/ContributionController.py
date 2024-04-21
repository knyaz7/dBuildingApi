from flask import jsonify, request
from Models.Contribution import Contribution, db


def get_contributions():
    contributions = Contribution.query.all()
    output = {
        'status': True if len(contributions) > 0 else False,
        'message': "OK" if len(contributions) > 0 else "Empty table",
        'data': []
    }
    for contribution in contributions:
        user_data = {'id': contribution.id, 'application_id': contribution.application_id, \
                     'summ': contribution.summ, 'period': contribution.period}
        output['data'].append(user_data)
    return jsonify(output)


def get_contribution(item_id):
    contribution = Contribution.query.get(item_id)
    if contribution:
        user_data = {'id': contribution.id, 'application_id': contribution.application_id, \
                     'summ': contribution.summ, 'period': contribution.period}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'Contribution not found'}), 404


def add_contribution():
    application_id = request.form.get('application_id')
    summ = request.form.get('summ', 0.0)
    period = request.form.get('period', 0)

    if not application_id:
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400

    new_contribution = Contribution(application_id=application_id, summ=summ, period=period)
    db.session.add(new_contribution)
    db.session.commit()

    # Получаем ID вставленной записи
    inserted_contribution_id = new_contribution.id

    return jsonify(
        {'status': True, 'message': 'Contribution added successfully', 'contribution_id': inserted_contribution_id}), 201


def update_contribution(item_id):
    contribution = Contribution.query.get(item_id)
    if not contribution:
        return jsonify({'status': False, 'message': 'Contribution not found'}), 404

    summ = request.form.get('summ')
    period = request.form.get('period')


    if summ:
        contribution.summ = summ
    if period:
        contribution.period = period

    db.session.commit()
    return jsonify({'status': True, 'message': 'Contribution updated successfully'})
