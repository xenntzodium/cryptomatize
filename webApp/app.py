from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from ecdsa import SigningKey, NIST256p
import hashlib
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
KEY_FOLDER = 'keys'

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, KEY_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def generate_keys():
    private_key = SigningKey.generate(curve=NIST256p)
    public_key = private_key.verifying_key

    with open(os.path.join(KEY_FOLDER, "private.pem"), "wb") as f:
        f.write(private_key.to_pem())
    with open(os.path.join(KEY_FOLDER, "public.pem"), "wb") as f:
        f.write(public_key.to_pem())

    return private_key, public_key

def sign_file(input_path, private_key):
    with open(input_path, "rb") as f:
        data = f.read()

    signature = private_key.sign(data, hashfunc=hashlib.sha256)
    output_path = os.path.join(OUTPUT_FOLDER, os.path.basename(input_path) + ".enc")

    with open(output_path, "wb") as f:
        f.write(signature + data)

    return output_path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "Dosya bulunamadı"

    file = request.files['file']
    if file.filename == "":
        return "Dosya seçilmedi"

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    private_key, _ = generate_keys()
    output_path = sign_file(input_path, private_key)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
