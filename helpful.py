import sys

class Helpful:

    def king_count(self, board):
        '''
        this functions checks if none, one or both kings have been destroyed. it prints out a message or nothing accordingly.
        '''
        king_count = 0
        for row in range(8):
            for col in range(8):
                tile = board[row][col]
                piece = [char for char in tile]
                if "K" in piece or "k" in piece: king_count += 1
                else: pass
        if king_count == 0: 
            #self.print_msg('stalemate')
            return True
        elif king_count == 1: 
            #self.print_msg("checkmate")
            return True
        else: return False

    def parse_move(self, move, rowswap):
        '''
        this functions converts the move according to my board arrays and returns it
        '''
        return self.char_to_int(move[0]), 8 - int(move[1]), self.char_to_int(move[3]), 8 - int(move[4]) 

    def get_current_fen(self, board, player_to_move, castling_rights, en_passant_square):
        '''
        This function turns the game state into a fen string to be stored in a history. Used for threefold checks
        '''
        fen = ""
        for row in board:
            empty_count = 0
            for square in row:
                if square == ".": empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += square
            if empty_count > 0: fen += str(empty_count)
            fen += "/"
        fen = fen[:-1] + f" {player_to_move} {castling_rights} {en_passant_square}"
        return fen

    def is_valid_tile(self, row, col):
        '''
        this functions checks if the tile being checked or selected is valid
        '''
        if 0 <= row < 8 and  0 <= col < 8: return True

    def chess_coordinates_to_index(self, coordinates):
        '''
        this functions convert chess coordinates to indices (row, col) for a 2D array
        '''
        file, rank = coordinates[0], coordinates[1]
        col = ord(file) - ord('a')
        row = 8 - int(rank)
        return row, col

    def concat_and_place(self, validated_board, row, column, obstacle):
        '''
        this functions is just used to concatenate pieces together and returns to where it will be placed on the board. Eg. walls with a piece
        '''
        concat_piece = ''
        tile = [char for char in validated_board[row][column]]
        if obstacle == "|": concat_piece = obstacle + validated_board[row][column]
        elif obstacle == "_":
            if tile[0] == "|":
                tile[0] = "|_"
                for char in tile: concat_piece += char
            else: concat_piece = obstacle + validated_board[row][column]
        else:
            tile[-1] = obstacle[-1]
            for char in tile: concat_piece += char
        return concat_piece

    def get_opponent(self, player):
        '''
        this function idea was taken from the last project. it basically just returns the oppossing player index
        '''
        return 1 - player

    def int_to_char(self, index):
        '''
        this function idea was taken from the last project. it basically just returns the corresponnding alphabetical value of a number
        '''
        return chr(index + 65)

    def char_to_int(self, ch):
        '''
        this function idea was taken from the last project. it basically just returns the numerical value of the corresponding letter
        '''
        return ord(str(ch).upper()) - 65

    def termination(self, coordinates): 
        '''
        this function basically just terminates the game
        '''
        sys.stderr.write("ERROR: illegal move " + coordinates)
        sys.exit()

    def print_msg(self, msg):
        '''
        this function prints a message to stdout
        '''
        sys.stdout.write("INFO: " + msg)
        sys.stdout.write('\n')

    def find_king(self, validated_board, player):
        '''
        this functions finds the position of the player's king and returns it
        '''
        king = 'K' if player == 0 else 'k'
        for row in range(8):
            for col in range(8):
                if len(validated_board[row][col]) > 1:
                    piece = [char for char in validated_board[row][col]]
                    if piece[-1] == king: return row, col
                else:
                    if validated_board[row][col] == king: return row, col 
 
    def get_piece_at(self, board, row, col):
        '''
        this functions just gets the piece requested from the first 2 letters of the move and returns it
        '''
        if (row > 8 or row < 0) or (col > 8 or col < 0): pass
        else:
            tile = [char for char in board[row][col]]
            return tile
        
    def is_init_status(self, board, status_line, halfmove_count):
        '''
        this functions checks if the board is in an intial state for obstacles to be placed
        '''
        wpawn_count = 0    
        bpawn_count = 0    
        row = [char for char in board[6]]
        for piece in row:
            if piece[-1] == "P": wpawn_count += 1
        if wpawn_count != 8 or board[7][1] != "N" or board[7][6] != "N" or halfmove_count != 0: return False
        row = [char for char in board[1]]
        for piece in row:
            if piece[-1] == "p": bpawn_count += 1
        if bpawn_count != 8 or board[0][1] != "n" or  board[0][6] != "n" or halfmove_count != 0: return False        
        return True

    def tile_name(self, row, col):
        # Convert row index to letter (A-H) and add 1 to col index (1-8)
        return chr(ord('A') + col) + str(8 - row)