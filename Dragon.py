import copy
import time

TIME_LIMIT = 15

class Dragon:

    def __init__(self):
        self.board = [[' ']*8 for i in range(8)]
        self.size = 8
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'
        self.board[3][3] = 'W'
        self.board[4][3] = 'B'
        # a list of unit vectors (row, col)
        self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]
        self.score = 0
        self.level = 4
        self.time = 0
        self.corner = ()
        self.origin_board = []

    #prints the boards
    def PrintBoard(self):

        # Print column numbers
        print("  ",end='')
        for i in range(self.size):
            print(i+1,end=" ")
        print()

        # Build horizontal separator
        linestr = " " + ("+-" * self.size) + "+"

        # Print board
        for i in range(self.size):
            print(linestr)                     # Separator
            print(i+1,end="|")                 # Row number
            for j in range(self.size):
                print(self.board[i][j],end="|")  # board[i][j] and pipe separator
            print()                           # End line
        print(linestr)

    #checks every direction fromt the position which is input via "col" and "row", to see if there is an opponent piece
    #in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
    #a chain of opponent pieces in that direction, which ends with one of the players pieces.
    def islegal(self, row, col, player, opp):
        if(self.get_square(row,col)!=" "):
            return False
        for Dir in self.directions:
            for i in range(self.size):
                if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
                    #does the adjacent square in direction dir belong to the opponent?
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
                        #no pieces will be flipped in this direction, so skip it
                        break
                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                    #of opponent pieces
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
                        break

                    #with one of player's pieces at the other end
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
                        #set a flag so we know that the move was legal
                        return True
        return False
        
    #returns true if the square was played, false if the move is not allowed
    def place_piece(self, row, col, player, opp):
        if(self.get_square(row,col)!=" "):
            return False
        
        if(player == opp):
            print("player and opponent cannot be the same")
            return False
        
        legal = False
        #for each direction, check to see if the move is legal by seeing if the adjacent square
        #in that direction is occuipied by the opponent. If it isnt check the next direction.
        #if it is, check to see if one of the players pieces is on the board beyond the oppponents piece,
        #if the chain of opponents pieces is flanked on both ends by the players pieces, flip
        #the opponents pieces 
        for Dir in self.directions:
            #look across the length of the board to see if the neighboring squares are empty,
            #held by the player, or held by the opponent
            for i in range(self.size):
                if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
                    #does the adjacent square in direction dir belong to the opponent?
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
                        #no pieces will be flipped in this direction, so skip it
                        break
                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                    #of opponent pieces
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
                        break

                    #with one of player's pieces at the other end
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
                        #set a flag so we know that the move was legal
                        legal = True
                        self.flip_tiles(row, col, Dir, i, player)
                        break

        return legal


    # Get a greedy move it exists
    def greedy(playerColor, oppColor):
        return None


    #Places piece of opponent's color at (row,col) and then returns
    #  the best move, determined by the make_move(...) function
    def play_square(self, row, col, playerColor, oppColor, board):
        # Place a piece of the opponent's color at (row,col)
        if (row,col) != (-1, -1):
            self.place_piece(row,col,oppColor,playerColor)

        # Determine best move and and return value to Matchmaker

        self.board = copy.deepcopy(board)
        self.time = time.time()
        self.corner = self.get_corner(playerColor, oppColor)
        self.origin_board = copy.deepcopy(board)

        move = self.greedy(playerColor, oppColor)
        if move is not None:
            move = self.make_move(playerColor, oppColor)

        print(move[0]+1, move[1]+1)
        self.place_piece(move[0], move[1], playerColor, oppColor)

        return move

    #sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
    # (dist) to be a given value ( player )
    def flip_tiles(self, row, col, Dir, dist, player):
        for i in range(dist):
            self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
        return True
    
    #returns the value of a square on the board
    def get_square(self, row, col):
        return self.board[row][col]

    def get_score(self, Color):
        score = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] is Color:
                    score += 1

        return score

    def is_full(self):
        for i in range(self.size):
            for j in range(self.size):
                if(self.board[i][j]==' '):
                    return False
        return True

    def first_step_end(self, playerColor, oppColor):


    def is_end(self, playerColor, oppColor, level):
        if (level > self.level) or self.is_full() or self.no_step(oppColor, playerColor):
            return True
        if time.time() - self.time > TIME_LIMIT:
            return True

        return False


    def no_step(self, playerColor, oppColor):
        for row in range(self.size):
            for col in range(self.size):
                if(self.islegal(row,col,playerColor, oppColor)):
                    return False
        return True

    def get_corner(self, playerColor, oppColor):
        player_corner = 0
        opp_corner = 0

        corner_place = [(0,0), (0,7), (7,0), (7,7)]

        for corner in corner_place:
            if self.get_square(corner[0], corner[1]) is playerColor:
                player_corner += 1
            elif self.get_square(corner[0], corner[1]) is oppColor:
                opp_corner += 1

        return (player_corner, opp_corner)



    def evaluation(self, playerColor, oppColor):
        score = 0
        score = self.get_score(playerColor) - self.score

        if self.no_step(oppColor, playerColor):
            score += 20

        win_corner = self.get_corner()[0] - self.corner[0] + self.corner[1] - self.get_corner()[1]
        score += win_corner * 20



        return score



    #Search the game board for a legal move, and play the first one it finds
    def make_move(self, playerColor, oppColor):
        value = None
        max  = None
        move = ()
        self.score = self.get_score(playerColor)
        level = 0

        for row in range(self.size):
            for col in range(self.size):
                if(self.islegal(row,col,playerColor, oppColor)):
                    tmp_board = copy.deepcopy(self.board)
                    self.place_piece(row, col, playerColor, oppColor)
                    if self.is_end(playerColor, oppColor, ):
                        value = self.evaluation(playerColor, oppColor)
                        if time.time() - self.time > TIME_LIMIT:
                            break
                    else:
                        value = self.min_value(oppColor, playerColor, value, level + 1)

                    if (max == None) or (max < value):
                        max = value
                        move = (row, col)

                    self.board = tmp_board

        return move if (value is not None) else (-1, -1)

    def min_value(self, playerColor, oppColor, alpha, level):
        min = None
        value = None

        for row in range(self.size):
            for col in range(self.size):
                if (self.islegal(row,col,playerColor, oppColor)):
                    tmp_board = copy.deepcopy(self.board)
                    self.place_piece(row, col, playerColor, oppColor)

                    if self.is_end(playerColor, oppColor, level):
                        value = self.evaluation(playerColor, oppColor)
                        if time.time() - self.time > TIME_LIMIT:
                            if min is None:
                                min = value
                            break
                    else:
                        value = self.max_value(oppColor, playerColor, value, level + 1)

                    if alpha != None and value <= alpha:
                        self.board = tmp_board
                        return alpha - 1
                    if (min is None) or (min > value):
                        min = value
                    self.board = tmp_board
        return min

    def max_value(self, playerColor, oppColor, beta, level):
        max = None
        value = None

        for row in range(self.size):
            for col in range(self.size):
                if (self.islegal(row,col,playerColor, oppColor)):
                    tmp_board = copy.deepcopy(self.board)
                    self.place_piece(row, col, playerColor, oppColor)

                    if self.is_end(playerColor, oppColor, level):
                        value = self.evaluation(playerColor, oppColor)
                        if time.time() - self.time > TIME_LIMIT:
                            if max is None:
                                max = value
                            break
                    else:
                        value = self.min_value(oppColor, playerColor, value, level + 1)

                    if (beta is not None) and value >= beta:
                        self.board = tmp_board
                        return beta + 1
                    if (max is None) or (max < value):
                        max = value
                    self.board = tmp_board
        return max



