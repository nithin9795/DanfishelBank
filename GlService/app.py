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
db = client.generalledgerdb
collection = db.generalledger
# app = Flask(__name__)

#Genearal ledger Transaction
@app.route('/gltransfer',methods=['POST'])
def gl():
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
        cursor = list(db.generalledger.find().sort('transaction_date', -1).limit(1))
        balance = ''
        for r in cursor:
            balance = r['balance']

        print('balance', balance)
        if from_account == to_account:
            transaction_type = "DP"
            credit_amount = transferd_amount
            debit_amount = 0
            balance = int(transferd_amount)+ int(balance)


            gl = Generalledger.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,
                                              to_account=to_account,
                                              credit_amount=credit_amount, debit_amount=debit_amount, balance=balance,
                                              transaction_date=transaction_date, transaction_type=transaction_type,
                                              description=description)
            gl.save()
            return (jsonify({'message': 'Amount is Transfered Sucessfully'}))
        else:
            if(transferd_amount<=balance):#checking whether the transfered amount is less than the actual balance
                debit_amount = transferd_amount
                transaction_type = "TX"
                credit_amount = 0
                balance = int(balance)- int(transferd_amount) #updated balance

                gl = Generalledger.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,to_account=to_account,
                                                    credit_amount=credit_amount,debit_amount=debit_amount,balance=balance,transaction_date=transaction_date,transaction_type=transaction_type,description=description)
                gl.save() #save in generalledger
                debit_amount = 0
                transaction_type = "DP"
                credit_amount = transferd_amount
                balance = int(balance)+ int(transferd_amount) #updated balance
                hqvault=HqVault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,to_account=to_account,
                                                    credit_amount=credit_amount,debit_amount=debit_amount,balance=balance,transaction_date=transaction_date,transaction_type=transaction_type,description=description)
                hqvault.save() #saves in hq vault
                return (jsonify({'message': 'Amount is Transfered Sucessfully'}))
            else:
                return (jsonify({'message': 'Insufficient Balance'}))



#General ledger account report
@app.route('/glreport', methods=['GET'])

def glreport():

    report = Generalledger.objects.filter()
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
        cursor = list(db.hq_vault.find().sort('transaction_date', -1).limit(1))

        balance = ''
        for r in cursor:
            balance = r['balance']

        #if from and to account is equal user can deposit in his own account
        if from_account == to_account:
            transaction_type = "DP"
            credit_amount = transferd_amount
            debit_amount = 0
            balance=int(balance)+ int(transferd_amount)
            hqvault = HqVault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,
                                        to_account=to_account,
                                        credit_amount=credit_amount, debit_amount=debit_amount, balance=balance,
                                        transaction_date=transaction_date, transaction_type=transaction_type,
                                        description=description)
            hqvault.save()
        else:
            if(transferd_amount<=balance):#checking whether the transfered amount is less than the actual balance
                debit_amount = transferd_amount
                transaction_type = "TX"
                credit_amount = 0
                balance=int(balance)- int(transferd_amount) #updated balance
                hqvault = HqVault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,to_account=to_account,
                                                credit_amount=credit_amount,debit_amount=debit_amount,balance=balance,transaction_date=transaction_date,transaction_type=transaction_type,description=description)

                hqvault.save() #save in hq_vault

                transaction_type = "DP"
                debit_amount = 0
                credit_amount = transferd_amount
                balance = int(balance)+ int(transferd_amount) #updated balance
                vault = Vault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,
                                             to_account=to_account,
                                             credit_amount=credit_amount, debit_amount=debit_amount, balance=balance,
                                             transaction_date=transaction_date, transaction_type=transaction_type,
                                             description=description)
                vault.save() #saves in vault

                return (jsonify({'message': 'Amount is Transfered Sucessfully'}))
            else:
                return (jsonify({'message': 'Insufficient Balance'}))


#head branch Transacton report
def hqreport():

    report = HqVault.objects.filter()

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
        cursor = list(collection.find().sort('transaction_date', -1).limit(1))

        balance = ''
        for r in cursor:
            balance = r['balance']
        if transferd_amount <=balance:
            debit_amount = transferd_amount
            transaction_type = "TX"
            credit_amount = 0
            balance=int(balance)- int(transferd_amount) #updated balance
            vault = HqVault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,
                                           to_account=to_account,
                                           credit_amount=credit_amount, debit_amount=debit_amount, balance=balance,
                                           transaction_date=transaction_date, transaction_type=transaction_type,
                                           description=description)
            vault.save() #saves in vault

            debit_amount = transferd_amount
            transaction_type = "DP"
            credit_amount = transferd_amount
            balance = int(balance)+ int(transferd_amount) #updated balance
            hqvault = Vault.objects.create(bank_name=bank_name, branch_name=branch_name, from_account=from_account,
                                           to_account=to_account,
                                           credit_amount=credit_amount, debit_amount=debit_amount, balance=balance,
                                           transaction_date=transaction_date, transaction_type=transaction_type,
                                           description=description)
            hqvault.save() #saves in hqvauult
            return (jsonify({'message': 'Amount is Transfered Sucessfully'}))



#child branch Transacton report
def hqreport():
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
    app.run(host='0.0.0.0', port=5000, debug=True)

