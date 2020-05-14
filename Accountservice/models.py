from flask_mongoengine import MongoEngine

from mongoengine import *




class SavingAccount(Document):
    name = StringField()
    bank_id = StringField(primary_key=True)
    branch_id = StringField(primary_key=True)
    account_no = StringField()
    customer_id = IntField(primary_key=True)
    account_type_id = IntField(primary_key=True)
    currency_id = IntField(primary_key=True)
    mini_balance_id=IntField(primary_key=True)
    interest_id=IntField(primary_key=True)
    transaction_id=StringField(primary_key=True)
    transaction_mode=StringField()
    net_balance=IntField()
    actual_balance=StringField()
    is_active=BooleanField()
    def to_json(self):
        return {
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
            "public_id": self.public_id
        }

disconnect(alias='generalledgerdb')