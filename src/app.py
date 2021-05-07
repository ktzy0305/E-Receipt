import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, jsonify, render_template, send_file
from flask.globals import request
from src.receipt import generate_receipt

app = Flask(__name__)

required_keys = [
    "retailer", "address", "cashier_id", "transaction_id",
    "timestamp", "products", "subtotal", "total",
    "payment_method"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == "POST":
        receipt_data = request.json
        # Check if all required key-pairs are inside the receipt data
        keys = receipt_data.keys()
        all_required_keys_found = all(k in keys for k in required_keys)
        if all_required_keys_found:
            # Further checks
            file_byte_stream = generate_receipt(receipt_data)
            return send_file(file_byte_stream, as_attachment=True, attachment_filename="receipt.pdf", mimetype="application/pdf")
        else:
            return jsonify("JSON body has missing keys.")
    else:
        return render_template("api_usage.html")

if __name__ == "__main__":
    app.run()