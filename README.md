#Othello
*Use python 3 to compile file*
* Running Matchmaker.py with command:
    Matchmaker.py Dragon.py Dragon2.py

Dragon.py is our player. Dragon2 is the default player which just scan next available step.



	
* Implement the greedy function, including four greedy cases: (Yang Zhang)
	
	def greedy(self, playerColor, oppColor):
	def get_corner(self, playerColor, oppColor):
	def no_step(self, playerColor, oppColor):	

* Implement iterative traversing and the picking strategy. Also bad_move function according to experience (Zhao Yang Liu)
	
	def play_square(self, row, col, playerColor, oppColor, board):
    def bad_move(self, move, playerColor, oppColor):
  

* Decide when to reach the edge and evaluation method. Also consider time limitation (Elaine Chang)

    def is_end(self, playerColor, oppColor, level):
    def evaluation(self, playerColor, oppColor):
    def get_score(self, Color):
    def is_full(self):

* implement the alpha-beta minimax method, also some assistant function like get_square_num_from_set (Ran Li)

    def get_square_num_from_set(self, square_set, playerColor, oppColor):
    def make_move(self, playerColor, oppColor):
    def min_value(self, playerColor, oppColor, alpha, level):
    def max_value(self, playerColor, oppColor, beta, level):

