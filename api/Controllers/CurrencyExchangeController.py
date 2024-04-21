from flask import jsonify, request
from Models.CurrencyExchange import CurrencyExchange, db


def get_currencyexchanges():
    currencyexchanges = CurrencyExchange.query.all()
    output = {
        'status': True if len(currencyexchanges) > 0 else False,
        'message': "OK" if len(currencyexchanges) > 0 else "Empty table",
        'data': []
    }
    for currencyexchange in currencyexchanges:
        user_data = {'id': currencyexchange.id, 'application_id': currencyexchange.application_id, \
                     'summ': currencyexchange.summ, 'currency_user': currencyexchange.currency_user, \
                        'currency_bank': currencyexchange.currency_bank}
        output['data'].append(user_data)
    return jsonify(output)


def get_currencyexchange(item_id):
    currencyexchange = CurrencyExchange.query.get(item_id)
    if currencyexchange:
        user_data = {'id': currencyexchange.id, 'application_id': currencyexchange.application_id, \
                     'summ': currencyexchange.summ, 'currency_user': currencyexchange.currency_user, \
                        'currency_bank': currencyexchange.currency_bank}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'CurrencyExchange not found'}), 404


def add_currencyexchange():
    application_id = request.form.get('application_id')
    summ = request.form.get('summ', 0.0)
    currency_user = request.form.get('currency_user', "")
    currency_bank = request.form.get('currency_bank', "")

    if not application_id:
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400

    new_currencyexchange = CurrencyExchange(application_id=application_id, summ=summ, currency_user=currency_user, currency_bank=currency_bank)
    db.session.add(new_currencyexchange)
    db.session.commit()

    # Получаем ID вставленной записи
    inserted_currencyexchange_id = new_currencyexchange.id

    return jsonify(
        {'status': True, 'message': 'CurrencyExchange added successfully', 'currencyexchange_id': inserted_currencyexchange_id}), 201


def update_currencyexchange(item_id):
    currencyexchange = CurrencyExchange.query.get(item_id)
    if not currencyexchange:
        return jsonify({'status': False, 'message': 'CurrencyExchange not found'}), 404

    summ = request.form.get('summ')
    currency_user = request.form.get('currency_user')
    currency_bank = request.form.get('currency_bank')

    if summ:
        currencyexchange.summ = summ
    if currency_user:
        currencyexchange.currency_user = currency_user
    if currency_bank:
        currencyexchange.currency_bank = currency_bank

    db.session.commit()
    return jsonify({'status': True, 'message': 'CurrencyExchange updated successfully'})
