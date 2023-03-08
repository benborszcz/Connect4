
import random
import numpy as np
import copy

class Board:
    tiles = [[0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0]]
    
    def toString(self):
        ret = ""
        count = 0
        ret = ret + "  1   2   3   4   5   6   7  "
        ret = ret + "\n-----------------------------\n"
        for i in range(6):
            ret = ret + "|"
            for j in range(7):
                add = "   "
                if self.tiles[i][j] == 1:
                    add = " O "
                elif self.tiles[i][j] == -1:
                    add = " X "
                ret = ret + add
                ret = ret + "|"
                count+=1
            ret = ret + "\n-----------------------------\n"
        return ret

    def check_for_win(self, key):
        #horizontalCheck 
        for j in range(len(self.tiles[0])-3):
            for i in range(len(self.tiles)):
                if self.tiles[i][j] == key and self.tiles[i][j+1] == key and self.tiles[i][j+2] == key and self.tiles[i][j+3] == key:
                    return True
                          
        #verticalCheck    
        for i in range(len(self.tiles)-3):
            for j in range(len(self.tiles[0])):
                if self.tiles[i][j] == key and self.tiles[i+1][j] == key and self.tiles[i+2][j] == key and self.tiles[i+3][j] == key:
                    return True

        #ascendingDiagonalCheck
        for j in range(len(self.tiles[0])-3):
            for i in range(3, len(self.tiles)):
                if self.tiles[i][j] == key and self.tiles[i-1][j+1] == key and self.tiles[i-2][j+2] == key and self.tiles[i-3][j+3] == key:
                    return True
        
        #descendingDiagonalCheck
        for j in range(3,len(self.tiles[0])):
            for i in range(3, len(self.tiles)):
                if self.tiles[i][j] == key and self.tiles[i-1][j-1] == key and self.tiles[i-2][j-2] == key and self.tiles[i-3][j-3] == key:
                    return True

        return False
    
    def check_for_3(self, key):
        #horizontalCheck 
        for j in range(len(self.tiles[0])-2):
            for i in range(len(self.tiles)):
                if self.tiles[i][j] == key and self.tiles[i][j+1] == key and self.tiles[i][j+2] == key:
                    return True
                          
        #verticalCheck    
        for i in range(len(self.tiles)-2):
            for j in range(len(self.tiles[0])):
                if self.tiles[i][j] == key and self.tiles[i+1][j] == key and self.tiles[i+2][j] == key:
                    return True

        #ascendingDiagonalCheck
        for j in range(len(self.tiles[0])-2):
            for i in range(2, len(self.tiles)):
                if self.tiles[i][j] == key and self.tiles[i-1][j+1] == key and self.tiles[i-2][j+2] == key:
                    return True
        
        #descendingDiagonalCheck
        for j in range(2,len(self.tiles[0])):
            for i in range(2, len(self.tiles)):
                if self.tiles[i][j] == key and self.tiles[i-1][j-1] == key and self.tiles[i-2][j-2] == key:
                    return True

        return False     

    def is_move_left(self):
        for i in range(7):
            if self.tiles[0][i] == 0:
                return True
        return False

    def drop_piece(self, loc, key):
        i = 0
        while self.tiles[i][loc] == 0:
            if i!=0:
                self.tiles[i-1][loc] = 0
            self.tiles[i][loc] = key
            i+=1
            if i == 6:
                break

    def remove_piece(self, loc):
        i = 0
        while self.tiles[i][loc] == 0:
            i+=1
        self.tiles[i][loc] = 0
            

class MinimaxPlayer:
    def __init__(self, key):
        self.key = key
        self.rows = 6
        self.cols = 7
        self.depth = 7
    
    def move(self, board):
        pos_values = [-1000000, -1000000, -1000000, -1000000, -1000000, -1000000, -1000000]
        alpha = -1000000
        beta = 1000000
        for i in range(self.cols):
            if board.tiles[0][i] == 0:
                board.drop_piece(i, self.key)
                value = self.minimax(board, self.depth-1, alpha, beta, False)+self.depth
                pos_values[i] = value
                board.remove_piece(i)

        print(pos_values)
        
        positions = [0]
        for i, val in enumerate(pos_values):
            if i == 0: continue
            if val > pos_values[positions[0]]:
                positions = [i]
            elif val == pos_values[positions[0]]:
                positions.append(i)

        print(positions)
        board.drop_piece(random.choice(positions), self.key)
        
    def minimax(self, board, depth, alpha, beta, isMaximizingPlayer):
        #initial checks
        if board.check_for_win(self.key):
            return 10000
        if board.check_for_win(-self.key):
            return -10000
        if depth == 0 or not board.is_move_left():
            return 0

        if isMaximizingPlayer:
            best_val = -1000000
            for i in range(self.cols):
                if board.tiles[0][i] == 0:
                    board.drop_piece(i, self.key)
                    value = self.minimax(board, depth-1, alpha, beta, False)+depth
                    best_val = max(best_val, value)
                    board.remove_piece(i)
                    alpha = max(alpha, best_val)
                if beta <= alpha:
                    break

        else:
            best_val = 1000000
            for i in range(self.cols):
                if board.tiles[0][i] == 0:
                    board.drop_piece(i, -self.key)
                    value = self.minimax(board, depth-1, alpha, beta, True)-depth
                    best_val = min(best_val, value)
                    board.remove_piece(i)
                    beta = min(beta, best_val)
                if beta <= alpha:
                    break
        
        return best_val


class HumanPlayer:
    def __init__(self, key):
        self.key = key
    def move(self, board):
        while True:
            move = int(input("Enter Move (1-7): "))
            if board.tiles[0][move-1] == 0:
                board.drop_piece(move-1, self.key)
                break


p1 = MinimaxPlayer(1)
p2 = HumanPlayer(-1)
board = Board()
print(board.toString())
while True:
    p1.move(board)
    win = board.check_for_win(1)
    print(board.toString())
    if win:
        print(1)
        break
    p2.move(board)
    win = board.check_for_win(-1)
    print(board.toString())
    if win:
        print(2)
        break


