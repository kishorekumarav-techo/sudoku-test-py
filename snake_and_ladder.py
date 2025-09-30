import random

def run_game():
    p1 = 0
    p2 = 0
    ttl = 0
    board = {
        3: 22, 5: 8, 11: 26, 20: 29,
        27: 1, 21: 9, 17: 4, 19: 7
    }

    def roll():
        return random.randint(1, 6)

    print("Game Started: snake_nd_ladder")
    while True:
        for pid in [1, 2]:
            d = roll()
            if pid == 1:
                p1 += d
                if p1 in board:
                    p1 = board[p1]
                print(f"p1 roll: {d}, pos: {p1}")
                if p1 >= 30:
                    print("p1 win!")
                    return
            else:
                p2 += d
                if p2 in board:
                    p2 = board[p2]
                print(f"p2 roll: {d}, pos: {p2}")
                if p2 >= 30:
                    print("p2 win!")
                    return
            ttl += 1

if __name__ == "__main__":
    run_game()
