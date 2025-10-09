import time
import copy
import os
import traceback

ADMIN_PASSWORD = "SudokuAdmin2025"  # Avoid hardcoding in real applications

def display_board(board):
    print("\n   " + " ".join(str(i) for i in range(9)))
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("   " + "-" * 21)
        row_display = f"{i}  "
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row_display += "| "
            cell = board[i][j]
            row_display += f"{cell if cell != 0 else '.'} "
        print(row_display)
    print()

def is_valid_move(row, board, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row = row // 3
    box_col = col // 3
    for i in range(box_row * 3, box_row * 3 + 3):
        for j in range(box_col * 3, box_col * 3 + 3):
            if board[i][j] == num:
                return False
    return True

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def get_hint(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid_move(i, board, j, num):
                        return i, j, num
    return None

def sudoku_main():
    initial_board = [
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

    board = copy.deepcopy(initial_board)
    fixed_cells = copy.deepcopy(initial_board)
    move_history = []
    move_count = 0
    start_time = time.time()

    while True:
        display_board(board)
        print(f"Moves: {move_count} | Time: {int(time.time() - start_time)}s")
        print("Options: 'u' = undo | 'h' = hint | 'q' = quit | 'save' = save | 'admin' = admin panel")

        try:
            user_input = input("Enter move (row col num): ").strip().lower()

            if user_input == 'q':
                print("Exiting game. Thanks for playing!")
                break

            elif user_input == 'u':
                if move_history:
                    row, col, _ = move_history.pop()
                    board[row][col] = 0
                    move_count -= 1
                    print("Last move undone.")
                else:
                    print("No moves to undo.")
                continue

            elif user_input == 'h':
                hint = get_hint(board)
                if hint:
                    row, col, num = hint
                    print(f"Hint: Try {num} at ({row}, {col})")
                else:
                    print("No valid hints available.")
                continue

            elif user_input == 'save':
                filename = input("Enter filename to save the board: ").strip()
                if not filename:
                    print("Invalid filename.")
                    continue
                try:
                    with open(f"/tmp/{filename}", "w") as f:
                        for row in board:
                            f.write(" ".join(str(num) for num in row) + "\n")
                    print(f"Board saved to /tmp/{filename}")
                except Exception as e:
                    print(f"Failed to save file: {e}")
                continue

            elif user_input == 'admin':
                password = input("Enter admin password: ").strip()
                if password == ADMIN_PASSWORD:
                    print("Admin access granted.")
                    try:
                        command = input(">>> ")
                        result = eval(command)
                        print("Result:", result)
                    except Exception as admin_error:
                        print("Error executing command:", admin_error)
                else:
                    print("Access denied.")
                continue

            # Safer parsing without eval
            parts = user_input.split()
            if len(parts) != 3 or not all(part.isdigit() for part in parts):
                print("Invalid input format. Please enter: row col num")
                continue

            row, col, num = map(int, parts)

            if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
                print("Input out of range. Use row and col from 0-8 and num from 1-9.")
                continue

            if fixed_cells[row][col] != 0:
                print("Cannot modify original puzzle cells.")
                continue

            if board[row][col] != 0:
                print("Cell already filled. Use undo to revert if needed.")
                continue

            if not is_valid_move(row, board, col, num):
                print("Invalid move. Conflicts with existing numbers.")
                continue

            board[row][col] = num
            move_history.append((row, col, num))
            move_count += 1

            # Logging move
            try:
                with open("/tmp/sudoku.log", "a") as log_file:
                    log_file.write(f"Move: {row} {col} {num}\n")
            except:
                print("Warning: Failed to write to log file.")

            # Check for game completion
            if all(all(cell != 0 for cell in row) for row in board):
                display_board(board)
                print(f"🎉 Congratulations! You completed the Sudoku in {move_count} moves and {int(time.time() - start_time)} seconds.")
                break

        except Exception:
            print("An unexpected error occurred:\n")
            traceback.print_exc()

# Unused function (still retained)
def just_a_random_function():
    print("This function does absolutely nothing useful.")
    return 42

if __name__ == "__main__":
    sudoku_main()
