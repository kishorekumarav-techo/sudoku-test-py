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