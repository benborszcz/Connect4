
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
                    add = " 0 "
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
    def move(self, board):
        bestMove = None
        bestVal = -100000
        count = 0
        for i in range(7):
            if board.tiles[0][i] == 0:
                board.drop_piece(i, self.key)
                value = self.minimax(board, 0, False, -10000, 10000)
                print("DEBUG @move: "+str(value)+" loc: "+str(count+1))
                if bestVal < value:
                    bestMove = count
                    bestVal = value
                board.remove_piece(i)
            count+=1
        board.drop_piece(bestMove, self.key)
        
    def minimax(self, board, depth, isMaximizingPlayer, alpha, beta):
        if board.check_for_win(1):
            ret = 100*self.key
            if ret < 0:
                ret+=depth
            else:
                ret-=depth
            return ret
        if board.check_for_win(-1):
            ret = -100*self.key
            if ret < 0:
                ret+=depth
            else:
                ret-=depth
            return ret
        if depth > 4 and False:
            ret = 0
            if board.check_for_3(1):
                ret+=(30)*self.key
            if board.check_for_3(-1):
                ret+=(-30)*self.key
            return ret
        if board.is_move_left() == False or depth > 6:
            return 0;
        if isMaximizingPlayer:
            bestVal = -100000
            count = 0
            for i in range(7):
                if board.tiles[0][i] == 0:
                    board.drop_piece(i, self.key)
                    value = self.minimax(board, depth+1, False, alpha, beta)
                    bestVal = max(bestVal, value)
                    board.remove_piece(i)

                    if bestVal >= beta:
                        return bestVal

                    if bestVal > alpha:
                        alpha = bestVal
                count+=1
            return bestVal
        else:
            bestVal = 100000
            count = 0
            for i in range(7):
                if board.tiles[0][i] == 0:
                    board.drop_piece(i, self.key*-1)
                    value = self.minimax(board, depth+1, True, alpha, beta)
                    bestVal = min(bestVal, value)
                    board.remove_piece(i)

                    if bestVal <= alpha:
                        return bestVal

                    if bestVal < beta:
                        beta = bestVal


                count+=1
            return bestVal


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


