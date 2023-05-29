from connect_four import ConnectFour


class MinimaxAI:
    def __init__(self, depth, player=1):
        self.depth = depth
        self.player = player

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.is_full() or game.has_won(self.player) or game.has_won(-self.player):
            return self.evaluate_board(game)

        if maximizing_player:
            max_score = float('-inf')
            for move in game.get_legal_moves():
                new_game = game.copy()
                new_game.drop_piece(move, self.player)
                score = self.minimax(new_game, depth - 1, alpha, beta, False)
                max_score = max(max_score, score)
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = float('inf')
            for move in game.get_legal_moves():
                new_game = game.copy()
                new_game.drop_piece(move, -self.player)
                score = self.minimax(new_game, depth - 1, alpha, beta, True)
                min_score = min(min_score, score)
                beta = min(beta, min_score)
                if beta <= alpha:
                    break
            return min_score

    def find_best_move(self, game):
        best_score = float('-inf')
        best_move = -1

        moves = [-1000000 for _ in range(game.columns)]

        for move in game.get_legal_moves():
            new_game = game.copy()
            new_game.drop_piece(move, self.player)
            score = self.minimax(new_game, self.depth - 1, float('-inf'), float('inf'), False)
            moves[move] = score
            if score > best_score:
                best_score = score
                best_move = move

        return best_move + 1

    def evaluate_board(self, game):
        if game.has_won(self.player):
            return 100
        elif game.has_won(-self.player):
            return -100
        else:
            return self.heuristic(game)

    def heuristic(self, game):
        score = 0
        for row in range(game.rows):
            for col in range(game.columns):
                if game.board[row][col] == self.player:
                    score += self.count_potential_wins(game, row, col, self.player)
                elif game.board[row][col] == -self.player:
                    score -= self.count_potential_wins(game, row, col, -self.player)
        return score

    def count_potential_wins(self, game, row, col, player):
        count = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            potential_win = True
            for i in range(4):
                r, c = row + dr * i, col + dc * i
                if not (0 <= r < game.rows and 0 <= c < game.columns) or game.board[r][c] == -player:
                    potential_win = False
                    break
            if potential_win:
                count += 1
        return count
