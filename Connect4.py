import sys

class ConnectFour:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = [[0] * columns for _ in range(rows)]

    def drop_piece(self, column, player):
        for row in reversed(self.board):
            if row[column] == 0:
                row[column] = player
                return True
        return False

    def is_full(self):
        return all(cell != 0 for row in self.board for cell in row)

    def has_won(self, player):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.check_for_win(row, col, player):
                    return True
        return False

    def check_for_win(self, row, col, player):
        if col <= self.columns - 4:
            if all(self.board[row][col + i] == player for i in range(4)):
                return True
        if row <= self.rows - 4:
            if all(self.board[row + i][col] == player for i in range(4)):
                return True
        if col <= self.columns - 4 and row <= self.rows - 4:
            if all(self.board[row + i][col + i] == player for i in range(4)):
                return True
        if col >= 3 and row <= self.rows - 4:
            if all(self.board[row + i][col - i] == player for i in range(4)):
                return True
        return False

    def get_legal_moves(self):
        return [col for col in range(self.columns) if self.board[0][col] == 0]

    def copy(self):
        new_game = ConnectFour(self.rows, self.columns)
        new_game.board = [row.copy() for row in self.board]
        return new_game


class MinimaxAI:
    def __init__(self, depth, player=1):
        self.depth = depth
        self.player = player

    def minimax(self, game, depth, maximizing_player):
        if depth == 0 or game.is_full() or game.has_won(self.player) or game.has_won(-self.player):
            return self.evaluate_board(game)

        if maximizing_player:
            max_score = float('-inf')
            for move in game.get_legal_moves():
                new_game = game.copy()
                new_game.drop_piece(move, self.player)
                score = self.minimax(new_game, depth - 1, False)
                max_score = max(max_score, score)
            return max_score
        else:
            min_score = float('inf')
            for move in game.get_legal_moves():
                new_game = game.copy()
                new_game.drop_piece(move, -self.player)
                score = self.minimax(new_game, depth - 1, True)
                min_score = min(min_score, score)
            return min_score

    def find_best_move(self, game):
        best_score = float('-inf')
        best_move = -1

        moves = [-1000000 for _ in range(game.columns)]

        for move in game.get_legal_moves():
            new_game = game.copy()
            new_game.drop_piece(move, self.player)
            score = self.minimax(new_game, self.depth - 1, False)
            moves[move] = score
            if score > best_score:
                best_score = score
                best_move = move

        print(moves)

        return best_move + 1

    def evaluate_board(self, game):
        if game.has_won(self.player):
            return 100
        elif game.has_won(-self.player):
            return -100
        else:
            return 0




#-----------------------------------------------------------

game = ConnectFour()


def print_board(board):
    print(" " + "   ".join(str(i+1) for i in range(game.columns)))
    print("-" * (game.columns * 4 - 1))
    for row in board:
        row_str = "|".join(" X " if cell == 1 else " O " if cell == -1 else "   " for cell in row)
        print(row_str)
        print("-" * (game.columns * 4 - 1))


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
