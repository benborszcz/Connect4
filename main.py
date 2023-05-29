from connect_four import ConnectFour
from minimax_ai import MinimaxAI


def print_board(board):
    print(" " + "   ".join(str(i+1) for i in range(game.columns)))
    print("-" * (game.columns * 4 - 1))
    for row in board:
        row_str = "|".join(" X " if cell == 1 else " O " if cell == -1 else "   " for cell in row)
        print(row_str)
        print("-" * (game.columns * 4 - 1))


game = ConnectFour()

current_player = 1
human_player = 1
ai_player = -1
minimax_ai = MinimaxAI(depth=4, player=ai_player)

print("Welcome to Connect Four!")
print_board(game.board)

while not game.is_full():
    try:
        column = -1
        if current_player == human_player:
            column = int(input(f"Player {current_player}, choose a column to drop your piece (1-{game.columns}): "))
        else:
            column = minimax_ai.find_best_move(game)

        if column < 1 or column > game.columns:
            print("Invalid column, please choose a column between 1 and", game.columns)
            continue

        if not game.drop_piece(column-1, current_player):
            print("This column is full, please choose another one.")
            continue

        print_board(game.board)

        if game.has_won(current_player):
            print(f"Congratulations, Player {current_player} has won!")
            break

        current_player *= -1

    except ValueError:
        print("Invalid input, please enter a number between 1 and", game.columns)
else:
    print("It's a draw!")