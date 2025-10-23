from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)
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
    </body>
</html>
'''
@app.route("/", methods=["GET", "POST"])
def sudoku_web():
    resp = make_response(render_template_string(TEMPLATE))  # ✅ Step 1: make_response used

    # ❌ Step 2 + Step 3: .set_cookie is called without secure=True
    resp.set_cookie("sudoku_session", "fake-session-id-12345")

    return resp
