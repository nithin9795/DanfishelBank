from flask_mongoengine import MongoEngine

from mongoengine import *


class SavingAccount(Document):
    name = StringField()
    bank_id = StringField()
    branch_id = StringField()
    account_no = StringField()
    customer_id = IntField()
    account_type_id = IntField()
    currency_id = IntField()
    mini_balance_id=IntField()
    interest_id=IntField()
    transaction_id=StringField()
    transaction_mode=StringField()
    net_balance=IntField()
    actual_balance=IntField()
    is_active=BooleanField()
    def to_json(self):
        return\
            {
            "_id": str(self.pk),
            "name": self.name,
            "bank_id": self.bank_id,
            "branch_id": self.branch_id,
            "account_no": self.account_no,
            "customer_id": self.customer_id,
            "mini_balance_id": self.mini_balance_id,
            "interest_id": self.interest_id,
            "transaction_id": self.transaction_id,
            "transaction_mode": self.transaction_mode,
            "net_balance": self.net_balance,
            "actual_balance":self.actual_balance,
            "is_active":self.is_active,


            }

class SavingInterest(Document):
    sav_acc_id = ReferenceField(SavingAccount)
    interest_charge = IntField()
    reason = StringField()
    charged_on = DateTimeField()
    def to_json(self):
        return {
            "_id": str(self.pk),
            "Saving Account Id": self.sav_acc_id,
            "Interest Charge": self.interest_charge,
            "Reason": self.reason,
            "Charged On": self.charged_on
               }
#disconnect(alias='savingaccountdb')