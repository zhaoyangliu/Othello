#Othello
*Use python 3 to compile file*
* Running Matchmaker.py with command:
<pre>
    Matchmaker.py Dragon.py Dragon2.py
</pre>
Dragon.py is our player. Dragon2 is the default player which just scan next available step.



	
* Implement the greedy function, including four greedy cases: (Yang Zhang)
	<pre>
	def greedy(self, playerColor, oppColor):
	def get_corner(self, playerColor, oppColor):
	def no_step(self, playerColor, oppColor):	
    </pre>
* Implement iterative traversing and the picking strategy. Also bad_move function according to experience (Zhao Yang Liu)
	
    <pre>
	def play_square(self, row, col, playerColor, oppColor, board):
    def bad_move(self, move, playerColor, oppColor):
    </pre>

* Decide when to reach the edge and evaluation method. Also consider time limitation (Elaine Chang)
<pre>
    def is_end(self, playerColor, oppColor, level):
    def evaluation(self, playerColor, oppColor):
    def get_score(self, Color):
    def is_full(self):
</pre>
* implement the alpha-beta minimax method, also some assistant function like get_square_num_from_set (Ran Li)
<pre>
    def get_square_num_from_set(self, square_set, playerColor, oppColor):
    def make_move(self, playerColor, oppColor):
    def min_value(self, playerColor, oppColor, alpha, level):
    def max_value(self, playerColor, oppColor, beta, level):
</pre>
