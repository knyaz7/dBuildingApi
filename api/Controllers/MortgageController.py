from flask import jsonify, request
from Models.Mortgage import Mortgage, db


def get_mortgages():
    mortgages = Mortgage.query.all()
    output = {
        'status': True if len(mortgages) > 0 else False,
        'message': "OK" if len(mortgages) > 0 else "Empty table",
        'data': []
    }
    for mortgage in mortgages:
        user_data = {'id': mortgage.id, 'application_id': mortgage.application_id, \
                     'summ': mortgage.summ, 'point': mortgage.point, 'first_payment': mortgage.first_payment, \
                     'period': mortgage.period, 'title': mortgage.title, \
                     'inn': mortgage.inn, 'fact_adress': mortgage.fact_adress, \
                     'avg_earning': mortgage.avg_earning}
        output['data'].append(user_data)
    return jsonify(output)


def get_mortgage(item_id):
    mortgage = Mortgage.query.get(item_id)
    if mortgage:
        user_data = {'id': mortgage.id, 'application_id': mortgage.application_id, \
                     'summ': mortgage.summ, 'point': mortgage.point, 'first_payment': mortgage.first_payment, \
                     'period': mortgage.period, 'title': mortgage.title, \
                     'inn': mortgage.inn, 'fact_adress': mortgage.fact_adress, \
                     'avg_earning': mortgage.avg_earning}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'Mortgage not found'}), 404


def add_mortgage():
    application_id = request.form.get('application_id')
    summ = request.form.get('summ', 0.0)
    point = request.form.get('point', "")
    first_payment = request.form.get('first_payment', 0.0)
    period = request.form.get('period', 0)
    title = request.form.get('title', "")
    inn = request.form.get('inn', "")
    fact_adress = request.form.get('fact_adress', "")
    avg_earning = request.form.get('avg_earning', 0.0)

    if not application_id:
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400

    new_mortgage = Mortgage(application_id=application_id, summ=summ, point=point, first_payment=first_payment, period=period, \
                                        title=title, inn=inn, fact_adress=fact_adress, avg_earning=avg_earning)
    db.session.add(new_mortgage)
    db.session.commit()

    # Получаем ID вставленной записи
    inserted_mortgage_id = new_mortgage.id

    return jsonify(
        {'status': True, 'message': 'Mortgage added successfully', 'mortgage_id': inserted_mortgage_id}), 201


def update_mortgage(item_id):
    mortgage = Mortgage.query.get(item_id)
    if not mortgage:
        return jsonify({'status': False, 'message': 'Mortgage not found'}), 404

    summ = request.form.get('summ')
    point = request.form.get('point')
    first_payment = request.form.get('first_payment')
    period = request.form.get('period')
    title = request.form.get('title')
    inn = request.form.get('inn')
    fact_adress = request.form.get('fact_adress')
    avg_earning = request.form.get('avg_earning')

    if period:
        mortgage.period = period
    if summ:
        mortgage.summ = summ
    if point:
        mortgage.point = point
    if first_payment:
        mortgage.first_payment = first_payment
    if title:
        mortgage.title = title
    if inn:
        mortgage.inn = inn
    if fact_adress:
        mortgage.fact_adress = fact_adress
    if avg_earning:
        mortgage.avg_earning = avg_earning

    db.session.commit()
    return jsonify({'status': True, 'message': 'Mortgage updated successfully'})
