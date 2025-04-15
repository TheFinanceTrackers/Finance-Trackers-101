from app import db, Transaction, app  # Import both db and Transaction

# Create an app context to allow database queries
with app.app_context():
    transactions = Transaction.query.all()
    for t in transactions:
        print(f"ID: {t.id}, Description: {t.description}, Amount: {t.amount}, Category: {t.category}, Date: {t.date}")
