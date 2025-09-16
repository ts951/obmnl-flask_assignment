# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/", methods = ["GET"])
def get_transactions():
    return render_template('transactions.html', transactions = transactions)

# Create operation
@app.route("/add", methods = ["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        transaction = {
            'id': len(transactions)+1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }

        transactions.append(transaction)
        return redirect(url_for('get_transactions'))
    return render_template('form.html')
    
# Update operation
@app.route("/edit/<int:transaction_id>", methods = ["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":        
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = request.form['date']
                transaction['amount'] = float(request.form['amount'])
        return redirect(url_for("get_transactions"))
    
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template('edit.html', transaction = transaction)

    return {"message": "Transaction with provided id not found"}, 404

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break

    return redirect(url_for('get_transactions'))

# Search operation
@app.route("/search", methods = ["GET", "POST"])
def search_transaction():
    if request.method == "POST":
        min_amount = float(request.form["min_amount"])
        max_amount = float(request.form["max_amount"])
        filtered_transactions = [transaction for transaction in transactions if min_amount <= transaction['amount'] <= max_amount]
        return render_template('transactions.html', transactions = filtered_transactions)

    return render_template('search.html')

# Get total balance operation
@app.route("/balance")
def total_balance():
    total_amount = 0
    for transaction in transactions:
        total_amount += transaction['amount']
    balance_message = f"Total Balance: {total_amount}"

    return render_template("transactions.html", transactions = transactions, balance = balance_message)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
