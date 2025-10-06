import random

def run_game():
    player1_position = 0
    player2_position = 0
    total_turns = 0

    # Ladders move you forward, snakes move you back
    snakes_and_ladders = {
        3: 22, 5: 8, 11: 26, 20: 29,  # Ladders
        27: 1, 21: 9, 17: 4, 19: 7   # Snakes
    }

    def roll_dice():
        return random.randint(1, 6)

    print("Game Started: Snakes and Ladders")

    while True:
        for player_id in [1, 2]:
            dice_roll = roll_dice()

            if player_id == 1:
                player1_position += dice_roll
                player1_position = snakes_and_ladders.get(player1_position, player1_position)
                print(f"Player 1 rolled: {dice_roll}, new position: {player1_position}")

                if player1_position >= 30:
                    print("Player 1 wins!")
                    return

            else:
                player2_position += dice_roll
                player2_position = snakes_and_ladders.get(player2_position, player2_position)
                print(f"Player 2 rolled: {dice_roll}, new position: {player2_position}")

                if player2_position >= 30:
                    print("Player 2 wins!")
                    return

            total_turns += 1

if __name__ == "__main__":
    run_game()
