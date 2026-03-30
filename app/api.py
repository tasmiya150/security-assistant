from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
from password_checker import check_strength, generate_password
from database import init_db, save_check, get_recent_checks

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    password = data.get("password", "")
    if not password:
        return jsonify({"error": "Password required"}), 400

    result = check_strength(password)
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    save_check(hashed, result["strength"], result["score"])
    return jsonify(result)

@app.route("/generate", methods=["GET"])
def generate():
    length = int(request.args.get("length", 12))
    return jsonify({"password": generate_password(length)})

@app.route("/history", methods=["GET"])
def history():
    return jsonify(get_recent_checks())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)   