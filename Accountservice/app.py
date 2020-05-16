from datetime import datetime, date

from flask import Flask, request, jsonify,abort

from flask_pymongo import MongoClient
from mongoengine import StringField

from Accountservice.dbconfig import app
from Accountservice.models import SavingAccount,SavingInterest



client = MongoClient()
db = client.savingaccount_service
collection = db.saving_account

#Saving Account  post method
@app.route('/sacccreate',methods=['POST'])
def saving_acc():
    name = request.json['name']
    bank_id = request.json['bank_id']
    branch_id = request.json['branch_id']
    account_no = request.json['account_no']
    customer_id = request.json['customer_id']
    account_type_id=request.json['account_type_id']
    currency_id = request.json['currency_id']
    mini_balance_id = request.json['mini_balance_id']
    interest_id = request.json['interest_id']
    transaction_id = request.json['transaction_id']
    #transaction_mode = request.json['transaction_mode']
    net_balance = request.json['net_balance']
    actual_balance = request.json['actual_balance']




    if name and bank_id and branch_id and account_no and customer_id and account_type_id and currency_id and mini_balance_id and \
      interest_id and transaction_id  and net_balance and actual_balance  and  request.method   == 'POST':
            #Checking  whether the acc is existing or acc
            existingacc = SavingAccount.objects.filter(account_no=account_no).count()
            if existingacc==0:

                transaction_mode='DP'
                is_active=True
                sav_acc = SavingAccount.objects.create(name=name, bank_id=bank_id, account_no=account_no,branch_id=branch_id,
                                              customer_id=customer_id,
                                              account_type_id=account_type_id, currency_id=currency_id, mini_balance_id=mini_balance_id,
                                              interest_id=interest_id, transaction_id=transaction_id,
                                              transaction_mode=transaction_mode,net_balance=net_balance,
                                                   actual_balance=actual_balance,is_active=is_active)
                sav_acc.save()
                return (jsonify({'message': ' Saving Accounnt is Created Sucessfully'}))
            else:
                return (jsonify({'message': 'Saving Accounnt already exist'}))
    else:
       abort(400)  # missing arguments

@app.route('/saccupdate/<account_no>', methods=['PUT'])#update by accno
def update_saccbyaccno(account_no):
    # Getting values

    name = request.json["name"]

    customer_id = request.json['customer_id']
    account_type_id = request.json['account_type_id']
    currency_id = request.json['currency_id']
    mini_balance_id = request.json['mini_balance_id']
    interest_id = request.json['interest_id']


    # validate the received values
    if name  and customer_id and account_type_id and currency_id and \
            mini_balance_id and interest_id  and request.method == 'PUT':
        # save edits
        #update query
        SavingAccount.objects.filter(account_no=account_no).update(name=name, customer_id=customer_id, account_type_id=account_type_id,
                                              currency_id=currency_id,mini_balance_id=mini_balance_id, interest_id=interest_id)
        resp = jsonify('Saving  Account  updated successfully')
        return resp

@app.route('/saccupdate/<id>', methods=['PUT'])#update by id
def update_saccbyid(id):
    # Getting values

    name = request.json["name"]

    customer_id = request.json['customer_id']
    account_type_id = request.json['account_type_id']
    currency_id = request.json['currency_id']
    mini_balance_id = request.json['mini_balance_id']
    interest_id = request.json['interest_id']


    # validate the received values
    if name  and customer_id and account_type_id and currency_id and \
            mini_balance_id and interest_id  and request.method == 'PUT':
        # save edits
        #update query
        SavingAccount.objects.filter(id=id).update(name=name, customer_id=customer_id, account_type_id=account_type_id,
                                              currency_id=currency_id,mini_balance_id=mini_balance_id, interest_id=interest_id)
        resp = jsonify('Saving  Account  updated successfully')
        return resp

@app.route('/sacc', methods=['GET'])
def all_sacc(): #fetches all the saving acc details

    resp = SavingAccount.objects.all()
    result = []
    for u in resp:
        result.append(u.to_json())
    return jsonify({'Saving  Account details': result})


@app.route('/sacc/<account_no>', methods=['GET'])
def getemployeeattendance(account_no): #fetches details based on accno

    sacc = SavingAccount.objects.get(account_no=account_no)
    return sacc.to_json()

@app.route('/saccintcreate',methods=['POST'])
def saving_acc_interest(): #to post saving account interest
    sav_acc_id = request.json['sav_acc_id']
    interest_charge = request.json['interest_charge']
    reason = request.json['reason']

    if sav_acc_id and interest_charge and reason  and request.method   == 'POST':


                charged_on = datetime.now()
                sav_acc = SavingInterest.objects.create(sav_acc_id=sav_acc_id, interest_charge=interest_charge, reason=reason,charged_on=charged_on)
                sav_acc.save()
                return (jsonify({'message': ' Saving Accounnt Interest is Created Sucessfully'}))

    else:
       abort(400)  # missing arguments

@app.route('/saccint', methods=['GET'])
def all_sacc_int():
    # query to select all values from database
    resp = SavingInterest.objects.all()
    result = []
    for u in resp:
        result.append(u.to_json())
    return jsonify({'Saving  Account Interest details': result})

@app.route('/saccintupdate/<id>', methods=['PUT'])
def update_saccint(id):
    # Getting values

    interest_charge = request.json["interest_charge"]

    reason = request.json['reson']



    # validate the received values
    if interest_charge  and reason and request.method == 'PUT':
        # save edits
        #update query
        SavingInterest.objects.filter(id=id).update(interest_charge=interest_charge, reason=reason)
        resp = jsonify('Saving  Account Interest  updated successfully')
        return resp

@app.route('/deletesavacc/<id>', methods=['DELETE'])
def delete_savaccbyid(id): #delete saving account based on id

    result=SavingAccount.objects.get(id=id)
    # delete the selected BranchSpecification
    result.delete()
    resp = jsonify('Saving  Account Details deleted successfully!')
    resp.status_code = 200
    return resp

@app.route('/deletesavacc/<accountno>', methods=['DELETE'])
def delete_savaccbyaccountno(accountno): #dalete saving account based on account number
    # query to select the SavingAccount
    result=SavingAccount.objects.get(accountno=accountno)
    # delete the selected SavingAccount
    result.delete()
    resp = jsonify('Saving  Account Details deleted successfully!')
    resp.status_code = 200
    return resp

@app.route('/deletesavaccint/<id>', methods=['DELETE'])
def delete_savaccint(id): #delet saving account interest based on id
    # query to select the SavingAccount
    result=SavingInterest.objects.get(id=id)
    # delete the selected SavingAccount
    result.delete()
    resp = jsonify('Saving  Account Details Interest deleted successfully!')
    resp.status_code = 200
    return resp

#Amount crediting to particular Account
@app.route('/sacccri/<accno>', methods=['PUT'])
def savacc_credit(accno):
    amount = request.json['amount']
    print(accno,'account number')
    result = list(collection.find({}, {'account_no':accno}))
    res=list(collection.find({'account_no': accno}))


    balance=''
    for r in res:
        balance=r['actual_balance']
    print(balance,'wwdkjhskjdhksjhdkjsh>>>>>>')
    actual_balance=(int(amount)+int(balance))
    print('actual_bal=',actual_balance)
    transaction_mode='DP'
    today = str(date.today())
    print(today)  # '2017-12
    if amount  and request.method == 'PUT':
        SavingAccount.objects.filter(account_no=accno).update(actual_balance=actual_balance, transaction_mode=transaction_mode)
    resp = jsonify('Your account no',accno,'is credited with INR',amount,'on',today ,'. Current Balance is INR',actual_balance)
    return resp

#Amount Debiting From particular Account
@app.route('/saccdep/<accno>', methods=['PUT'])
def savacc_debit(accno):
    amount = request.json['amount']
    print(accno,'account number')
    # result = list(collection.find({}, {'account_no':accno}))
    res=list(collection.find({'account_no': accno}))


    balance=''
    for r in res:
        balance=r['actual_balance']
    print(balance,'wwdkjhskjdhksjhdkjsh>>>>>>')
    #Checking whether the requested amount is less than or equal to actual balance
    if(amount<=balance):
        actual_balance=(int(balance)-int(amount))
        print('actual_bal=',actual_balance)
        transaction_mode='DP'
        today = str(date.today())
        print(today)  # '2017-12
        if amount  and request.method == 'PUT':
            SavingAccount.objects.filter(account_no=accno).update(actual_balance=actual_balance, transaction_mode=transaction_mode)
        resp = jsonify('Your account no',accno,'is debited with INR',amount,'on',today ,'. Current Balance is INR',actual_balance)
        return resp

    else:
        resp = jsonify('Insufficient Balance')
        return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)