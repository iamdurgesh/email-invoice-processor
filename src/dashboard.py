# src/dashboard.py

from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import os

# Get the absolute path to the project root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
TEMPLATE_DIR = os.path.join(BASE_DIR, "../templates")  # Ensure Flask finds the correct templates directory

# Debugging: Print the resolved template directory path
print(f"Looking for templates in: {TEMPLATE_DIR}")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

def get_db_client():
    """
    Establish a connection to MongoDB.
    """
    client = MongoClient("mongodb://localhost:27017/")
    return client

@app.route('/invoices', methods=['GET'])
def get_invoices():
    """
    API endpoint to retrieve all invoices as JSON.
    """
    client = get_db_client()
    db = client.invoice_db
    invoices = list(db.invoices.find({}))
    client.close()
    return dumps(invoices)

@app.route('/')
def index():
    """
    Render the dashboard with the list of invoices.
    """
    client = get_db_client()
    db = client.invoice_db
    invoices = list(db.invoices.find({}))
    client.close()
    invoices_json = dumps(invoices)  # Convert to JSON format
    return render_template("index.html", invoices=invoices_json)

@app.route('/edit/<invoice_id>', methods=['GET', 'POST'])
def edit_invoice(invoice_id):
    """
    Allow users to edit and update an invoice.
    """
    client = get_db_client()
    db = client.invoice_db
    invoices = db.invoices

    if request.method == 'POST':
        # Update the invoice record in MongoDB
        updated_data = {
            "sender": request.form.get("sender"),
            "invoice_number": request.form.get("invoice_number"),
            "total_amount": request.form.get("total_amount"),
            "due_date": request.form.get("due_date")
        }
        invoices.update_one({"_id": ObjectId(invoice_id)}, {"$set": updated_data})
        client.close()
        return redirect(url_for('index'))
    
    # Handle GET request: Fetch the existing invoice data
    invoice = invoices.find_one({"_id": ObjectId(invoice_id)})
    client.close()
    return render_template("edit.html", invoice=invoice)

if __name__ == "__main__":
    app.run(debug=True)
