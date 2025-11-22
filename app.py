from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    port=int(os.getenv("DB_PORT")),   # <-- ADD THIS
    database=os.getenv("DB_NAME")
)


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()  # use JSON instead of form

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    service = data.get("service")

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO leads (name, email, phone, service) VALUES (%s, %s, %s, %s)",
            (name, email, phone, service)
        )
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"status": "success", "message": "Lead stored!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Bare7 backend running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
