import unittest
import io
import csv
from src import create_app
from src.database import db, Transaction


class LawnMowingAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(
            {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        with self.app.app_context():
            # Clear the test database
            db.session.query(Transaction).delete()
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            # Clear the test database after each test
            db.session.query(Transaction).delete()
            db.session.commit()

    def test_upload_transactions(self):
        data = io.BytesIO(
            b"Date,Type,Amount($),Memo\n"
            b"2020-07-01,Expense,18.77,Gas\n"
            b"2020-07-04,Income,40.00,347 Woodrow\n"
        )
        response = self.client.post(
            '/transactions', data={'file': (data, 'data.csv')})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Transactions uploaded successfully", response.data)

        with self.app.app_context():
            transactions = db.session.query(Transaction).all()
            self.assertEqual(len(transactions), 2)
            self.assertEqual(transactions[0].amount, 18.77)
            self.assertEqual(transactions[1].amount, 40.00)

    def test_generate_report(self):
        with self.app.app_context():
            # Adding test data directly
            transactions = [
                Transaction(date='2020-07-01', type='Expense',
                            amount=18.77, memo='Gas'),
                Transaction(date='2020-07-04', type='Income',
                            amount=40.00, memo='347 Woodrow')
            ]
            db.session.add_all(transactions)
            db.session.commit()

        response = self.client.get('/report')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['gross-revenue'], 40.00)
        self.assertEqual(data['expenses'], 18.77)
        self.assertEqual(data['net-revenue'], 21.23)


if __name__ == '__main__':
    unittest.main()
