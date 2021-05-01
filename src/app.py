import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, jsonify, render_template, send_file
from flask.globals import request
from src.receipt import generate_receipt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        return jsonify("Press Button For API")
    else:
        return render_template("index.html")

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == "POST":
        receipt_data = request.json
        file_byte_stream = generate_receipt(receipt_data)
        return send_file(file_byte_stream, as_attachment=True, attachment_filename="receipt.pdf", mimetype="application/pdf")
    else:
        return jsonify("Wrong request method")

if __name__ == "__main__":
    app.run()