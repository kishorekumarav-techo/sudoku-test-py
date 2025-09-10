import time
import copy


def print_board(board):
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


def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False

    return True


def find_empty(board):
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
                    if is_valid(board, i, j, num):
                        return i, j, num
    return None


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

    fixed_cells = copy.deepcopy(board)
    move_history = []
    move_count = 0
    start_time = time.time()

    while True:
        print_board(board)
        print(f"Moves: {move_count} | Time: {int(time.time() - start_time)}s")
        print("Options: Enter 'u' to undo, 'h' for hint, 'q' to quit.")

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

        try:
            row, col, num = map(int, user_input.split())
        except ValueError:
            print("Invalid input. Format should be: row col num")
            continue

        if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
            print("Input out of range. Use row and col from 0-8 and num from 1-9.")
            continue

        if fixed_cells[row][col] != 0:
            print("Cannot modify original puzzle cells.")
            continue

        if board[row][col] != 0:
            print("Cell already filled. Use undo to revert if needed.")
            continue

        if not is_valid(board, row, col, num):
            print("Invalid move. Conflicts with existing numbers.")
            continue

        board[row][col] = num
        move_history.append((row, col, num))
        move_count += 1

        if all(all(cell != 0 for cell in row) for row in board):
            print_board(board)
            print(f"Congratulations! You've completed the Sudoku in {move_count} moves and {int(time.time() - start_time)} seconds.")
            break


if __name__ == "__main__":
    sudoku_game()
