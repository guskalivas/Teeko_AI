import random
import copy
import time


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        # intially set drop phase to true
        drop_phase = True
        move = [] # list to make moves with to return
        succ = self.succ(state) # get the successor of this state
        # intial postion of board to set up most advantagous spot if its empty
        if sum(x.count(self.my_piece) for x in self.board) == 0 and self.board[2][2] == ' ':
            move.insert(0, (2, 2))
            return move
        
        # check the number of 'r' and 'b' on board if theres 4 of each drop phase is false
        if sum(x.count('r') for x in self.board) == 4 and sum(x.count('b') for x in self.board) == 4:
            drop_phase = False

        # if not during drop phase use minimax to make next move from one postion to next
        if not drop_phase:
            move = []
            d = self.Max_value(state, 0)
            val = d['val']
            m = d['move']
            p = d['pos']
            f = d['from']
            s = sorted(succ, key=lambda e: e['f'])
            moveto = s[-1]
            move.insert(1, (moveto['from'][0], moveto['from'][1]))
            move.insert(0, (moveto['pos'][0], moveto['pos'][1]))
            return move # return the from, to move

        else: #else use minimax and to make move during drop phase selecting spot to place AI piece
            d = self.Max_value(state, 0)
            val = d['val']
            m = d['move']
            p = d['pos']
            hold = []
            move = []
            n = None
            hold = []
            for s in succ:
                p = s['pos'][0]
                p1 = s['pos'][1]
                if s['f'] == val and state[p][p1] == ' ':
                    hold.append(s)
            if len(hold) == 1:
                row = hold[0]['pos'][0]
                col = hold[0]['pos'][1]
            else:
                f = sorted(hold, key=lambda e: e['pos'])
                row = f[0]['pos'][0]
                col = f[0]['pos'][1]

        move.insert(0, (row, col)) # return the move 
        return move

    '''
    CheckNeighbor takes in state, and x,y postion, it is called from the successor function if drop phase is
    over. Returns valid moves for when drop phase is over
    '''
    def checkneighbor(self, state, x, y):
        full = []
        if self.board[x+1][y] == ' ' and x+1 <= 4:
            d = {}
            s = copy.deepcopy(state)
            s[x+1][y] = self.my_piece
            s[x][y] = ' '
            d['pos'] = [x+1, y]
            d['from'] = [x, y]
            d['state'] = s
            d['f'] = self.heuristic_game_value(s)
            full.append(d)
        if self.board[x][y+1] == ' ' and y+1 <= 4:
            d = {}
            s = copy.deepcopy(state)
            s[x][y+1] = self.my_piece
            s[x][y] = ' '
            d['pos'] = [x, y+1]
            d['from'] = [x, y]
            d['state'] = s
            d['f'] = self.heuristic_game_value(s)
            full.append(d)
        if self.board[x+1][y+1] == ' 'and x+1 <= 4 and y+1 <= 4:
            d = {}
            s = copy.deepcopy(state)
            s[x+1][y+1] = self.my_piece
            s[x][y] = ' '
            d['pos'] = [x+1, y+1]
            d['from'] = [x, y]
            d['state'] = s
            d['f'] = self.heuristic_game_value(s)
            full.append(d)
        if self.board[x-1][y-1] == ' 'and x-1 >= 0 and y-1 >= 0:
            d = {}
            s = copy.deepcopy(state)
            s[x-1][y-1] = self.my_piece
            s[x][y] = ' '
            d['pos'] = [x-1, y-1]
            d['from'] = [x, y]
            d['state'] = s
            d['f'] = self.heuristic_game_value(s)
            full.append(d)
        if self.board[x-1][y] == ' ' and x-1 >= 0:
            d = {}
            s = copy.deepcopy(state)
            s[x-1][y] = self.my_piece
            s[x][y] = ' '
            d['pos'] = [x-1, y]
            d['from'] = [x, y]
            d['state'] = s
            d['f'] = self.heuristic_game_value(s)
            full.append(d)
        if self.board[x][y-1] == ' 'and y-1 >= 0:
            d = {}
            s = copy.deepcopy(state)
            s[x][y-1] = self.my_piece
            s[x][y] = ' '
            d['pos'] = [x, y-1]
            d['from'] = [x, y]
            d['state'] = s
            d['f'] = self.heuristic_game_value(s)
            full.append(d)
        if self.board[x-1][y+1] == ' 'and x-1 >= 0 and y+1 <= 4:
            d = {}
            s = copy.deepcopy(state)
            s[x-1][y+1] = self.my_piece
            s[x][y] = ' '
            d['pos'] = [x-1, y+1]
            d['from'] = [x, y]
            d['state'] = s
            d['f'] = self.heuristic_game_value(s)
            full.append(d)
        if self.board[x+1][y-1] == ' 'and x+1 <= 4 and y-1 >= 0:
            d = {}
            s = copy.deepcopy(state)
            s[x+1][y-1] = self.my_piece
            s[x][y] = ' '
            d['pos'] = [x+1, y-1]
            d['from'] = [x, y]
            d['state'] = s
            d['f'] = self.heuristic_game_value(s)
            full.append(d)
        return full

    '''
    Successor function takes in a state and returns a list of valid successor states. During drop phase 
    it moves my piece to all the other potential spots. During not drop phase it calls check neightbor function
    to get a list of of the valid moves for that state 
    '''
    def succ(self, state):
        full = []
        if sum(x.count(self.my_piece) for x in self.board) < 4:
            for col in range(0, len(state)):
                for row in range(0, len(state)):
                    create = {}
                    s = copy.deepcopy(state)
                    if state[col][row] == ' ':
                        s[col][row] = self.my_piece
                        create['pos'] = [col, row]
                        create['from'] = [col, row]
                        create['state'] = list(s)
                        create['f'] = self.heuristic_game_value(s)
                        full.append(create)
        else:
            for col in range(0, 4):
                for row in range(0, 4):
                    if state[col][row] == self.my_piece:
                        full += self.checkneighbor(state, col, row)

        return full

    '''
    Heruistic game value takes in a current state. It first checks the game value of of the state to check for
    a terminal value. If its a terminal value. Return it, otherwise calculate a heruistic value for the internal
    state by calling get_adjacent function. 
    '''
    def heuristic_game_value(self, state):
        val = self.game_value(state)
        total = 0

        if val == 0:
            total = self.get_adjacent(state)
            #divide by 39 to keep values between -1 and 1
            return total/39
        else:
            return val

    '''
    Get adjacent function calculates the heuristic for a state if its a internal node. It counts the number of
    pieces in a row/diag/col or square. It weights the moves by adding more to count if the move has three in 
    a row/col/diag and an open space next to it. This makes the herusitc higher if there is a move to get 3 in 
    a row vs getting two in a row etc. 
    '''
    def get_adjacent(self, state):
        count = 0
        # loop through and count col peices in a row and add to count
        for row in state:
            for i in range(2):
                if row[i] == self.my_piece and row[i+1] == ' ':
                    count += 1 if row[i] == self.my_piece else count-1
                if row[i] == self.my_piece == row[i+1] and row[i+2] == ' ':
                    count += 2*2 if row[i] == self.my_piece else count-2*2
                if row[i] == self.my_piece == row[i+1] == row[i+2] and row[i+3] == ' ':
                    count += 3*5 if row[i] == self.my_piece else count-3*5
        # loop and count row pieces in a row and add to count 
        for col in range(5):
            for i in range(2):
                if state[i][col] == self.my_piece and state[i+1][col] == ' ':
                    count += 1 if state[i][col] == self.my_piece else count-1
                if state[i][col] == self.my_piece == state[i+1][col] and state[i+2][col] == ' ':
                    count += 2*2 if state[i][col] == self.my_piece else count-2*2
                if state[i][col] == self.my_piece == state[i+1][col] == state[i+2][col] and state[i+3][col] == ' ':
                    count += 3 *5 if state[i][col] == self.my_piece else count-3*5
        # loop to check diag down 
        for x in range(2):
            for y in range(2):
                if state[x][y] == self.my_piece and state[x+1][y+1] == ' ':
                    count += 1 if state[x][y] == self.my_piece else count-1
                if state[x][y] == self.my_piece == state[x+1][y+1] and state[x+2][y+2] == ' ':
                    count += 2 if state[x][y] == self.my_piece else count-2
                if state[x][y] == self.my_piece == state[x+1][y+1] == state[x+2][y+2] and state[x+3][y+3] == ' ':
                    count += 3*3 if state[x][y] == self.my_piece else count-3*3
        # loop to check diag up
        for x in range(2):
            for y in range(3, 5):
                if state[x][y] == self.my_piece and state[x+1][y-1] == ' ':
                    count += 1 if state[x][y] == self.my_piece else count-1
                if state[x][y] == self.my_piece == state[x+1][y-1] and state[x+2][y-2] == ' ':
                    count += 2 if state[x][y] == self.my_piece else count-2
                if state[x][y] == self.my_piece == state[x+1][y-1] == state[x+2][y-2] and state[x+3][y-3] == ' ':
                    count += 3*3 if state[x][y] == self.my_piece else count-3*3
        # loop to check square box 
        for x in range(4):
            for y in range(4):
                if state[x][y] == self.my_piece == state[x+1][y] and state[x][y+1] == ' ':
                    count += 2 if state[x][y] == self.my_piece else count-2
                if state[x][y] == self.my_piece == state[x+1][y] == state[x][y+1] and state[x+1][y+1] == ' ':
                    count += 3*3 if state[x][y] == self.my_piece else count-3*3
        # return the count for the number of peices in a row to be divided by 39
        return count

    '''
    Max_value method for minimax implementation takes in a state and depth
    '''
    def Max_value(self, state, depth):
        d = {} # dictionary to create and return 
        moves = [] # list to return of dictionaries 
        if self.game_value(state) == 1: # check if terminal node
            return {'val': 1, 'move': state}
        if depth == 2: # if reached depth return the hueristic of this state
            return {'val': self.heuristic_game_value(state), 'move': state}
        else: #complete minimax algo
            a = -100
            depth += 1
            suc = self.succ(state)
            d['val'] = a
            d['move'] = state
            for s in suc:
                a = max(a, self.Min_value(s['state'], depth)['val'])
                d['val'] = a
                d['move'] = s['state']
                d['from'] = s['from']
                d['pos'] = s['pos']
                d['f'] = self.heuristic_game_value(s['state'])
                moves.append(d)

        return moves[0]

    '''
    Min_value to implement minimax algorithm takes in state and depth as parameters
    '''
    def Min_value(self, state, depth):
        d = {} # dictionary of the state to create
        moves = [] # list to return 
        if self.game_value(state) == -1: # check terminal node
            return {'val': -1, 'move': state}
        if depth == 2: # check if reached depth
            return {'val': self.heuristic_game_value(state), 'move': state}
        else: # complete min value algo
            b = 100
            depth += 1
            d['val'] = b
            d['move'] = state
            suc = self.succ(state)
            for s in suc:
                b = min(b, self.Max_value(s['state'], depth)['val'])
                d['val'] = b
                d['move'] = state
                d['pos'] = s['pos']
                d['from'] = s['from']
                d['f'] = self.heuristic_game_value(s['state'])
                moves.append(d)

        return moves[0]

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i] == self.my_piece else -1
        # check col wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col] == self.my_piece else -1
        #check diag up wins
        for x in range(2):
            for y in range(2):
                if state[x][y] != ' ' and state[x][y] == state[x+1][y+1] == state[x+2][y+2] == state[x+3][y+3]:
                    return 1 if state[x][y] == self.my_piece else -1
        #check diag down wins
        for x in range(2):
            for y in range(3, 5):
                if state[x][y] != ' ' and state[x][y] == state[x+1][y-1] == state[x+2][y-2] == state[x+3][y-3]:
                    return 1 if state[x][y] == self.my_piece else -1
        #check square box wins 
        for x in range(4):
            for y in range(4):
                if state[x][y] != ' ' and state[x][y] == state[x+1][y] == state[x][y+1] == state[x+1][y+1]:
                    return 1 if state[x][y] == self.my_piece else -1

        return 0  # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################


def main():

    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

    # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at " +
                chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from " +
                chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")
if __name__ == "__main__":
    main()
