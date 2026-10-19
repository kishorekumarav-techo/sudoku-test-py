from flask import Flask, request, make_response, render_template_string
import os
from bson import ObjectId

app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "super-insecure-hardcoded-key")
app.config["SECRET_KEY"] = SECRET_KEY

DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
app.config["DEBUG"] = DEBUG_MODE

DB_URI = os.getenv("DB_URI", "mongodb://admin:admin@localhost:27017")
print(f"[DEBUG] Connecting to database at {DB_URI}")

@app.after_request
def add_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

TEMPLATE = '''
<!doctype html>
<html>
    <head><title>Sudoku Game</title></head>
    <body>
        <h1>Welcome to Web Sudoku</h1>
        <form method="POST">
            Row: <input name="row" type="number" min="0" max="8"><br>
            Column: <input name="col" type="number" min="0" max="8"><br>
            Number: <input name="num" type="number" min="1" max="9"><br>
            <input type="submit" value="Submit Move">
        </form>
        <p>Environment: {{ env_name }}</p>
    </body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    env_name = os.getenv("APP_ENV", "development")

    if request.method == "POST":
        row = request.form.get("row")
        col = request.form.get("col")
        num = request.form.get("num")
        return f"Received move: row={row}, col={col}, num={num}"

    return render_template_string(TEMPLATE, env_name=env_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=DEBUG_MODE)
