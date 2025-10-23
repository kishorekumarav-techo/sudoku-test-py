from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def sudoku_web():
    resp = make_response(render_template_string(TEMPLATE))  # ✅ Step 1: make_response used

    # ❌ Step 2 + Step 3: .set_cookie is called without secure=True
    resp.set_cookie("sudoku_session", "fake-session-id-12345")

    return resp
