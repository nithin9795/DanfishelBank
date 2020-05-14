from datetime import datetime
from json import dumps

import pymongo

from GlService.models import Generalledger, HqVault,Vault
from GlService.dbconfig import *
from flask import Flask,abort
from pymongo import MongoClient

from flask import jsonify
from flask import request




client = MongoClient()
db = client.generlledgerdb
collection = db.generalledger
app = Flask(__name__)

#Genearal ledger Transaction
@app.route('/gltransfer',methods=['POST'])
def add_post():
    bank_name = request.json['bank_name']
    branch_name = request.json['branch_name']
    from_account = request.json['from_account']
    to_account = request.json['to_account']
    transferd_amount = request.json['transferd_amount']

    description = request.json['description']
    transaction_date = datetime.now()
    print('hello',transaction_date)



    if from_account and to_account and transferd_amount and description and bank_name and branch_name and request.method   == 'POST':
        # to fetch the previous collection balance and add that with transfered amount
        cursor = list(collection.find().sort('_id', -1).limit(100))
        print(cursor)
        for i in cursor:
            print(i)
            #balance=i.balance
        if from_account == to_account:
            transaction_type = "DP"
            credit_amount = transferd_amount
            debit_amount = 0
            #balance = transferd_amount+ balance
            balance=transferd_amount

            gl = Generalledger.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,
                                              to_account=to_account,
                                              credit_amount=credit_amount, debit_amount=debit_amount, balance=balance,
                                              transaction_date=transaction_date, transaction_type=transaction_type,
                                              description=description)
            gl.save()
            return (jsonify({'message': 'Amount is Transfered Sucessfully'}))
        else:
            debit_amount = transferd_amount
            transaction_type = "TX"
            credit_amount = 0
        balance = transferd_amount

        gl = Generalledger.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,to_account=to_account,
                                            credit_amount=credit_amount,debit_amount=debit_amount,balance=balance,transaction_date=transaction_date,transaction_type=transaction_type,description=description)
        gl.save()
        hqvault=HqVault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,to_account=to_account,
                                            credit_amount=credit_amount,debit_amount=debit_amount,balance=balance,transaction_date=transaction_date,transaction_type=transaction_type,description=description)
        hqvault.save()
        return (jsonify({'message': 'Amount is Transfered Sucessfully'}))



#General ledger account report
@app.route('/glreport', methods=['GET'])

def glreport():
    cursor = collection.find().sort('_id',-1).limit(100)
    print('cursor',cursor) #printing <pymongo.cursor.Cursor object at 0x000001E775B84610>
    data=[]

    for i in cursor: #note-------->its not going inside the loop
        res=i.balance
        print(res)


    report = Generalledger.objects.filter()
    print(report,'report------->')
    if not report:
        abort(400)
    result = []
    for u in report:
        report_data = {}
        report_data['bank_name'] = u.bank_name
        report_data['branch_name'] = u.branch_name
        report_data['from_account'] = u.from_account
        report_data['to_account'] = u.to_account
        report_data['debit_amount'] = u.debit_amount
        report_data['credit_amount'] = u.credit_amount
        report_data['balance'] = u.balance
        report_data['transaction_date'] = u.transaction_date
        report_data['transaction_type'] = u.transaction_type
        report_data['description'] = u.description
        result.append(report_data)

    return jsonify({'user': result})


#head branch amount transaction
@app.route('/hqtransfer',methods=['POST'])
def hqTransfer():
    bank_name = request.json['bank_name']
    branch_name = request.json['branch_name']
    from_account = request.json['from_account']
    to_account = request.json['to_account']
    transferd_amount = request.json['transferd_amount']

    description = request.json['description']
    transaction_date = datetime.now()


    if from_account and to_account and transferd_amount and description and bank_name and branch_name and request.method   == 'POST':
        # to fetch the previous collection balance and add that with transfered amount
        cursor = list(collection.find().sort('_id', -1).limit(100))
        print(cursor)
        for i in cursor:
            print(i)
        balance = transferd_amount
        if from_account == to_account:
            transaction_type = "DP"
            credit_amount = transferd_amount
            debit_amount = 0

            hqvault = HqVault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,
                                        to_account=to_account,
                                        credit_amount=credit_amount, debit_amount=debit_amount, balance=balance,
                                        transaction_date=transaction_date, transaction_type=transaction_type,
                                        description=description)
            hqvault.save()
        else:
            debit_amount = transferd_amount
            transaction_type = "TX"
            credit_amount = 0

            hqvault = HqVault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,to_account=to_account,
                                            credit_amount=credit_amount,debit_amount=debit_amount,balance=balance,transaction_date=transaction_date,transaction_type=transaction_type,description=description)
            hqvault.save()
            transaction_type = "DP"
            vault = Vault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,
                                         to_account=to_account,
                                         credit_amount=credit_amount, debit_amount=debit_amount, balance=balance,
                                         transaction_date=transaction_date, transaction_type=transaction_type,
                                         description=description)
            vault.save()
            return (jsonify({'message': 'Amount is Transfered Sucessfully'}))


#head branch Transacton report
def hqreport():
    cursor = collection.find().sort('_id',-1).limit(100)
    print('cursor',cursor) #printing <pymongo.cursor.Cursor object at 0x000001E775B84610>
    data=[]

    for i in cursor: #note-------->its not going inside the loop
        res=i.balance
        print(res)


    report = HqVault.objects.filter()
    print(report,'report------->')
    if not report:
        abort(400)
    result = []
    for u in report:
        report_data = {}
        report_data['bank_name'] = u.bank_name
        report_data['branch_name'] = u.branch_name
        report_data['from_account'] = u.from_account
        report_data['to_account'] = u.to_account
        report_data['debit_amount'] = u.debit_amount
        report_data['credit_amount'] = u.credit_amount
        report_data['balance'] = u.balance
        report_data['transaction_date'] = u.transaction_date
        report_data['transaction_type'] = u.transaction_type
        report_data['description'] = u.description
        result.append(report_data)

    return jsonify({'user': result})

# child branch amount transaction
@app.route('/vaulttransfer',methods=['POST'])
def VaultTransfer():
    bank_name = request.json['bank_name']
    branch_name = request.json['branch_name']
    from_account = request.json['from_account']
    to_account = request.json['to_account']
    transferd_amount = request.json['transferd_amount']

    description = request.json['description']
    transaction_date = datetime.now()


    if from_account and to_account and transferd_amount and description and bank_name and branch_name and request.method   == 'POST':
        # to fetch the previous collection balance and add that with transfered amount
        cursor = list(collection.find().sort('_id', -1).limit(100))
        print(cursor)
        for i in cursor:
            print(i)
        balance = transferd_amount
        if from_account == to_account:
            transaction_type = "DP"
            credit_amount = transferd_amount
            debit_amount = 0

            vault = Vault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,
                                        to_account=to_account,
                                        credit_amount=credit_amount, debit_amount=debit_amount, balance=balance,
                                        transaction_date=transaction_date, transaction_type=transaction_type,
                                        description=description)
            vault.save()
        else:
            debit_amount = transferd_amount
            transaction_type = "TX"
            credit_amount = 0

            vault = HqVault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,to_account=to_account,
                                            credit_amount=credit_amount,debit_amount=debit_amount,balance=balance,transaction_date=transaction_date,transaction_type=transaction_type,description=description)
            vault.save()
            transaction_type = "DP"
            hqvault = Vault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,
                                         to_account=to_account,
                                         credit_amount=credit_amount, debit_amount=debit_amount, balance=balance,
                                         transaction_date=transaction_date, transaction_type=transaction_type,
                                         description=description)
            hqvault.save()
            return (jsonify({'message': 'Amount is Transfered Sucessfully'}))


#child branch Transacton report
def hqreport():
    cursor = collection.find().sort('_id',-1).limit(100)
    print('cursor',cursor) #printing <pymongo.cursor.Cursor object at 0x000001E775B84610>
    data=[]

    for i in cursor: #note-------->its not going inside the loop
        res=i.balance
        print(res)


    report = HqVault.objects.filter()
    print(report,'report------->')
    if not report:
        abort(400)
    result = []
    for u in report:
        report_data = {}
        report_data['bank_name'] = u.bank_name
        report_data['branch_name'] = u.branch_name
        report_data['from_account'] = u.from_account
        report_data['to_account'] = u.to_account
        report_data['debit_amount'] = u.debit_amount
        report_data['credit_amount'] = u.credit_amount
        report_data['balance'] = u.balance
        report_data['transaction_date'] = u.transaction_date
        report_data['transaction_type'] = u.transaction_type
        report_data['description'] = u.description
        result.append(report_data)

    return jsonify({'user': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)

