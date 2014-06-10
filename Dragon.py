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
        self.origin_corner_around_diff = 0
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

    #checks every direction from the position which is input via "col" and "row", to see if there is an opponent piece
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
    def greedy(self, playerColor, oppColor):
        '''
        1. take up corner unconditionally
        2. make opponent no move
        3. irreversible move
        '''
        greedy_move = None
        corner_place = [(0,0), (0,7), (7,0), (7,7)]
        move_num = 0

        # condition 1
        for corner in corner_place:
            if self.get_square(corner[0], corner[1]) is " " and self.islegal(corner[0], corner[1], playerColor, oppColor):
                greedy_move = (corner[0], corner[1])
                move_num = 1

        #condition 2
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]==' ' and self.islegal(i, j, playerColor, oppColor):
                    tmp = copy.deepcopy(self.board)
                    self.place_piece(i, j, playerColor, oppColor)
                    if self.no_step(oppColor, playerColor):
                        if greedy_move is None:
                            greedy_move = (i, j)
                            move_num = 2
                        #if opp has no move and for next step we still can move to a corner
                        else:
                            for corner in corner_place:
                                if self.get_square(corner[0], corner[1]) != " " and self.islegal(corner[0], corner[1], playerColor, oppColor):
                                    greedy_move = (i, j)
                                    move_num = 2
                    self.board = tmp
        #condition 3
        if greedy_move is None:
            edge_len = 8
            for corner in corner_place:
                #traverse four edges for irreversible move
                if self.get_square(corner[0], corner[1]) == playerColor:
                    for pos in range(1, edge_len - 1):
                        if self.get_square(corner[0], abs(corner[1]-pos)) == " ":
                            if self.islegal(corner[0], abs(corner[1]-pos), playerColor, oppColor):
                                greedy_move = (corner[0], abs(corner[1]-pos))
                                move_num = 3
                            break
                    for pos in range(1, edge_len - 1):
                        if self.get_square(abs(corner[0] - pos), corner[1]) == " ":
                            if self.islegal(abs(corner[0] - pos), corner[1], playerColor, oppColor):
                                greedy_move = (abs(corner[0] - pos), corner[1])
                                move_num = 3
                            break
                #traverse the triangle for irreversible move
                if self.get_square(corner[0], corner[1]) == playerColor and greedy_move is None:
                    for pos in range(1, edge_len):
                        broken_line = False
                        for s in range(0, pos):
                            base = (s, pos - s - 1)
                            corner_base = (abs(corner[0] - base[0]), abs(corner[1] - base[1]))
                            if self.get_square(corner_base[0], corner_base[1]) == " ":
                                broken_line = True
                                if self.islegal(corner_base[0], corner_base[1], playerColor, oppColor):
                                    greedy_move = corner_base
                                    move_num = 3
                                break
                        #check backwards
                        if broken_line:
                            for s in range(0, pos):
                                base = (pos - s - 1, s)
                                corner_base = (abs(corner[0] - base[0]), abs(corner[1] - base[1]))
                                if self.get_square(corner_base[0], corner_base[1]) == " ":
                                    if self.islegal(corner_base[0], corner_base[1], playerColor, oppColor):
                                        greedy_move = corner_base
                                        move_num = 3
                                    break
                        if broken_line:
                            break
        print("greedy move using condition: " + str(move_num))
        return greedy_move


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
        self.origin_corner_around_diff = self.get_corner_around_diff(playerColor, oppColor)
        self.origin_board = copy.deepcopy(board)

        move = self.greedy(playerColor, oppColor)

        move_set = []

        if move is None:
            for i in range(1, 20):
                self.level = i
                move = self.make_move(playerColor, oppColor)
                move_set.append(move)
                if time.time() - self.time > TIME_LIMIT:
                    break

            if len(move_set) >= 2:
                last_index = len(move_set) - 2
            else:
                last_index = len(move_set) - 1

            move = move_set[last_index]
            last_index -= 1

            while ( self.bad_move(move, playerColor, oppColor) or (not self.islegal(move[0], move[1], playerColor, oppColor)) ) and (last_index >= 0):
                move = move_set[last_index]
                last_index -= 1
        else:
            print("Greedy taken!!!")

        print(move[0]+1, move[1]+1)
        print("original evaluation: ", self.evaluation(playerColor, oppColor))

        self.place_piece(move[0], move[1], playerColor, oppColor)

        print("current evaluation: ", self.evaluation(playerColor, oppColor))
        return move

    def bad_move(self, move, playerColor, oppColor):
        corner_place = [(0,0), (0,7), (7,0), (7,7)]
        corner_around =[ [(0, 1), (1, 0), (1, 1)], [(0, 6), (1, 6), (1, 7)],
                        [(7, 1), (6, 0), (6, 1)], [(7, 6), (6, 7), (6, 6)] ]

        for i in range(len(corner_place)):
            if self.get_square(corner_place[i][0], corner_place[i][1]) is ' ':
                if move in corner_around[i]:
                    return True
        return False






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

    # input a set like [(1,2), (2,3)], output how many player tile in this set and how many opp tile.
    def get_square_num_from_set(self, square_set, playerColor, oppColor):
        player_count = 0
        opp_count = 0

        for square in square_set:
            if self.get_square(square[0], square[1]) is playerColor:
                player_count += 1
            elif self.get_square(square[0], square[1]) is oppColor:
                opp_count += 1
        return (player_count, opp_count)

    def get_corner_around_diff(self, playerColor, oppColor):
        corner_place = [(0,0), (0,7), (7,0), (7,7)]
        corner_around =[ [(0, 1), (1, 0), (1, 1)], [(0, 6), (1, 6), (1, 7)],
                        [(7, 1), (6, 0), (6, 1)], [(7, 6), (6, 7), (6, 6)] ]

        player_corner_around = 0
        opp_corner_around = 0

        for i in range(len(corner_place)):
            if self.get_square(corner_place[i][0], corner_place[i][1]) is ' ':
                player_corner_around += self.get_square_num_from_set(corner_around[i], playerColor, oppColor)[0]
                opp_corner_around += self.get_square_num_from_set(corner_around[i], playerColor, oppColor)[1]

        return player_corner_around - opp_corner_around

    def evaluation(self, playerColor, oppColor):
        '''
        1. incraese of your piecse
        2. make opp no move 20'
        3. increase of corner 20' * n, lose of corner -20 * n
        4. corner around when corner is not taken diff opp - player
        '''

        corner_set = [(0, 0), (0, 7), (7, 0), (7, 7)]
        corner_around_set1 = [(0, 1), (0, 6), (1, 0), (1, 7), (6, 0), (6, 7), (7, 1), (7, 6)]
        corner_around_set2 = [(1, 1), (1, 6), (6, 1), (6, 6) ]
        second_side_set = [(2, 1), (3, 1), (4, 1), (5, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                           (2, 6), (3, 6), (4, 6), (5, 6), (6 ,2), (6, 3), (6, 4), (6, 5)]
        edge_set = [(0, 2), (0, 3), (0, 4), (0, 5), (7, 2),  (7, 3), (7, 4), (7, 5),
                    (2, 0), (3, 0), (4, 0), (5, 0), (2, 7), (3, 7), (4, 7), (5, 7)]

        inside_set = []
        for i in range (2, 6):
            for j in range (2, 6):
                inside_set.append((i,j))

        score = 0

        if self.no_step(oppColor, playerColor):
            score += 20

        for place in edge_set:
            if self.get_square(place[0], place[1]) is playerColor:
                score += 10
            elif self.get_square(place[0], place[1]) is oppColor:
                score -= 10

        for place in corner_set:
            if self.get_square(place[0], place[1]) is playerColor:
                score += 30
            elif self.get_square(place[0], place[1]) is oppColor:
                score -= 30

        for place in corner_around_set1:
            if self.get_square(place[0], place[1]) is playerColor:
                score -= 20
            elif self.get_square(place[0], place[1]) is oppColor:
                score += 20

        for place in corner_around_set2:
            if self.get_square(place[0], place[1]) is playerColor:
                score -= 25
            elif self.get_square(place[0], place[1]) is oppColor:
                score += 25

        for place in second_side_set:
            if self.get_square(place[0], place[1]) is playerColor:
                score += 5
            elif self.get_square(place[0], place[1]) is oppColor:
                score -= 5

        for place in inside_set:
            if self.get_square(place[0], place[1]) is playerColor:
                score += 1
            elif self.get_square(place[0], place[1]) is oppColor:
                score -= 1
        #
        # score = self.get_score(playerColor) - self.score
        #

        #
        # win_corner = self.get_corner(playerColor, oppColor)[0] - self.corner[0] \
        #              + self.corner[1] - self.get_corner(playerColor, oppColor)[1]
        # score += win_corner * 20
        #
        # caf = self.get_corner_around_diff(playerColor, oppColor) - self.origin_corner_around_diff
        # score -= caf * 10

        return score

    #Search the game board for a legal move, and play the first one it finds
    def make_move(self, playerColor, oppColor):
        value = None
        max  = None
        move = ()
        self.score = self.get_score(playerColor)
        level = 0
        move_back_up = ()
        max_score_back_up = None


        for row in range(self.size):
            for col in range(self.size):
                if(self.islegal(row,col,playerColor, oppColor)):
                    tmp_board = copy.deepcopy(self.board)
                    self.place_piece(row, col, playerColor, oppColor)

                    # This part is for back up
                    score_back_up = self.get_score(playerColor)
                    if (max_score_back_up is None) or (score_back_up > max_score_back_up):
                        max_score_back_up = score_back_up
                        move_back_up = (row, col)

                    # End of back up part


                    if self.is_end(playerColor, oppColor, level):
                        value = self.evaluation(playerColor, oppColor)
                        if time.time() - self.time > TIME_LIMIT:
                            if (max == None) or (max < value):
                                max = value
                                move = (row, col)
                            self.board = tmp_board
                            break
                    else:
                        value = self.min_value(oppColor, playerColor, value, level + 1)

                    if (max == None) or (max < value):
                        max = value
                        move = (row, col)

                    self.board = tmp_board

        if value is not None:
            if not self.islegal(move[0], move[1], playerColor, oppColor):
                return move_back_up
            else:
                return move
        else:
            return (-1, -1)



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
                            if (min is None) or (min > value):
                                min = value
                            self.board = tmp_board
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
                            if (max is None) or (max < value):
                                max = value
                            self.board = tmp_board
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


def test():
    test_dragon = Dragon()
    test_dragon.board[0][7] = 'B'
    test_dragon.board[0][6] = 'B'
    test_dragon.board[7][6] = 'W'

    test_dragon.PrintBoard()
    print(test_dragon.evaluation('B', 'W'))


test()
