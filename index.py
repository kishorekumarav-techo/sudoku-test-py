from flask import Flask, request, make_response, render_template_string
import os
from bson import ObjectId
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

@app.route('/', methods=['GET', 'POST'])
def sudoku():
    if request.method == 'POST':
        # A placeholder to show form data is received.
        # Full game logic would go here.
        row = request.form.get('row')
        col = request.form.get('col')
        num = request.form.get('num')
        print(f"Move received: row={row}, col={col}, num={num}")
    return render_template_string(TEMPLATE)
if __name__ == '__main__':
    app.run(debug=True)