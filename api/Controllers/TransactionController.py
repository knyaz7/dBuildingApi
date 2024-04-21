from flask import jsonify, request
from Models.Transaction import Transaction, db


def get_transactions():
    transactions = Transaction.query.all()
    output = {
        'status': True if len(transactions) > 0 else False,
        'message': "OK" if len(transactions) > 0 else "Empty table",
        'data': []
    }
    for transaction in transactions:
        user_data = {'id': transaction.id, 'application_id': transaction.application_id, \
                     'input_wallet': transaction.input_wallet, 'output_wallet': transaction.output_wallet, \
                        'summ': transaction.summ}
        output['data'].append(user_data)
    return jsonify(output)


def get_transaction(item_id):
    transaction = Transaction.query.get(item_id)
    if transaction:
        user_data = {'id': transaction.id, 'application_id': transaction.application_id, \
                     'input_wallet': transaction.input_wallet, 'output_wallet': transaction.output_wallet, \
                        'summ': transaction.summ}
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'Translation not found'}), 404


def add_transaction():
    application_id = request.form.get('application_id')
    input_wallet = request.form.get('input_wallet', "")
    output_wallet = request.form.get('output_wallet', "")
    summ = request.form.get('summ', 0.0)

    if not application_id:
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400

    new_translation = Transaction(application_id=application_id, input_wallet=input_wallet, output_wallet=output_wallet, summ=summ)
    db.session.add(new_translation)
    db.session.commit()

    # Получаем ID вставленной записи
    inserted_translation_id = new_translation.id

    return jsonify(
        {'status': True, 'message': 'Translation added successfully', 'transaction_id': inserted_translation_id}), 201


def update_transaction(item_id):
    transaction = Transaction.query.get(item_id)
    if not transaction:
        return jsonify({'status': False, 'message': 'Translation not found'}), 404

    input_wallet = request.form.get('input_wallet')
    output_wallet = request.form.get('output_wallet')
    summ = request.form.get('summ')

    if input_wallet:
        transaction.input_wallet = input_wallet
    if output_wallet:
        transaction.output_wallet = output_wallet
    if summ:
        transaction.summ = summ

    db.session.commit()
    return jsonify({'status': True, 'message': 'Transaction updated successfully'})
