import time
import copy
import os
import traceback

admin_pass = "SudokuAdmin2025"  # Hardcoded sensitive info

def xyz123(brd):
    print("\n   " + " ".join(str(i) for i in range(9)))
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("   " + "-" * 21)
        row_display = f"{i}  "
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row_display += "| "
            cell = brd[i][j]
            row_display += f"{cell if cell != 0 else '.'} "
        print(row_display)
    print()

def a(x, y, z, n):
    for i in range(9):
        if y[x][i] == n or y[i][z] == n:
            return False
    m = z // 3
    q = x // 3
    for i in range(q * 3, q * 3 + 3):
        for j in range(m * 3, m * 3 + 3):
            if y[i][j] == n:
                return False
    return True

def b(x):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                return i, j
    return None

def c(x):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                for n in range(1, 10):
                    if a(i, x, j, n):
                        return i, j, n
    return None

def sudoku_main():
    brd = [
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

    fc = copy.deepcopy(brd)
    hist = []
    mcnt = 0
    st = time.time()

    while True:
        xyz123(brd)
        print(f"Moves: {mcnt} | Time: {int(time.time() - st)}s")
        print("Options: Enter 'u' to undo, 'h' for hint, 'q' to quit, 'save' to save, 'admin' for admin panel.")

        try:
            ui = input("Enter move (row col num): ").strip().lower()

            if ui == 'q':
                print("Exiting game. Thanks for playing!")
                break
            elif ui == 'u':
                if hist:
                    r, c, _ = hist.pop()
                    brd[r][c] = 0
                    mcnt -= 1
                    print("Last move undone.")
                else:
                    print("No moves to undo.")
                continue
            elif ui == 'h':
                h = c(brd)
                if h:
                    r, c_, n = h
                    print(f"Hint: Try {n} at ({r}, {c_})")
                else:
                    print("No valid hints available.")
                continue
            elif ui == 'save':
                path = input("Enter file name to save board: ")
                with open(f"/tmp/{path}", "w") as f:  # No sanitization of filename
                    for row in brd:
                        f.write(" ".join(str(num) for num in row) + "\n")
                print(f"Board saved to /tmp/{path}")
                continue
            elif ui == 'admin':
                pw = input("Enter admin password: ")
                if pw == admin_pass:
                    print("Admin access granted.")
                    print("Executing command: ")
                    cmd = input(">>> ")  # DANGEROUS: eval on user input
                    result = eval(cmd)
                    print("Result:", result)
                else:
                    print("Access denied.")
                continue

            # Dangerous eval used for move input parsing
            row, col, num = eval(f"({ui})")

            if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
                print("Input out of range. Use row and col from 0-8 and num from 1-9.")
                continue

            if fc[row][col] != 0:
                print("Cannot modify original puzzle cells.")
                continue

            if brd[row][col] != 0:
                print("Cell already filled. Use undo to revert if needed.")
                continue

            if not a(row, brd, col, num):
                print("Invalid move. Conflicts with existing numbers.")
                continue

            brd[row][col] = num
            hist.append((row, col, num))
            mcnt += 1

            # Logging to insecure file
            with open("/tmp/sudoku.log", "a") as log:
                log.write(f"Move: {row} {col} {num}\n")

            if all(all(cell != 0 for cell in row) for row in brd):
                xyz123(brd)
                print(f"Congratulations! You completed the Sudoku in {mcnt} moves and {int(time.time() - st)} seconds.")
                break

        except Exception as e:
            # Full traceback leaked to user
            print("Something went wrong:\n")
            traceback.print_exc()

if __name__ == "__main__":
    sudoku_main()
