import stdarray
from helpful import Helpful

class Moves(Helpful):
    def __init__(self, status_line):
        self.status_line = status_line
        self.board_coordinates = stdarray.create2D(8, 8, 0)
        ##potential change here
        Column = 9
        for Row in range(8):
            Column = Column - 1
            for tile in range(8): self.board_coordinates[Row][tile] = self.int_to_char(tile).lower() + str(Column)

    def king_possible_moves(self, validated_board, board_coordinates, player, from_col, from_row):
        '''
        This function checks for all possible moves the player's king can make and returns them.
        '''
        possible_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        pieces = ["P", "R", "N", "B", "Q", "K", "O"] if player == 0 else ["p", "r", "n", "b", "q", "k", "O"]
        
        # Loop through all possible move directions for the king.
        for dir_col, dir_row in directions:
            new_col = from_col + dir_col
            new_row = from_row + dir_row
            
            # Check if the new position is a valid tile on the board.
            if self.is_valid_tile(new_row, new_col):
                destination_piece = self.get_piece_at(validated_board, new_row, new_col)
                
                # Check each possible move direction and add valid moves to the list.
                if dir_col == 1 and dir_row == 0:
                    if "|" in destination_piece or destination_piece[-1] in pieces:
                        pass
                    else: possible_moves.append(board_coordinates[new_row][new_col])
                elif dir_row == -1 and dir_col == 0:
                    if "_" in destination_piece:
                        pass
                    elif destination_piece[-1] in pieces:
                        pass
                    else: possible_moves.append(board_coordinates[new_row][new_col])

            # Similar checks for other directions...
                #check left tile
                elif dir_col == -1 and dir_row == 0:
                    current_position = self.get_piece_at(validated_board, new_row, new_col+1)
                    if "|" in current_position: pass
                    elif destination_piece[-1] in pieces: pass
                    else: possible_moves.append(board_coordinates[new_row][new_col])
                #check lower tile
                elif dir_row == 1 and dir_col == 0:
                    current_position = self.get_piece_at(validated_board, new_row-1, new_col)
                    if "_" in current_position: pass
                    elif destination_piece[-1] in pieces: pass
                    else: possible_moves.append(board_coordinates[new_row][new_col])
                #check upper right tile
                elif dir_row == -1 and dir_col == 1:
                    destination_piecetoLeft = self.get_piece_at(validated_board, new_row, new_col-1)
                    destination_pieceBelow = self.get_piece_at(validated_board, new_row+1, new_col)
                ##turn these if statements into a function
                    if destination_piece[-1] in pieces or "O" in destination_piece: pass
                    elif "|" in destination_piece and "_" in destination_piece: pass
                    elif "|" in destination_piece and "|" in destination_pieceBelow: pass 
                    elif "_" in destination_piece and "_" in destination_piecetoLeft: pass
                    elif "_" in destination_piecetoLeft and "|" in destination_pieceBelow: pass
                    else: possible_moves.append(board_coordinates[new_row][new_col])
                #check upper left tile
                elif dir_row == -1 and dir_col == -1:
                    current_position = self.get_piece_at(validated_board, new_row+1, new_col+1)
                    destination_piecetoRight = self.get_piece_at(validated_board, new_row, new_col+1)
                    destination_pieceBelow = self.get_piece_at(validated_board, new_row+1, new_col)
                    if destination_piece[-1] in pieces or "O" in destination_piece: pass
                    elif "|" in destination_piece and "|" in destination_pieceBelow: pass
                    elif "_" in destination_piecetoRight and "|" in current_position: pass
                    elif "_" in destination_piece and "|" in destination_piecetoRight: pass
                    elif "_" in destination_piece and "_" in destination_piecetoRight: pass
                    else: possible_moves.append(board_coordinates[new_row][new_col])
                #check lower left tile
                elif dir_row == 1 and dir_col == -1:
                    current_position = self.get_piece_at(validated_board, new_row-1, new_col+1)
                    destination_pieceAbove = self.get_piece_at(validated_board, new_row-1, new_col)
                    destination_piecetoRight = self.get_piece_at(validated_board, new_row, new_col+1)
                    if destination_piece[-1] in pieces or "O" in destination_piece: pass
                    elif "_" in current_position and "|" in current_position: pass
                    elif "_" in current_position and "_" in destination_pieceAbove: pass
                    elif "|" in current_position and "|" in destination_piecetoRight: pass
                    elif "_" in destination_pieceAbove and "|" in destination_piecetoRight: pass
                    else: possible_moves.append(board_coordinates[new_row][new_col])
                #check lower right tile
                elif dir_row == 1 and dir_col == 1:
                    current_position = self.get_piece_at(validated_board, new_row-1, new_col-1)
                    destination_pieceAbove = self.get_piece_at(validated_board, new_row-1, new_col)
                    if destination_piece[-1] in pieces or "O" in destination_piece: pass
                    elif "|" in destination_piece and "_" in destination_pieceAbove: pass
                    elif "_" in current_position and "|" in destination_pieceAbove: pass
                    elif "_" in current_position and "_" in destination_pieceAbove: pass
                    elif "|" in destination_piece and "|" in destination_pieceAbove: pass
                    else: possible_moves.append(board_coordinates[new_row][new_col])
            else: pass
        return possible_moves

    def queen_possible_moves(self, validated_board, board_coordinates, player, from_col, from_row):
        '''
        the function checks for all possible moves the player's queens can make then returns them
        '''
        possible_moves = []
        straight_possible_moves = self.rook_possible_moves(validated_board, board_coordinates, player, from_col, from_row)
        diag_possible_moves = self.bishop_possible_moves(validated_board, board_coordinates, player, from_col, from_row)
        for i in straight_possible_moves:
            possible_moves.append(i)
        for i in diag_possible_moves:
            possible_moves.append(i)
        return possible_moves

    def knight_possible_moves(self, validated_board, board_coordinates, player, from_col, from_row):
        '''
        This function checks for all possible moves the player's knights can make and returns them.
        '''
        forward_direction = -1 if player == 0 else 1
        pieces = ["P", "R", "N", "B", "Q", "K"] if player == 0 else ["p", "r", "n", "b", "q", "k"]
        possible_moves = []
        directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

        # Loop through all possible move directions for a knight.
        for dir_col, dir_row in directions:
            new_col = from_col + (dir_col * forward_direction)
            new_row = from_row + (dir_row * forward_direction)

            # Check if the new position is a valid tile on the board.
            if self.is_valid_tile(new_row, new_col):
                destination_piece = self.get_piece_at(validated_board, new_row, new_col)
                
                # Check if the move is valid, and add it to the list of possible moves.
                if destination_piece[-1] in pieces:
                    pass
                else:
                    possible_moves.append(board_coordinates[new_row][new_col])

        return possible_moves

    def pawn_possible_moves(self, validated_board, board_coordinates, player, from_col, from_row, to_col, to_row):
        '''
        the function checks for all possible moves the player's pawns can make then returns them
        '''
        pieces = ["P", "R", "N", "B", "Q", "K"] if player == 0 else ["p", "r", "n", "b", "q", "k"]
        possible_moves = []
        self.two_step_moves = []
        if player == 0:
            directions = [(1, -1), (-1, -1)]
            forward_direction = -1  # White pawns move upward
        else:
            directions = [(1, 1), (-1, 1)]
            forward_direction = 1  # Black pawns move downward
        new_col = from_col
        new_row = from_row + forward_direction
        # Check two squares forward (only for initial move)
        if (player == 0 and from_row == 6):
            for i in range(2):
                if self.is_valid_tile(new_row, new_col) and "_" not in validated_board[new_row][new_col] and validated_board[new_row][new_col][-1] not in pieces:
                    possible_moves.append(board_coordinates[new_row-i][new_col])
                    if i == 1: self.two_step_moves.append(board_coordinates[new_row-i][new_col])
                else: break
        elif (player == 1 and from_row == 1):
            for i in range(2):
                if self.is_valid_tile(new_row, new_col) and "_" not in validated_board[new_row-i][new_col] and validated_board[new_row][new_col][-1] not in pieces:
                    possible_moves.append(board_coordinates[new_row+i][new_col])
                    if i == 1: self.two_step_moves.append(board_coordinates[new_row+i][new_col])
                else: break
        else:
            if self.is_valid_tile(new_row, new_col):
                if "." in validated_board[new_row][new_col] or "D" in validated_board[new_row][new_col] or "O" in validated_board[new_row][new_col]:
                    # Check one square forward
                    if player == 0:
                        if "_" not in validated_board[new_row][new_col]:
                            possible_moves.append(board_coordinates[new_row][new_col])
                    else: 
                        if "_" not in validated_board[new_row-1][new_col]:
                            possible_moves.append(board_coordinates[new_row][new_col])
        #add en passant 
        if board_coordinates[to_row][to_col] in self.two_step_moves: 
            self.status_line[7] = board_coordinates[to_row-forward_direction][to_col]
            self.en_passant_target = self.status_line[7]
        #Check enpassant
        if self.is_valid_tile(to_row, from_col+1):
            if board_coordinates[to_row][from_col+1] == self.status_line[7]:
                possible_moves.append(self.status_line[7])

        if self.is_valid_tile(to_row, from_col-1):
            if board_coordinates[to_row][from_col-1] == self.status_line[7]:
                possible_moves.append(self.status_line[7])

        # Check diagonal capture
        for dir_col, dir_row in directions:
            new_col = from_col + dir_col
            new_row = from_row + dir_row
            if self.is_valid_tile(new_row, new_col):
                destination_piece = self.get_piece_at(validated_board, new_row, new_col)
                if dir_row == -1 and dir_col == 1:
                    destination_piecetoLeft = self.get_piece_at(validated_board, new_row, new_col-1)
                    destination_pieceBelow = self.get_piece_at(validated_board, new_row+1, new_col)
                    if destination_piece[-1] not in pieces or destination_piece[-1] not in ["D", "M", "X", "O", "."]: 
                        if "|" in destination_piece and "_" in destination_piece: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "|" in destination_piece and "|" in destination_pieceBelow: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col]) 
                        elif "_" in destination_piece and "_" in destination_piecetoLeft: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in destination_piecetoLeft and "|" in destination_pieceBelow: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        else: possible_moves.append(board_coordinates[new_row][new_col])
                    else: pass
                #check upper left tile
                elif dir_row == -1 and dir_col == -1:
                    current_position = self.get_piece_at(validated_board, new_row+1, new_col+1)
                    destination_piecetoRight = self.get_piece_at(validated_board, new_row, new_col+1)
                    destination_pieceBelow = self.get_piece_at(validated_board, new_row+1, new_col)
                    if destination_piece[-1] not in pieces or destination_piece[-1] not in ["D", "M", "X", "O", "."]:
                        if "|" in destination_piece and "|" in destination_pieceBelow: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in destination_piecetoRight and "|" in current_position: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in destination_piece and "|" in destination_piecetoRight: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in destination_piece and "_" in destination_piecetoRight: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        else: possible_moves.append(board_coordinates[new_row][new_col])
                    else: pass
                #check lower left tile
                elif dir_row == 1 and dir_col == -1:
                    current_position = self.get_piece_at(validated_board, new_row-1, new_col+1)
                    destination_pieceAbove = self.get_piece_at(validated_board, new_row-1, new_col)
                    destination_piecetoRight = self.get_piece_at(validated_board, new_row, new_col+1)
                    if destination_piece[-1] not in pieces or destination_piece[-1] not in ["D", "M", "X", "O", "."]:
                        if "_" in current_position and "|" in current_position: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in current_position and "_" in destination_pieceAbove: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "|" in current_position and "|" in destination_piecetoRight: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in destination_pieceAbove and "|" in destination_piecetoRight: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        else: possible_moves.append(board_coordinates[new_row][new_col])
                    else: pass
                #check lower right tile
                elif dir_row == 1 and dir_col == 1:
                    current_position = self.get_piece_at(validated_board, new_row-1, new_col-1)
                    destination_pieceAbove = self.get_piece_at(validated_board, new_row-1, new_col)
                    if destination_piece[-1] not in pieces or destination_piece[-1] not in ["D", "M", "X", "O", "."]:
                        if "|" in destination_piece and "_" in destination_pieceAbove: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in current_position and "|" in destination_pieceAbove: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in current_position and "_" in destination_pieceAbove: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "|" in destination_piece and "|" in destination_pieceAbove: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        else: possible_moves.append(board_coordinates[new_row][new_col])
                    else:
                        pass
        #check if pawn is jumping onto a trap
        if ("D" in validated_board[to_row][to_col] or "O" in validated_board[to_row][to_col]) and board_coordinates[to_row][to_col] in self.two_step_moves:
            self.status_line[7] = "-"
            self.en_passant_target = self.status_line[7]
        return possible_moves

    def rook_possible_moves(self, validated_board, board_coordinates, player, from_col, from_row):
        '''
        the function checks for all possible moves the player's rooks can make then returns them
        '''
        pieces = ["P", "R", "N", "B", "Q", "K"] if player == 0 else ["p", "r", "n", "b", "q", "k"]
        possible_moves = []
        #check upwards
        rowup = from_row
        column = from_col
        while rowup > 0:
            rowup -= 1
            if self.is_valid_tile(rowup, column):
                destination_piece = self.get_piece_at(validated_board, rowup, column)
                if "_" in destination_piece: break
                elif destination_piece[-1] in pieces: break
                else: 
                    if destination_piece[-1] not in pieces and destination_piece[-1] != "." and destination_piece[-1] != "O":
                        possible_moves.append(board_coordinates[rowup][column])
                        break
                    else: possible_moves.append(board_coordinates[rowup][column]) 
        #check downwards
        rowdown = from_row
        column = from_col
        while rowdown < 7:
            rowdown += 1
            if self.is_valid_tile(rowdown, column):
                current_position = self.get_piece_at(validated_board, rowdown-1, column)
                destination_piece = self.get_piece_at(validated_board, rowdown, column)
                if "_" in current_position: break
                elif destination_piece[-1] in pieces: 
                    break  
                else: 
                    if destination_piece[-1] not in pieces and destination_piece[-1] != "." and destination_piece[-1] != "O":
                        possible_moves.append(board_coordinates[rowdown][column])
                        break
                    else: possible_moves.append(board_coordinates[rowdown][column])
        #check right
        row = from_row
        columnRight = from_col
        while columnRight < 7:
            columnRight += 1
            if self.is_valid_tile(row, columnRight):
                destination_piece = self.get_piece_at(validated_board, row, columnRight)
                if "|" in destination_piece: break
                elif destination_piece[-1] in pieces: break
                else: 
                    if destination_piece[-1] not in pieces and destination_piece[-1] != "." and destination_piece[-1] != "O":
                        possible_moves.append(board_coordinates[row][columnRight])
                        break
                    else: possible_moves.append(board_coordinates[row][columnRight])
        #check left
        row = from_row
        columnLeft = from_col
        while columnLeft > 0:
            columnLeft -= 1
            if self.is_valid_tile(row, columnLeft):
                current_position = self.get_piece_at(validated_board, row, columnLeft+1)
                destination_piece = self.get_piece_at(validated_board, row, columnLeft)
                if "|" in current_position: break
                elif destination_piece[-1] in pieces: break
                else: 
                    if destination_piece[-1] not in pieces and destination_piece[-1] != "." and destination_piece[-1] != "O":
                        possible_moves.append(board_coordinates[row][columnLeft])
                        break
                    else: possible_moves.append(board_coordinates[row][columnLeft])
        return possible_moves

    def bishop_possible_moves(self, validated_board, board_coordinates, player, from_col, from_row):
        '''
        the function checks for all possible moves the player's bishops can make then returns them
        '''
        pieces = ["P", "R", "N", "B", "Q", "K"] if player == 0 else ["p", "r", "n", "b", "q", "k"]
        possible_moves = []
        #check downright
        rowdown = from_row
        columnRight = from_col
        while rowdown < 7 and columnRight < 7:
            rowdown += 1
            columnRight += 1
            if self.is_valid_tile(rowdown, columnRight):
                destination_piece = self.get_piece_at(validated_board, rowdown, columnRight)
                current_position = self.get_piece_at(validated_board, rowdown-1, columnRight-1)
                destination_pieceabove = self.get_piece_at(validated_board, rowdown-1, columnRight)
                if destination_piece[-1] in pieces: break
                elif "|" in destination_piece  and "_" in destination_pieceabove: break
                elif "|" in destination_piece and "|" in  destination_pieceabove: break 
                elif "_" in current_position and "_" in destination_pieceabove: break
                elif "_" in current_position and "|" in destination_pieceabove: break
                else: 
                    if destination_piece[-1] not in pieces and destination_piece[-1] != "." and destination_piece[-1] != "O":
                        possible_moves.append(board_coordinates[rowdown][columnRight])
                        break
                    else: possible_moves.append(board_coordinates[rowdown][columnRight])
        #check downleft
        rowdown = from_row
        columnLeft = from_col
        while rowdown < 7 and columnLeft > 0:
            rowdown += 1
            columnLeft -= 1
            if self.is_valid_tile(rowdown, columnLeft):
                current_position = self.get_piece_at(validated_board, rowdown-1, columnLeft+1)
                destination_piece = self.get_piece_at(validated_board, rowdown, columnLeft)
                destination_piecetoRight = self.get_piece_at(validated_board, rowdown, columnLeft+1)
                destination_pieceabove = self.get_piece_at(validated_board, rowdown-1, columnLeft)
                if destination_piece[-1] in pieces: break
                elif "|" in current_position and "|" in destination_piecetoRight: break
                elif "_" in current_position and "|" in current_position: break
                elif "_" in destination_pieceabove and "|" in destination_piecetoRight: break
                elif "_" in current_position and "_" in  destination_pieceabove: break
                else: 
                    if destination_piece[-1] not in pieces and destination_piece[-1] != "." and destination_piece[-1] != "O":
                        possible_moves.append(board_coordinates[rowdown][columnLeft])
                        break
                    else: possible_moves.append(board_coordinates[rowdown][columnLeft])
        #check upright
        rowup = from_row
        columnRight = from_col
        while rowup > 0 and columnRight < 7:
            rowup -= 1
            columnRight += 1
            if self.is_valid_tile(rowup, columnRight):
                destination_piece = self.get_piece_at(validated_board, rowup, columnRight)
                destination_piecebelow = self.get_piece_at(validated_board, rowup+1, columnRight)
                destination_piecetoLeft = self.get_piece_at(validated_board, rowup, columnRight-1)
                if destination_piece[-1] in pieces: break
                elif "_" in destination_piece and "_" in destination_piecetoLeft: break
                elif "|" in destination_piecebelow and "_" in destination_piecetoLeft: break
                elif "|" in destination_piece and "|" in destination_piecebelow: break
                elif "|" in destination_piece and "_" in destination_piece: break
                else: 
                    if destination_piece[-1] not in pieces and destination_piece[-1] != "." and destination_piece[-1] != "O":
                        possible_moves.append(board_coordinates[rowup][columnRight])
                        break
                    else: possible_moves.append(board_coordinates[rowup][columnRight])
        #check upleft
        rowup = from_row
        columnLeft = from_col
        while rowup > 0 and columnLeft > 0:
            rowup -= 1
            columnLeft -= 1
            if self.is_valid_tile(rowup, columnLeft):
                current_position = self.get_piece_at(validated_board, rowup+1, columnLeft+1)
                destination_piecetoRight = self.get_piece_at(validated_board, rowup, columnLeft+1)
                destination_piece = self.get_piece_at(validated_board, rowup, columnLeft)
                if destination_piece[-1] in pieces: break
                elif "_" in destination_piece and "|" in destination_piecetoRight: break
                elif "_" in destination_piece and "_" in destination_piecetoRight: break
                elif "|" in current_position and "|" in destination_piecetoRight: break
                elif "|" in current_position and "_" in destination_piecetoRight: break
                else: 
                    if destination_piece[-1] not in pieces and destination_piece[-1] != "." and destination_piece[-1] != "O":
                        possible_moves.append(board_coordinates[rowup][columnLeft])
                        break
                    else: possible_moves.append(board_coordinates[rowup][columnLeft])
        return possible_moves

    def gui_pawn_moves(self, validated_board, board_coordinates, player, from_col, from_row):
        '''
        the function checks for all possible moves the player's pawns can make then returns them
        '''
        pieces = ["P", "R", "N", "B", "Q", "K"] if player == 1 else ["p", "r", "n", "b", "q", "k"]
        possible_moves = []
        two_step_moves = []
        if player == 0:
            directions = [(1, -1), (-1, -1)]
            forward_direction = -1  # White pawns move upward
        else:
            directions = [(1, 1), (-1, 1)]
            forward_direction = 1  # Black pawns move downward
        new_col = from_col
        new_row = from_row + forward_direction
        # Check two squares forward (only for initial move)
        if (player == 0 and from_row == 6):
            for i in range(2):
                if self.is_valid_tile(new_row+(i*forward_direction), new_col) and "_" not in validated_board[new_row+(i*forward_direction)][new_col] and validated_board[new_row+(i*forward_direction)][new_col][-1] not in ["P", "R", "N", "B", "Q", "K"] and validated_board[new_row+(i*forward_direction)][new_col][-1] not in pieces:
                    possible_moves.append(board_coordinates[new_row-i][new_col])
                    if i == 1: two_step_moves.append(board_coordinates[new_row-i][new_col])
                else: break
        elif (player == 1 and from_row == 1):
            for i in range(2):
                if self.is_valid_tile(new_row+(i*forward_direction), new_col) and "_" not in validated_board[new_row-i+(i*forward_direction)][new_col] and validated_board[new_row+(i*forward_direction)][new_col][-1] not in ["p", "r", "n", "b", "q", "k"] and validated_board[new_row+(i*forward_direction)][new_col][-1] not in pieces:
                    possible_moves.append(board_coordinates[new_row+i][new_col])
                    if i == 1: two_step_moves.append(board_coordinates[new_row+i][new_col])
                else: break
        else:
            if self.is_valid_tile(new_row, new_col):
                if "." in validated_board[new_row][new_col] or "D" in validated_board[new_row][new_col] or "O" in validated_board[new_row][new_col]:
                    # Check one square forward
                    if player == 0:
                        if "_" not in validated_board[new_row][new_col]:
                            possible_moves.append(board_coordinates[new_row][new_col])
                    else: 
                        if "_" not in validated_board[new_row-1][new_col]:
                            possible_moves.append(board_coordinates[new_row][new_col])
        # Check diagonal capture
        for dir_col, dir_row in directions:
            new_col = from_col + dir_col
            new_row = from_row + dir_row
            if self.is_valid_tile(new_row, new_col):
                destination_piece = self.get_piece_at(validated_board, new_row, new_col)
                if dir_row == -1 and dir_col == 1:
                    destination_piecetoLeft = self.get_piece_at(validated_board, new_row, new_col-1)
                    destination_pieceBelow = self.get_piece_at(validated_board, new_row+1, new_col)
                    if destination_piece[-1] in pieces or board_coordinates[new_row][new_col] == self.status_line[7]:
                        if "|" in destination_piece and "_" in destination_piece: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "|" in destination_piece and "|" in destination_pieceBelow: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col]) 
                        elif "_" in destination_piece and "_" in destination_piecetoLeft: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in destination_piecetoLeft and "|" in destination_pieceBelow: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        else: possible_moves.append(board_coordinates[new_row][new_col])
                    else: pass
                #check upper left tile
                elif dir_row == -1 and dir_col == -1:
                    current_position = self.get_piece_at(validated_board, new_row+1, new_col+1)
                    destination_piecetoRight = self.get_piece_at(validated_board, new_row, new_col+1)
                    destination_pieceBelow = self.get_piece_at(validated_board, new_row+1, new_col)
                    if destination_piece[-1] in pieces or board_coordinates[new_row][new_col] == self.status_line[7]:
                        if "|" in destination_piece and "|" in destination_pieceBelow: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in destination_piecetoRight and "|" in current_position: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in destination_piece and "|" in destination_piecetoRight: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in destination_piece and "_" in destination_piecetoRight: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        else: possible_moves.append(board_coordinates[new_row][new_col])
                    else: pass
                #check lower left tile
                elif dir_row == 1 and dir_col == -1:
                    current_position = self.get_piece_at(validated_board, new_row-1, new_col+1)
                    destination_pieceAbove = self.get_piece_at(validated_board, new_row-1, new_col)
                    destination_piecetoRight = self.get_piece_at(validated_board, new_row, new_col+1)
                    if destination_piece[-1] in pieces or board_coordinates[new_row][new_col] == self.status_line[7]:
                        if "_" in current_position and "|" in current_position: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in current_position and "_" in destination_pieceAbove: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "|" in current_position and "|" in destination_piecetoRight: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in destination_pieceAbove and "|" in destination_piecetoRight: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        else: possible_moves.append(board_coordinates[new_row][new_col])
                    else: pass
                #check lower right tile
                elif dir_row == 1 and dir_col == 1:
                    current_position = self.get_piece_at(validated_board, new_row-1, new_col-1)
                    destination_pieceAbove = self.get_piece_at(validated_board, new_row-1, new_col)
                    if destination_piece[-1] in pieces or board_coordinates[new_row][new_col] == self.status_line[7]:
                        if "|" in destination_piece and "_" in destination_pieceAbove: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in current_position and "|" in destination_pieceAbove: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "_" in current_position and "_" in destination_pieceAbove: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        elif "|" in destination_piece and "|" in destination_pieceAbove: 
                            if self.board_coordinates[new_row][new_col] in possible_moves: 
                                possible_moves.remove(self.board_coordinates[new_row][new_col])
                        else: possible_moves.append(board_coordinates[new_row][new_col])
                    else:
                        pass
        return possible_moves

    def obstacle_possible_moves(self, piece, board_coordinates):
        possible_moves = []
        if piece == "M":
            for row in range(3, 5):
                for col in range(8):
                    possible_moves.append(board_coordinates[row][col])
        else: 
            for row in range(2, 6):
                for col in range(8):
                    possible_moves.append(board_coordinates[row][col])
        return possible_moves

    def calculate_all_moves(self, validated_board, board_coordinates, player):
        '''
        this functions calculates all possible moves a player can make and returns it. its mainly used in-conjunction with the in_in_check function
        '''
        pieces = ["P", "R", "N", "B", "Q", "K"] if player == 0 else ["p", "r", "n", "b", "q", "k"]
        possible_moves = []
        to_col = 0
        to_row = 0
        for row in range(8):
            for col in range(8):
                if pieces[0] in validated_board[row][col]:
                    pawn_possible_attack = self.pawn_possible_moves(validated_board, board_coordinates, player, col, row, to_col, to_row)
                    for possible_check in pawn_possible_attack:
                        if possible_check not in possible_moves: possible_moves.append(possible_check)
                elif pieces[1] in validated_board[row][col]:
                    rook_possible_attack = self.rook_possible_moves(validated_board, board_coordinates, player, col, row)
                    for possible_check in rook_possible_attack:
                        if possible_check not in possible_moves: possible_moves.append(possible_check)
                elif pieces[2] in validated_board[row][col]:
                    knight_possible_attack = self.knight_possible_moves(validated_board, board_coordinates, player, col, row)
                    for possible_check in knight_possible_attack:
                        if possible_check not in possible_moves: possible_moves.append(possible_check)
                elif pieces[3] in validated_board[row][col]:
                    bishop_possible_attack = self.bishop_possible_moves(validated_board, board_coordinates, player, col, row)
                    for possible_check in bishop_possible_attack:
                        if possible_check not in possible_moves: possible_moves.append(possible_check)
                elif pieces[4] in validated_board[row][col]:
                    queen_possible_attack = self.queen_possible_moves(validated_board, board_coordinates, player, col, row)
                    for possible_check in queen_possible_attack:
                        if possible_check not in possible_moves: possible_moves.append(possible_check)
                elif pieces[5] in validated_board[row][col]:
                    king_possible_checks = self.king_possible_moves(validated_board, board_coordinates, player, col, row)
                    for possible_check in king_possible_checks:
                        if possible_check not in possible_moves: possible_moves.append(possible_check)
                else: pass
        return possible_moves
    