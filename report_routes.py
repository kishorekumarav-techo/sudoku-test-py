
from flask import Flask, jsonify, request, abort
import jwt
import secrets
import os
from datetime import datetime, timedelta, timezone
from functools import wraps

app = Flask(__name__)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY"
)

if not app.config["JWT_SECRET_KEY"]:
    raise RuntimeError("JWT_SECRET_KEY environment variable is required")

JWT_ALGORITHM = "HS256"

reports_db = {}

# Demo credentials (replace with a real user database)
USERNAME = "admin"
PASSWORD = "admin123"


# Generate JWT Token
def generate_jwt_token(username):
    payload = {
        "sub": username,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        app.config["JWT_SECRET_KEY"],
        algorithm=JWT_ALGORITHM
    )

    return token


# JWT Authentication Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            # Expected format: Bearer <token>
            token = token.split(" ", 1)

            if len(token) != 2 or token[0].lower() != "bearer":
                raise jwt.InvalidTokenError("Invalid authorization format")

            decoded_token = jwt.decode(
                token[1],
                app.config["JWT_SECRET_KEY"],
                algorithms=[JWT_ALGORITHM]
            )

            request.current_user = decoded_token["sub"]

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401

        except (jwt.InvalidTokenError, KeyError):
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


# LOGIN ENDPOINT
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if username == USERNAME and password == PASSWORD:

        token = generate_jwt_token(username)

        return jsonify({
            "message": "Login successful",
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": 3600
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401


# NEW PROTECTED ENDPOINT
@app.route('/protected', methods=['GET'])
@token_required
def protected():

    return jsonify({
        "message": "You have accessed a protected endpoint",
        "user": request.current_user
    }), 200


# CREATE REPORT
@app.route('/reports', methods=['POST'])
@token_required
def create_report():

    data = request.get_json(silent=True)

    if not data or not data.get("file_name"):
        abort(400, description="file_name is required")

    report_id = max(reports_db.keys(), default=0) + 1

    reports_db[report_id] = {
        "id": report_id,
        "file_name": data.get("file_name"),
        "status": data.get("status", "pending"),
        "summary": data.get("summary", "")
    }

    return jsonify({
        "message": "Report created successfully",
        "report": reports_db[report_id]
    }), 201


# GET ALL REPORTS
@app.route('/reports', methods=['GET'])
@token_required
def get_all_reports():

    return jsonify(list(reports_db.values())), 200


# GET SINGLE REPORT
@app.route('/reports/<int:report_id>', methods=['GET'])
@token_required
def get_report(report_id):

    report = reports_db.get(report_id)

    if not report:
        abort(404, description="Report not found")

    return jsonify(report), 200


# UPDATE REPORT
@app.route('/reports/<int:report_id>', methods=['PUT'])
@token_required
def update_report(report_id):

    report = reports_db.get(report_id)

    if not report:
        abort(404, description="Report not found")

    data = request.get_json(silent=True)

    if not data:
        abort(400, description="Invalid JSON payload")

    report["file_name"] = data.get("file_name", report["file_name"])
    report["status"] = data.get("status", report["status"])
    report["summary"] = data.get("summary", report["summary"])

    return jsonify({
        "message": "Report updated successfully",
        "report": report
    }), 200


# DELETE REPORT
@app.route('/reports/<int:report_id>', methods=['DELETE'])
@token_required
def delete_report(report_id):

    if report_id not in reports_db:
        abort(404, description="Report not found")

    del reports_db[report_id]

    return jsonify({
        "message": f"Report {report_id} deleted successfully"
    }), 200


# DELETE REPORT V2
@app.route('/reports/v2/<int:report_id>', methods=['DELETE'])
@token_required
def delete_report_v2(report_id):

    if report_id not in reports_db:
        abort(404, description="Report not found")

    del reports_db[report_id]

    return jsonify({
        "message": f"Report {report_id} deleted successfully"
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
