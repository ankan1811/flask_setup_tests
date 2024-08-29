from flask import Blueprint, request, jsonify
from io import StringIO
import csv

from src.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from src.database import db, Transaction

tax_report = Blueprint("tax_report", __name__, url_prefix="")


@tax_report.route('/transactions', methods=['POST'])
def upload_transactions():
    if 'file' not in request.files:
        return "No file part", HTTP_400_BAD_REQUEST

    file = request.files['file']
    if file.filename == '':
        return "No selected file", HTTP_400_BAD_REQUEST

    file_content = file.read().decode('utf-8')
    csv_reader = csv.reader(StringIO(file_content), delimiter=',')

    invalid_rows = []
    valid_rows = 0

    for row in csv_reader:
        if not row or row[0].startswith("#"):
            continue

        if len(row) != 4:
            invalid_rows.append(row)
            continue  # Skip invalid rows

        date, type_, amount, memo = row
        try:
            amount = float(amount)
        except ValueError:
            invalid_rows.append(row)
            continue  # Skip invalid amount entries
            # Check for existing transaction to prevent duplicates
        existing_transaction = Transaction.query.filter_by(
            date=date, type=type_.strip(), amount=amount, memo=memo.strip()).first()

        if existing_transaction:
            continue  # Skip duplicates
        # Assuming Transaction model is already defined with date, type, amount, memo fields
        new_transaction = Transaction(
            date=date, type=type_, amount=amount, memo=memo)
        db.session.add(new_transaction)
        valid_rows += 1

    db.session.commit()
    print("Inserted Transactions:", db.session.query(Transaction).all())
    if invalid_rows:
        return jsonify({
            "message": f"Transactions uploaded successfully, but {len(invalid_rows)} row(s) were invalid and skipped.",
            "invalid_rows": invalid_rows,
            "valid_rows": valid_rows
        }), HTTP_200_OK

    return jsonify({
        "message": "All transactions uploaded successfully.",
        "valid_rows": valid_rows
    }), HTTP_200_OK


@tax_report.route('/report', methods=['GET'])
def generate_report():
    # Query for gross revenue
    gross_revenue_query = db.session.query(db.func.sum(Transaction.amount)).filter(
        db.func.trim(Transaction.type) == 'Income')
    gross_revenue = gross_revenue_query.scalar() or 0

    # Query for expenses
    expenses_query = db.session.query(db.func.sum(Transaction.amount)).filter(
        db.func.trim(Transaction.type) == 'Expense')
    expenses = expenses_query.scalar() or 0

    # Calculate net revenue
    net_revenue = gross_revenue - expenses

    # Debug output
    print(f"Gross Revenue Query: {gross_revenue_query}")
    print(f"Expenses Query: {expenses_query}")
    print(f"Gross Revenue: {gross_revenue}")
    print(f"Expenses: {expenses}")
    print(f"Net Revenue: {net_revenue}")

    return jsonify({
        "gross-revenue": gross_revenue,
        "expenses": expenses,
        "net-revenue": net_revenue
    })
