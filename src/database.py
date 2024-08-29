from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    memo = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.id} {self.type} {self.amount}>'
