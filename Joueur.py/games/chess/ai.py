import random
import time
import sys
#sys.setrecursionlimit(50000000)

# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
import random
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The AI you add and improve code inside to play Chess. """

    @property
    def game(self) -> 'games.chess.game.Game':
        """games.chess.game.Game: The reference to the Game instance this AI is playing.
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self) -> 'games.chess.player.Player':
        """games.chess.player.Player: The reference to the Player this AI controls in the Game.
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self) -> str:
        """This is the name you send to the server so your AI will control the player named this string.

        Returns:
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Omen" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self) -> None:
        """This is called once the game starts and your AI knows its player and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        # <<-- /Creer-Merge: start -->>

    def game_updated(self) -> None:
        """This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won: bool, reason: str) -> None:
        """This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    
    #####Start of code######
    
    
    # converts fen string and returns list with values
    def fen_to_board(self, fen_str):
        board = []
        ranks = fen_str.split('/')[::-1]
        for rank in ranks:
            row = []
            for char in rank:
                if char.isdigit():
                    row += [''] * int(char)
                else:
                    row.append(char)
            board += row
        return board
    
    # checks if move is valid of pawn
    # def get_valid_moves_for_pawn(self, board, index) -> list[int]:
    def get_valid_moves_for_pawn(self, board, index) :
        """
        Returns a list of valid moves for a pawn on the board at the given index.

        Args:
            board (list): the current state of the board as a 1D array
            index (int): the index of the pawn on the board

        Returns:
            list: a list of valid moves for the given pawn
        """
        valid_moves = []
        color = board[index].isupper()

        # Calculate the pawn's current rank and file
        rank = index // 8
        file = index % 8

        # Determine the direction of the pawn's movement based on its color
        direction = 1 if color else -1

        # Check if the pawn can move one or two spaces forward
        if board[index + direction * 8] == '':
            valid_moves.append(index + direction * 8)
            if (rank == 6 and color == False and board[index + direction * 16] == '') or (rank == 1 and color == True and board[index + direction * 16] == ''):
                valid_moves.append(index + direction * 16)

        return valid_moves

        # Check if the pawn can capture diagonally to the left
        if file > 0:
            if board[index + direction * 7] != '':
                if (color and board[index + direction * 7].islower()) or (not color and board[index + direction * 7].isupper()):
                    valid_moves.append(index + direction * 7)
            else:
                # Check for en passant capture to the left
                en_fen_split = self.game.fen.split(' ')
                en_passant_uci = en_fen_split[3]
                if en_passant_uci == '-':
                    en_passant = -1
                else:
                    file = ord(en_passant_uci[0]) - ord('a')
                    rank = int(en_passant_uci[1])
                    en_passant = rank * 8 + file
                if en_passant == index + direction * 7:
                    valid_moves.append(en_passant)

        # Check if the pawn can capture diagonally to the right
        if file < 7:
            if board[index + direction * 9] != '':
                if (color and board[index + direction * 9].islower()) or (not color and board[index + direction * 9].isupper()):
                    valid_moves.append(index + direction * 9)
            else:
                # Check for en passant capture to the right
                en_fen_split = self.game.fen.split(' ')
                en_passant_uci = en_fen_split[3]
                if en_passant_uci == '-':
                    en_passant = -1
                else:
                    file = ord(en_passant_uci[0]) - ord('a')
                    rank = int(en_passant_uci[1])
                    en_passant = rank * 8 + file
                if en_passant == index + direction * 9:
                    valid_moves.append(en_passant)

        return valid_moves



    # checks if move is valid of rook
    def get_valid_moves_for_rook(self, board, index):
        """
        Returns a list of valid moves for a rook on the board at the given index.

        Args:
            board (list): the current state of the board as a 1D array
            index (int): the index of the rook on the board

        Returns:
            list: a list of valid moves for the given rook
        """
        valid_moves = []
        color = board[index].isupper()

        # Calculate the rook's current rank and file
        rank = index // 8
        file = index % 8

        # Determine the direction of the rook's movement based on its color
        direction = -1 if color else 1

        # Check valid moves in the horizontal direction
        for i in range(file-1, -1, -1): # Check left
            if board[rank*8 + i] == '':
                valid_moves.append(rank*8 + i)
            elif (color and board[rank*8 + i].islower()) or (not color and board[rank*8 + i].isupper()):
                valid_moves.append(rank*8 + i)
                break
            else:
                break
        for i in range(file+1, 8): # Check right
            if board[rank*8 + i] == '':
                valid_moves.append(rank*8 + i)
            elif (color and board[rank*8 + i].islower()) or (not color and board[rank*8 + i].isupper()):
                valid_moves.append(rank*8 + i)
                break
            else:
                break

        # Check valid moves in the vertical direction
        for i in range(rank-1, -1, -1): # Check up
            if board[i*8 + file] == '':
                valid_moves.append(i*8 + file)
            elif (color and board[i*8 + file].islower()) or (not color and board[i*8 + file].isupper()):
                valid_moves.append(i*8 + file)
                break
            else:
                break
        for i in range(rank+1, 8): # Check down
            if board[i*8 + file] == '':
                valid_moves.append(i*8 + file)
            elif (color and board[i*8 + file].islower()) or (not color and board[i*8 + file].isupper()):
                valid_moves.append(i*8 + file)
                break
            else:
                break

        return valid_moves
     
     # checks if move is valid of queen
    def get_valid_moves_for_queen(self, board, index):
        """
        Returns a list of valid moves for a queen on the board at the given index.

        Args:
            board (list): the current state of the board as a 1D array
            index (int): the index of the queen on the board

        Returns:
            list: a list of valid moves for the given queen
        """
        valid_moves = []
        color = board[index].isupper()

        # Calculate the queen's current rank and file
        rank = index // 8
        file = index % 8

        # Determine the direction of the queen's movement based on its color
        direction = -1 if color else 1

        # Check valid moves in the horizontal direction
        for i in range(file-1, -1, -1): # Check left
            if board[rank*8 + i] == '':
                valid_moves.append(rank*8 + i)
            elif (color and board[rank*8 + i].islower()) or (not color and board[rank*8 + i].isupper()):
                valid_moves.append(rank*8 + i)
                break
            else:
                break
        for i in range(file+1, 8): # Check right
            if board[rank*8 + i] == '':
                valid_moves.append(rank*8 + i)
            elif (color and board[rank*8 + i].islower()) or (not color and board[rank*8 + i].isupper()):
                valid_moves.append(rank*8 + i)
                break
            else:
                break

        # Check valid moves in the vertical direction
        for i in range(rank-1, -1, -1): # Check up
            if board[i*8 + file] == '':
                valid_moves.append(i*8 + file)
            elif (color and board[i*8 + file].islower()) or (not color and board[i*8 + file].isupper()):
                valid_moves.append(i*8 + file)
                break
            else:
                break
        for i in range(rank+1, 8): # Check down
            if board[i*8 + file] == '':
                valid_moves.append(i*8 + file)
            elif (color and board[i*8 + file].islower()) or (not color and board[i*8 + file].isupper()):
                valid_moves.append(i*8 + file)
                break
            else:
                break

        # Check valid moves in the diagonal direction
        for i, j in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
            for k in range(1, 8):
                r = rank + k*i
                f = file + k*j
                if r < 0 or r > 7 or f < 0 or f > 7:
                    break
                if board[r*8 + f] == '':
                    valid_moves.append(r*8 + f)
                elif (color and board[r*8 + f].islower()) or (not color and board[r*8 + f].isupper()):
                    valid_moves.append(r*8 + f)
                    break
                else:
                    break

        return valid_moves

    # checks if move is valid of bishop    
    def get_valid_moves_for_bishop(self, board, index):
        """
        Returns a list of valid moves for a bishop on the board at the given index.

        Args:
            board (list): the current state of the board as a 1D array
            index (int): the index of the bishop on the board

        Returns:
            list: a list of valid moves for the given bishop
        """
        valid_moves = []
        color = board[index].isupper()

        # Calculate the bishop's current rank and file
        rank = index // 8
        file = index % 8

        # Check valid moves in the diagonal directions
        for i in range(1, min(rank+1, 8-file)):
            dest_index = (rank-i)*8 + (file+i)
            if board[dest_index] == '':
                valid_moves.append(dest_index)
            elif (color and board[dest_index].islower()) or (not color and board[dest_index].isupper()):
                valid_moves.append(dest_index)
                break
            else:
                break
        for i in range(1, min(8-rank, file+1)):
            dest_index = (rank+i)*8 + (file-i)
            if board[dest_index] == '':
                valid_moves.append(dest_index)
            elif (color and board[dest_index].islower()) or (not color and board[dest_index].isupper()):
                valid_moves.append(dest_index)
                break
            else:
                break
        for i in range(1, min(rank+1, file+1)):
            dest_index = (rank-i)*8 + (file-i)
            if board[dest_index] == '':
                valid_moves.append(dest_index)
            elif (color and board[dest_index].islower()) or (not color and board[dest_index].isupper()):
                valid_moves.append(dest_index)
                break
            else:
                break
        for i in range(1, min(8-rank, 8-file)):
            dest_index = (rank+i)*8 + (file+i)
            if board[dest_index] == '':
                valid_moves.append(dest_index)
            elif (color and board[dest_index].islower()) or (not color and board[dest_index].isupper()):
                valid_moves.append(dest_index)
                break
            else:
                break

        return valid_moves

     # checks if move is valid of knight   
    def get_valid_moves_for_knight(self, board, index):
        """
        Returns a list of valid moves for a knight on the board at the given index.

        Args:
            board (list): the current state of the board as a 1D array
            index (int): the index of the knight on the board

        Returns:
            list: a list of valid moves for the given knight
        """
        valid_moves = []
        color = board[index].isupper()

        # Calculate the knight's current rank and file
        rank = index // 8
        file = index % 8

        # Define the relative positions of the knight's valid moves
        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        # Check each potential move
        for move in moves:
            new_rank = rank + move[0]
            new_file = file + move[1]

            # Check if the new position is on the board
            if 0 <= new_rank <= 7 and 0 <= new_file <= 7:

                # Check if the new position is empty or contains an opponent's piece
                if board[new_rank*8 + new_file] == '' or (color and board[new_rank*8 + new_file].islower()) or (not color and board[new_rank*8 + new_file].isupper()):
                    valid_moves.append(new_rank*8 + new_file)

        return valid_moves
    
    # checks if move is valid of king
    def get_valid_moves_for_king(self, board, index):
        """
        Returns a list of valid moves for a king on the board at the given index.

        Args:
            board (list): the current state of the board as a 1D array
            index (int): the index of the king on the board

        Returns:
            list: a list of valid moves for the given king
        """
        valid_moves = []
        color = board[index].isupper()

        # Calculate the king's current rank and file
        rank = index // 8
        file = index % 8

        # Check valid moves in all 8 possible directions
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= rank+i <= 7 and 0 <= file+j <= 7:
                    dest_index = (rank+i)*8 + (file+j)
                    if board[dest_index] == '':
                        valid_moves.append(dest_index)
                    elif (color and board[dest_index].islower()) or (not color and board[dest_index].isupper()):
                        valid_moves.append(dest_index)

        return valid_moves

    # returns position of pawn
    def find_pawn_indices(self, board, color):
        """
        Returns a list of indices where pawns of the given color are located on the board.

        Args:
            board (list): a 1D array list representing the current state of the board.
            color (str): the color of the pawns to find ('white' or 'black').

        Returns:
            list: a list of indices where pawns of the given color are located on the board.
        """
        pawn_indices = []
        for i, piece in enumerate(board):
            if (color == 'white' and piece == 'P') or (color == 'black' and piece == 'p'):
                pawn_indices.append(i)
        return pawn_indices  
 
    # returns position of rook
    def find_rook_indices(self, board, color):
        """
        Returns a list of indices where rooks of the given color are located on the board.

        Args:
            board (list): a 1D array list representing the current state of the board.
            color (str): the color of the rooks to find ('white' or 'black').

        Returns:
            list: a list of indices where rooks of the given color are located on the board.
        """
        rook_indices = []
        for i, piece in enumerate(board):
            if (color == 'white' and piece == 'R') or (color == 'black' and piece == 'r'):
                rook_indices.append(i)
        return rook_indices
   
   # returns position of queen
    def find_queen_indices(self, board, color):
        """
        Returns a list of indices where queens of the given color are located on the board.

        Args:
            board (list): a 1D array list representing the current state of the board.
            color (str): the color of the queens to find ('white' or 'black').

        Returns:
            list: a list of indices where queens of the given color are located on the board.
        """
        queen_indices = []
        for i, piece in enumerate(board):
            if (color == 'white' and piece == 'Q') or (color == 'black' and piece == 'q'):
                queen_indices.append(i)
        return queen_indices

    # returns position of bishop
    def find_bishop_indices(self, board, color):
        """
        Returns a list of indices of all bishops on the board for the given color.

        Args:
            board (list): the current state of the board as a 1D array
            color (bool): the color of the bishops to find, True for white, False for black

        Returns:
            list: a list of indices of all bishops of the given color on the board
        """
        bishop_indices = []
        for i, piece in enumerate(board):
            if (color == 'white' and piece == 'B') or (color == 'black' and piece == 'b'):
                bishop_indices.append(i)
            elif piece == 'b' and not color:
                bishop_indices.append(i)
        return bishop_indices

   # returns position of knight
    def find_knight_indices(self, board, color):
        """
        Returns a list of indices where knights of the given color are located on the board.

        Args:
            board (list): a 1D array list representing the current state of the board.
            color (str): the color of the knights to find ('white' or 'black').

        Returns:
            list: a list of indices where knights of the given color are located on the board.
        """
        knight_indices = []
        for i, piece in enumerate(board):
            if (color == 'white' and piece == 'N') or (color == 'black' and piece == 'n'):
                knight_indices.append(i)
        return knight_indices

    # returns position of king
    def find_king_indices(self, board, color):
        """
        Returns a list of indices where kings of the given color are located on the board.

        Args:
            board (list): a 1D array list representing the current state of the board.
            color (str): the color of the kings to find ('white' or 'black').

        Returns:
            list: a list of indices where kings of the given color are located on the board.
        """
        king_indices = []
        for i, piece in enumerate(board):
            if (color == 'white' and piece == 'K') or (color == 'black' and piece == 'k'):
                king_indices.append(i)
        return king_indices

    #converts valid move position into uci format 
    def move_to_uci(self, move):
        """
        Converts a move represented as a list of two indices to a move string in UCI format.

        Args:
            move (list): a list of two indices representing the start and end squares of the move

        Returns:
            str: the move string in UCI format
        """
        start_file = chr((ord('a') + (move[0] % 8)))
        start_rank = str(((move[0]//8) + 1))
        end_file = chr((ord('a') + (move[1] % 8)) )
        end_rank = str(((move[1]//8) + 1))
        return start_file + start_rank + end_file + end_rank

    
    

    # The heuristic function to evaluate the board
    def evaluate(self, board):
        """
        Evaluate the given chess board based on piece values.

        Args:
            board (list): The current state of the chess board.

        Returns:
            float: The evaluation score of the board.
        """
        piece_values = {
            'P': 1,  # Pawn value
            'N': 3,  # Knight value
            'B': 3,  # Bishop value
            'R': 5,  # Rook value
            'Q': 9,  # Queen value
            'K': 0,  # King value (not used in piece values calculation)
            'p': -1,  # Black Pawn value
            'n': -3,  # Black Knight value
            'b': -3,  # Black Bishop value
            'r': -5,  # Black Rook value
            'q': -9,  # Black Queen value
            'k': 0  # Black King value (not used in piece values calculation)
        }

        score = 0
        for piece in board:
            if piece in piece_values:
                score += piece_values[piece]

        return score

    def is_king_in_check(self, board, player):
        """Return True if the player's king is in check."""
        # Find the player's king
        king_index = self.find_king_indices(board, self.player.color)[0]
        # Check if any of the opponent's pieces can attack the king
        opponent_color = 'white' if self.player.color == 'white' else 'black'
        opponent_moves = self.get_all_moves(board, opponent_color)
        #print("this is opponent moves", opponent_moves)
        #print("this is king's index", king_index)
        for move in opponent_moves:
           # print(move[-1])
            if move[-1] == king_index:
                return True
        return False

    # The TL-ID-DL-MM algorithm with time-based depth limit
    def tl_id_dl_mm(self, board, max_time=5):
        start_time = time.time()
        depth = 0
        best_move = None
        while (time.time() - start_time) < max_time and depth <= 3:
            print(' d=',depth, flush=True)
            _, move = self.dl_mm(board, depth, True)
            best_move = move
            depth += 1
        #print('best move in tl-id-dl-mm ', best_move)
        return best_move

    #--------------------
    def results( self, board1, move ) :
        board2 = list(board1)
        piece = board2[move[0]]
        board2[move[0]] = ''
        board2[move[1]] = piece
        return board2
        
    #--------------------

    # The depth-limited MiniMax algorithm
    def dl_mm(self, board, depth, is_maximizing_player):
        if depth <= 0:
            this_value = self.evaluate(board)
            #print('leaf ',this_value)
            return this_value, None

        best_move = None
        if is_maximizing_player:
            best_value = -float('inf')
            for move in self.get_all_moves(board, 'white'):
                new_board = self.results( board, move )
                value, _ = self.dl_mm(new_board, depth-1, False)
                if value > best_value:
                    best_value = value
                    best_move = move
                    
            #print(f'in dl_mm {best_value} {best_move}')
            return best_value, best_move
        else:
            best_value = float('inf')
            for move in self.get_all_moves(board, 'black'):
                #new_board = self.make_move()
                new_board = self.results(board, move)
                value, _ = self.dl_mm(new_board, depth-1, True)
                if value < best_value:
                    best_value = value
                    best_move = move
                    
          #  print(f'in else dl_mm {best_value} {best_move}')
            return best_value, best_move
    
    def get_all_moves(self, board, player):
        
        fen_split = self.game.fen.split(' ')
        fen_reverse = fen_split[0]
        #print('this is rev fen ', fen_reverse)
        # Convert the FEN string to a board representation
        board = self.fen_to_board(fen_reverse)

        #to find opponents color
        if self.player.color == 'white':
            opponent_color = 'black'
        else:
            opponent_color = 'white'
        #gets pawn position
        pawn_index  = self.find_pawn_indices(board, opponent_color)

        #gets rook position
        rook_index = self.find_rook_indices(board, opponent_color)

        #gets queen position
        queen_index = self.find_queen_indices(board, opponent_color)

        #gets bishop position
        bishop_index = self.find_bishop_indices(board, opponent_color)

        #gets knight position
        knight_index = self.find_knight_indices(board, opponent_color)

        #gets king position
        king_index = self.find_king_indices(board, opponent_color)

        #print(board)
        #print("this is king", pawn_index)
        
        valid_uci = []
        valid_move = []
       
       # creating a array of piece moves 
        piece_index = [pawn_index, rook_index, queen_index, bishop_index, knight_index, king_index]
        
        
        
        valid_uci = []
        valid_move_w = []
        valid_move_b = []
        if opponent_color == 'white':
            for indices in piece_index: 
                for i in indices:
                    if board[i] == 'P':
                        valid_moves = self.get_valid_moves_for_pawn(board, i)
                    elif board[i] == 'R':
                        valid_moves = self.get_valid_moves_for_rook(board, i)
                    elif board[i] == 'Q':
                        valid_moves = self.get_valid_moves_for_queen(board, i)
                    elif board[i] == 'B':
                        valid_moves = self.get_valid_moves_for_bishop(board, i)
                    elif board[i] == 'N':
                        valid_moves = self.get_valid_moves_for_knight(board, i)
                    elif board[i] == 'K':
                        valid_moves = self.get_valid_moves_for_king(board, i)

                for j in valid_moves:
                    valid_move.append([i, j])
                    #print('this is validd moves',valid_move)

                for mov_w in valid_move:
                    valid_uci = self.move_to_uci(mov_w)

            return valid_move
            
        elif opponent_color == 'black':
            for indices in piece_index:  
                for i in indices:
                    if board[i] == 'p':
                        valid_moves = self.get_valid_moves_for_pawn(board, i)
                    elif board[i] == 'r':
                        valid_moves = self.get_valid_moves_for_rook(board, i)
                    elif board[i] == 'q':
                        valid_moves = self.get_valid_moves_for_queen(board, i)
                    elif board[i] == 'b':
                        valid_moves = self.get_valid_moves_for_bishop(board, i)
                    elif board[i] == 'n':
                        valid_moves = self.get_valid_moves_for_knight(board, i)
                    elif board[i] == 'k':
                        valid_moves = self.get_valid_moves_for_king(board, i)

                for j in valid_moves:
                    valid_move.append([i, j])
    
                for mov_b in valid_move:
                    valid_uci = self.move_to_uci(mov_b)

            return valid_move
            
    
    # default make move function 
    def make_move(self) -> str:
        #print(f"this is self game fen {self.game.fen}")
        
        fen_split = self.game.fen.split(' ')
        fen_reverse = fen_split[0]
        #print('this is rev fen ', fen_reverse)
        # Convert the FEN string to a board representation
        board = self.fen_to_board(fen_reverse)
        print('at ', board)

        #gets pawn position
        pawn_index  = self.find_pawn_indices(board, self.player.color)

        #gets rook position
        rook_index = self.find_rook_indices(board, self.player.color)

        #gets queen position
        queen_index = self.find_queen_indices(board, self.player.color)

        #gets bishop position
        bishop_index = self.find_bishop_indices(board, self.player.color)

        #gets knight position
        knight_index = self.find_knight_indices(board, self.player.color)

        #gets king position
        king_index = self.find_king_indices(board, self.player.color)

        #print(board)
        #print("this is king", pawn_index)
        
        valid_uci = []
        valid_move = []
       
       # creating a array of piece moves 
        piece_index = [pawn_index, rook_index, queen_index, bishop_index, knight_index, king_index]
        

        for indices in piece_index:
            for x in indices:
                index = int(x)
                if indices == pawn_index:
                    valid_moves = self.get_valid_moves_for_pawn(board, index)
                elif indices == rook_index:
                    valid_moves = self.get_valid_moves_for_rook(board, index)
                elif indices == queen_index:
                    valid_moves = self.get_valid_moves_for_queen(board, index)
                elif indices == bishop_index:
                    valid_moves = self.get_valid_moves_for_bishop(board, index)
                elif indices == knight_index:
                    valid_moves = self.get_valid_moves_for_knight(board, index)
                elif indices == king_index:
                    valid_moves = self.get_valid_moves_for_king(board, index)

                for y in valid_moves:
                    valid_move.append([x,y])
                    
        print('old valid move', valid_move)
		
        my_move = self.tl_id_dl_mm(board, max_time=5)
        print("Go: ", my_move)
        
        if len(valid_move) != 0:
            rand_moves = random.choice(valid_move)
            rand_uci_move = self.move_to_uci(rand_moves)
        
        
        for mov in valid_move:
            uci_mov = self.move_to_uci(mov)
            
            valid_uci.append(uci_mov)
       # print(f"Valid move {valid_moves}")    
        #prints number of moves available
       # print(len(valid_uci))
        #prints valid moves available in uci format
       # print(*valid_uci)
        #prints the move which is to be played
        print(f"My move = {rand_uci_move}")
        
        print(self.is_king_in_check(board, True))
        
        return rand_uci_move

       



        # <<-- /Creer-Merge: makeMove -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>
