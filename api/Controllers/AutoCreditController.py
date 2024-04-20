from flask import jsonify, request
from Models.AutoCredit import AutoCredit, db

def get_autocredits():
    autocredits = AutoCredit.query.all()
    output = {
        'status': True if len(autocredits) > 0 else False,
        'message': "OK" if len(autocredits) > 0 else "Empty table",
        'data': []
    }
    for autocredit in autocredits:
        user_data = {'id': autocredit.id, 'application_id' : autocredit.application_id, \
                     'car_price': autocredit.car_price, 'first_payment': autocredit.first_payment, \
                        'period': autocredit.period, 'title': autocredit.title, \
                            'inn': autocredit.inn, 'fact_adress': autocredit.fact_adress, \
                                'avg_earning': autocredit.avg_earning}
        output['data'].append(user_data)
    return jsonify(output)

def get_autocredit(item_id):
    autocredit = AutoCredit.query.get(item_id)
    if autocredit:
        user_data = {'id': autocredit.id, 'application_id' : autocredit.application_id, \
                     'car_price': autocredit.car_price, 'first_payment': autocredit.first_payment, \
                        'period': autocredit.period, 'title': autocredit.title, \
                            'inn': autocredit.inn, 'fact_adress': autocredit.fact_adress, \
                                'avg_earning': autocredit.avg_earning}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'AutoCredit not found'}), 404

    
def add_autocredit():
    application_id = request.form.get('application_id')
    car_price = request.form.get('car_price', 0.0)
    first_payment = request.form.get('first_payment', 0.0)
    period = request.form.get('period', 0.0)
    title = request.form.get('title', "")
    inn = request.form.get('inn', "")
    fact_adress = request.form.get('fact_adress', "")
    avg_earning = request.form.get('avg_earning', 0.0)
    
    if not application_id:
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400

    new_autocredit = AutoCredit(application_id=application_id, car_price=car_price, first_payment=first_payment, period = period, \
                                  title=title, inn=inn, fact_adress=fact_adress, avg_earning=avg_earning)
    db.session.add(new_autocredit)
    db.session.commit()

    # Получаем ID вставленной записи
    inserted_autocredit_id = new_autocredit.id

    return jsonify({'status': True, 'message': 'Application added successfully', 'application_id': inserted_autocredit_id}), 201

def update_autocredit(item_id):
    autocredit = AutoCredit.query.get(item_id)
    if not autocredit:
        return jsonify({'status': False, 'message': 'AutoCredit not found'}), 404

    car_price = request.form.get('status')
    first_payment = request.form.get('status')
    period = request.form.get('status')
    title = request.form.get('status')
    inn = request.form.get('status')
    fact_adress = request.form.get('status')
    avg_earning = request.form.get('status')

    if car_price:
        autocredit.car_price = car_price
    if first_payment:
        autocredit.first_payment = first_payment
    if period:
        autocredit.period = period
    if title:
        autocredit.title = title
    if inn:
        autocredit.inn = inn
    if fact_adress:
        autocredit.fact_adress = fact_adress
    if avg_earning:
        autocredit.avg_earning = avg_earning

    db.session.commit()
    return jsonify({'status': True, 'message': 'Application updated successfully'})
