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