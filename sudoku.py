def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if board[i][j] == 0:
                print(".", end=" ")
            else:
                print(board[i][j], end=" ")
        print()


def is_valid(board, row, col, num):
    # Check row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False

    return True


def sudoku_game():
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    while True:
        print_board(board)
        try:
            row = int(input("Enter row (0-8): "))
            col = int(input("Enter column (0-8): "))
            num = int(input("Enter number (1-9): "))
        except ValueError:
            print("Invalid input. Use numbers.")
            continue

        if 0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9:
            if board[row][col] == 0:
                if is_valid(board, row, col, num):
                    board[row][col] = num
                else:
                    print("Invalid move. Try again.")
            else:
                print("Cell is already filled.")
        else:
            print("Input out of range.")

        if all(all(cell != 0 for cell in row) for row in board):
            print("Congratulations! You've completed the Sudoku.")
            print_board(board)
            break

from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

# Simple HTML template to simulate Sudoku interface
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
    resp = make_response(render_template_string(TEMPLATE))

    resp.set_cookie("sudoku_session", "fake-session-id-12345")

    return resp

if __name__ == "__main__":
    sudoku_game()