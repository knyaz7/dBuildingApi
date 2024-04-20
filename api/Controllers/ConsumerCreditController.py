from flask import jsonify, request
from Models.ConsumerCredit import ConsumerCredit, db

def get_consumercredits():
    consumercredits = ConsumerCredit.query.all()
    output = {
        'status': True if len(consumercredits) > 0 else False,
        'message': "OK" if len(consumercredits) > 0 else "Empty table",
        'data': []
    }
    for consumercredit in consumercredits:
        user_data = {'id': consumercredit.id, 'application_id' : consumercredit.application_id, \
                     'summ': consumercredit.summ, 'point': consumercredit.point, \
                        'period': consumercredit.period, 'title': consumercredit.title, \
                            'inn': consumercredit.inn, 'fact_adress': consumercredit.fact_adress, \
                                'avg_earning': consumercredit.avg_earning}
        output['data'].append(user_data)
    return jsonify(output)

def get_consumercredit(item_id):
    consumercredit = ConsumerCredit.query.get(item_id)
    if consumercredit:
        user_data = {'id': consumercredit.id, 'application_id' : consumercredit.application_id, \
                     'summ': consumercredit.summ, 'point': consumercredit.point, \
                        'period': consumercredit.period, 'title': consumercredit.title, \
                            'inn': consumercredit.inn, 'fact_adress': consumercredit.fact_adress, \
                                'avg_earning': consumercredit.avg_earning}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'ConsumerCredit not found'}), 404

    
def add_consumercredit():
    application_id = request.form.get('application_id')
    summ = request.form.get('summ', 0.0)
    point = request.form.get('point', "")
    period = request.form.get('period', 0.0)
    title = request.form.get('title', "")
    inn = request.form.get('inn', "")
    fact_adress = request.form.get('fact_adress', "")
    avg_earning = request.form.get('avg_earning', 0.0)
    
    if not application_id:
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400

    new_consumercredit = ConsumerCredit(application_id=application_id, summ=summ, point=point, period = period, \
                                  title=title, inn=inn, fact_adress=fact_adress, avg_earning=avg_earning)
    db.session.add(new_consumercredit)
    db.session.commit()

    # Получаем ID вставленной записи
    inserted_autocredit_id = new_consumercredit.id

    return jsonify({'status': True, 'message': 'ConsumerCredit added successfully', 'application_id': inserted_autocredit_id}), 201

def update_consumercredit(item_id):
    autocredit = ConsumerCredit.query.get(item_id)
    if not autocredit:
        return jsonify({'status': False, 'message': 'ConsumerCredit not found'}), 404

    summ = request.form.get('summ')
    point = request.form.get('point')
    period = request.form.get('period')
    title = request.form.get('title')
    inn = request.form.get('inn')
    fact_adress = request.form.get('fact_adress')
    avg_earning = request.form.get('avg_earning')

    if period:
        autocredit.period = period
    if summ:
        autocredit.summ = summ
    if point:
        autocredit.point = point
    if title:
        autocredit.title = title
    if inn:
        autocredit.inn = inn
    if fact_adress:
        autocredit.fact_adress = fact_adress
    if avg_earning:
        autocredit.avg_earning = avg_earning

    db.session.commit()
    return jsonify({'status': True, 'message': 'ConsumerCredit updated successfully'})
