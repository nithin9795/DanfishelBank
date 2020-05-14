from flask_mongoengine import MongoEngine

from mongoengine import *




class Generalledger(Document):
    bank_name = StringField()
    branch_name = StringField()
    from_account = StringField()
    to_account = StringField()
    debit_amount = IntField()
    credit_amount = IntField()
    balance = IntField()
    transaction_date=DateTimeField()
    transaction_type=StringField()
    description=StringField()
    def to_json(self):
        return {
            "_id": str(self.pk),
            "bank_name": self.bank_name,
            "branch_name": self.branch_name,
            "from_account": self.from_account,
            "to_account": self.to_account,
            "debit_amount": self.debit_amount,
            "credit_amount": self.credit_amount,
            "balance": self.balance,
            "transaction_date": self.transaction_date,
            "transaction_type": self.transaction_type,
            "description": self.description,

            "public_id": self.public_id
        }
class HqVault(Document):
        bank_name = StringField()
        branch_name = StringField()
        from_account = StringField()
        to_account = StringField()
        debit_amount = IntField()
        credit_amount = IntField()
        balance = IntField()
        transaction_date = DateTimeField()
        transaction_type = StringField()
        description = StringField()

        def to_json(self):
            return {
                "_id": str(self.pk),
                "bank_name": self.bank_name,
                "branch_name": self.branch_name,
                "from_account": self.from_account,
                "to_account": self.to_account,
                "debit_amount": self.debit_amount,
                "credit_amount": self.credit_amount,
                "balance": self.balance,
                "transaction_date": self.transaction_date,
                "transaction_type": self.transaction_type,
                "description": self.description,

                "public_id": self.public_id
            }
class Vault(Document):
            bank_name = StringField()
            branch_name = StringField()
            from_account = StringField()
            to_account = StringField()
            debit_amount = IntField()
            credit_amount = IntField()
            balance = IntField()
            transaction_date = DateTimeField()
            transaction_type = StringField()
            description = StringField()

            def to_json(self):
                return {
                    "_id": str(self.pk),
                    "bank_name": self.bank_name,
                    "branch_name": self.branch_name,
                    "from_account": self.from_account,
                    "to_account": self.to_account,
                    "debit_amount": self.debit_amount,
                    "credit_amount": self.credit_amount,
                    "balance": self.balance,
                    "transaction_date": self.transaction_date,
                    "transaction_type": self.transaction_type,
                    "description": self.description,

                    "public_id": self.public_id
                }
disconnect(alias='generalledgerdb')