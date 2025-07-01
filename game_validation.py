import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ''
import stdarray
import stddraw
import copy
from chessboard import Chessboard
from moves import Moves
from gui import Gui
from helpful import Helpful

class ChessGame(Helpful):

    def __init__(self, input_file, output_file, move_file):
        self.classic_board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        self.classic_status = "w 3 3 + + + + - 0"
        self.custom = [
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."]
        ]
        self.tutorial = False
        self.MINES = [1, 1]
        self.TRAPDOORS = [1, 1]
        if len(sys.argv) == 4:
            self.move_file = move_file
        else: self.move_file = ''
        chessboard = Chessboard(input_file)
        self.output_file = output_file
        chessboard.piece_validation()
        validated_board, status_line = chessboard.get_board()
        self.validated_board = validated_board
        status_line = status_line.strip()
        self.status_line = status_line.split(" ")
        self.moves = Moves(self.status_line)
        self.gui = Gui()
        self.tutorial = False
        self.gui.create_board(self.validated_board, self.status_line, self.tutorial)
        self.has_king_moved = [False, False]
        self.WALLS = [int(self.status_line[1]), int(self.status_line[2])]
        self.halfmove_count = int(self.status_line[-1])
        self.en_passant_target = str(self.status_line[7])
        self.total_obstacle_count = 4
        self.fen_history = []
        self.board_log = []
        
        board = copy.deepcopy(self.validated_board)
        status = copy.deepcopy(self.status_line)
        self.board_log.append((board, status))
        self.move_log = []
        Column = 9
        self.board_coordinates = stdarray.create2D(8, 8, 0)
        for Row in range(8):
            Column = Column - 1
            for tile in range(8): self.board_coordinates[Row][tile] = self.int_to_char(tile).lower() + str(Column)

    def start_game(self):
        choice = self.gui.menu_screen()
        
        if choice == "classic":
            self.validated_board = self.classic_board
            self.status_line = self.classic_status.strip()
            self.status_line = self.status_line.split(" ")
            if len(sys.argv) == 4:
                self.move_file = sys.argv[3]
                self.move_file = open(self.move_file, "r")
        
        elif choice == "create board":
            self.gui.custom_board(self.custom)
            input_file = self.gui.create_custom(self.custom)
            chessboard = Chessboard(input_file)
            chessboard.piece_validation()
            validated_board, status_line = chessboard.get_board()
            self.validated_board = validated_board
            status_line = status_line.strip()
            self.status_line = status_line.split(" ")
            if len(sys.argv) == 4:
                self.move_file = sys.argv[3]
                self.move_file = open(self.move_file, "r")

        elif choice == "load board":
            input_file = stddraw.tkFileDialog.askopenfilename()
            chessboard = Chessboard(input_file)
            chessboard.piece_validation()
            validated_board, status_line = chessboard.get_board()
            self.validated_board = validated_board
            status_line = status_line.strip()
            self.status_line = status_line.split(" ")

        elif choice == "tutorial":
            self.tutorial = True
            self.input_file = stddraw.tkFileDialog.askopenfilename()
            chessboard = Chessboard(self.input_file)
            chessboard.piece_validation()
            validated_board, status_line = chessboard.get_board()
            self.validated_board = validated_board
            status_line = status_line.strip()
            self.status_line = status_line.split(" ")
            self.move_file = stddraw.tkFileDialog.askopenfilename()
            self.move_file = open(self.move_file, "r")
            

        self.moves = Moves(self.status_line)
        self.board_log = []
        board = copy.deepcopy(self.validated_board)
        status = copy.deepcopy(self.status_line)
        self.board_log.append((board, status))
        self.halfmove_count = int(self.status_line[-1])
        self.en_passant_target = str(self.status_line[7])
        self.gui.create_board(self.validated_board, self.status_line, self.tutorial)
        self.WALLS = [int(self.status_line[1]), int(self.status_line[2])]
        self.run_game()
            
    def run_game(self):
        '''
        this functions reads the game file and runs the game. If the game file is not terminated before its done being read it prints the outcome and the board
        '''
        turn = 0
        undo_pressed = 0
        redo_pressed = 0
        while True:
            board_index = len(self.board_log)
            if self.status_line[0] == "w": 
                player = 0
                rowswap = 8
            else: 
                player = 1
                rowswap = -8
            forward_dir = 1 if player == 0 else -1
            self.status_line[-1] = self.halfmove_count
            #if we select automatic mode then this is used to read in moves
            if self.tutorial:
                move = self.move_file.readline()
                if move.startswith("%"): continue
                elif move.strip() == "": 
                    if self.check_stalemate(player, self.validated_board, self.board_coordinates):
                        self.gui.write_comment("stalemate", self.validated_board, self.status_line)
                        self.print_msg("stalemate")
                        if self.tutorial:
                            move = self.move_file.readline()
                            if move.startswith("%"): break
                            elif move.strip() != "": self.termination(move)
                        else: 
                            self.gui.get_mouse_input(self.status_line, self.move_log, self.board_log[:board_index-undo_pressed], self.halfmove_count)
                    else: 
                        king_row, king_col = self.find_king(self.validated_board, player)
                        if self.is_in_check(self.validated_board, self.board_coordinates, player) and not self.can_escape_check(self.validated_board, self.board_coordinates, player, king_col, king_row):
                            self.gui.write_comment("checkmate", self.validated_board, self.status_line)
                            self.print_msg("checkmate")
                            if self.tutorial:
                                move = self.move_file.readline()
                                if move.startswith("%"): break
                                elif move.strip() != "": self.termination(move)
                            else: 
                                self.gui.get_mouse_input(self.status_line, self.move_log, self.board_log[:board_index-undo_pressed], self.halfmove_count)
                        else: pass
                    break
            #If we playing the game then this is used to read in moves
            else: move = self.gui.get_mouse_input(self.status_line, self.move_log, self.board_log[:board_index-undo_pressed], self.halfmove_count)
            #checks threefold
            if self.is_threefold_repetition(self.fen_history): 
                self.gui.write_comment("threefold repetition", self.validated_board, self.status_line)
                self.print_msg("draw due to threefold repetition")
            #If move is Home then go to latest board
            if move == "Home":
                undo_pressed = 0
                redo_pressed = 0
                self.gui.create_board(self.board_log[len(self.board_log) - 1][0], self.board_log[len(self.board_log) - 1][1], self.tutorial)
                self.validated_board = copy.deepcopy(self.board_log[len(self.board_log) - 1][0])
                self.status_line = copy.deepcopy(self.board_log[len(self.board_log) - 1][1])
            #if move is undo then display previous board
            elif move == "Undo":
                if redo_pressed > 0: redo_pressed -= 1
                undo_pressed += 1
                if len(self.board_log) - 1 - undo_pressed < 0: self.gui.write_comment("No more moves to undo", self.validated_board, self.status_line)
                else:
                    self.gui.create_board(self.board_log[len(self.board_log) - 1 - undo_pressed][0], self.board_log[len(self.board_log) - 1 - undo_pressed][1], self.tutorial)
                    self.validated_board = copy.deepcopy(self.board_log[len(self.board_log) - 1 - undo_pressed][0])
                    self.status_line = copy.deepcopy(self.board_log[len(self.board_log) - 1 - undo_pressed][1])
            #if move is redo then display next board
            elif move == "Redo":
                if redo_pressed >= len(self.board_log)-1: self.gui.write_comment("No more moves to redo", self.validated_board, self.status_line)
                else:
                    if undo_pressed > 0: undo_pressed -= 1
                    redo_pressed += 1
                    self.gui.create_board(self.board_log[len(self.board_log) - 1 - (undo_pressed+redo_pressed) + redo_pressed][0], self.board_log[len(self.board_log) - 1 - (undo_pressed+redo_pressed) + redo_pressed][1], self.tutorial)
                    self.validated_board = copy.deepcopy(self.board_log[len(self.board_log) - 1 - (undo_pressed+redo_pressed) + redo_pressed][0])
                    self.status_line = copy.deepcopy(self.board_log[len(self.board_log) - 1 - (undo_pressed+redo_pressed) + redo_pressed][1])
            #if move is print then print board to file
            elif move == "Print": 
                self.gui.write_comment("printing", self.validated_board, self.status_line)
                self.print_board(self.validated_board, self.status_line)
                self.gui.create_board(self.validated_board, self.status_line, self.tutorial)
            #if resign then resign from the game
            elif move == "resign": 
                self.resign()
            #The player wants to move a piece
            else:
                if undo_pressed > 0:
                   self.board_log = self.board_log[:-undo_pressed]
                   self.move_log = self.move_log[:-undo_pressed]
                   self.halfmove_count = int(self.board_log[len(self.board_log) - 1][1][-1])
                undo_pressed = 0
                redo_pressed = 0
                move = move.strip()
                original_move = move
                self.move_log.append(move)
                move = [char for char in move]
                #If the move he selects is kingside castling or placing an obstacle
                if len(original_move) == 3:
                    if '0' in move: 
                        if not self.has_king_moved[player] and not self.is_in_check(self.validated_board, self.board_coordinates, player):
                            self.validated_board = self.perform_castling(move, self.validated_board, player)
                        else: self.termination(original_move)
                    elif original_move == "...": 
                        self.total_obstacle_count -= 1
                        pass
                    else:
                        rowplacement, columnplacement = self.chess_coordinates_to_index(move[1]+move[2])
                        if self.is_valid_tile(rowplacement, columnplacement):
                            if turn == 0 and self.status_line[0] != "w" and self.total_obstacle_count == 4: self.termination(original_move)
                            self.validated_board, self.status_line = self.place_obstacles(move, self.validated_board, columnplacement, rowplacement, self.status_line, player)
                        else: self.termination(original_move)
                #if they move a piece
                elif len(original_move) == 5:
                    if '0' in move: 
                        if not self.has_king_moved[player]: self.validated_board = self.perform_castling(move, self.validated_board, player)
                    else:
                        from_col, from_row, to_col, to_row = self.parse_move(move, rowswap)
                        if self.is_valid_tile(from_row, from_col):
                            piece = self.get_piece_at(self.validated_board, from_row, from_col)
                            self.gui.animation(from_col, from_row, to_col, to_row, piece[-1], self.validated_board)
                            if player == 0 and piece in ["p", "r", "n", "b", "q", "k"]: self.termination(original_move)
                            elif player == 1 and piece in ["P", "R", "N", "B", "Q", "K"]: self.termination(original_move)
                            else: pass
                            
                            if piece[-1] == "K" or piece[-1] == "k":
                                possible_moves = self.moves.king_possible_moves(self.validated_board, self.board_coordinates, player, from_col, from_row)
                                possible_moves = self.check_pot_check(possible_moves, self.validated_board, self.board_coordinates, player, from_row, from_col)
                                if len(possible_moves) != 0:
                                    for king_move in possible_moves:
                                        if self.board_coordinates[to_row][to_col] not in possible_moves:self.termination(original_move)
                                        elif self.board_coordinates[to_row][to_col] != king_move: pass
                                        else: break
                                    self.halfmove_count += 1
                                    #update the board and castling
                                    self.validated_board = self.update_board(original_move, piece, possible_moves, self.board_coordinates, from_row, from_col, to_row, to_col, self.validated_board, player)
                                    self.has_king_moved[player] = True
                                    if player == 0: self.status_line[3], self.status_line[4] = "-", "-"
                                    else: self.status_line[5], self.status_line[6] = "-", "-"
                                    self.en_passant_target = None
                                    self.status_line[7] = "-"
                                    current_fen = self.get_current_fen(self.validated_board, self.status_line[0], self.status_line[3:7], self.status_line[7])
                                    self.fen_history.append(current_fen)
                                    
                            elif piece[-1] == "Q" or piece[-1] == "q":
                                possible_moves = self.moves.queen_possible_moves(self.validated_board, self.board_coordinates, player,from_col, from_row)
                                possible_moves = self.check_pot_check(possible_moves, self.validated_board, self.board_coordinates, player, from_row, from_col)
                                if len(possible_moves) != 0:
                                    for queen_move in possible_moves:
                                        if self.board_coordinates[to_row][to_col] not in possible_moves:self.termination(original_move)
                                        elif self.board_coordinates[to_row][to_col] != queen_move: pass
                                        else: break
                                    self.halfmove_count += 1
                                    self.validated_board = self.update_board(original_move, piece, possible_moves, self.board_coordinates, from_row, from_col, to_row, to_col, self.validated_board, player)
                                    self.en_passant_target = None
                                    self.status_line[7] = "-"
                                    current_fen = self.get_current_fen(self.validated_board, self.status_line[0], self.status_line[3:7], self.status_line[7])
                                    self.fen_history.append(current_fen)
                            
                            elif piece[-1] == "N" or piece[-1] == "n":
                                possible_moves = self.moves.knight_possible_moves(self.validated_board, self.board_coordinates, player, from_col, from_row)
                                possible_moves = self.check_pot_check(possible_moves, self.validated_board, self.board_coordinates, player, from_row, from_col)
                                if len(possible_moves) != 0:
                                    for knight_move in possible_moves:
                                        if self.board_coordinates[to_row][to_col] not in possible_moves:self.termination(original_move)
                                        elif self.board_coordinates[to_row][to_col] != knight_move: pass
                                        else: break
                                    self.halfmove_count += 1
                                    self.validated_board = self.update_board(original_move, piece, possible_moves, self.board_coordinates, from_row, from_col, to_row, to_col, self.validated_board, player)
                                    self.en_passant_target = None
                                    self.status_line[7] = "-"
                                    current_fen = self.get_current_fen(self.validated_board, self.status_line[0], self.status_line[3:7], self.status_line[7])
                                    self.fen_history.append(current_fen)
                                    
                            elif piece[-1] == "R" or piece[-1] == "r":
                                possible_moves = self.moves.rook_possible_moves(self.validated_board, self.board_coordinates, player, from_col, from_row)
                                possible_moves = self.check_pot_check(possible_moves, self.validated_board, self.board_coordinates, player, from_row, from_col)
                                if len(possible_moves) != 0:
                                    for rook_move in possible_moves:
                                        if self.board_coordinates[to_row][to_col] not in possible_moves:self.termination(original_move)
                                        elif self.board_coordinates[to_row][to_col] != rook_move: pass
                                        else: break
                                    self.halfmove_count += 1
                                    self.validated_board = self.update_board(original_move, piece, possible_moves, self.board_coordinates, from_row, from_col, to_row, to_col, self.validated_board, player)
                                    self.en_passant_target = None
                                    self.status_line[7] = "-"
                                    current_fen = self.get_current_fen(self.validated_board, self.status_line[0], self.status_line[3:7], self.status_line[7])
                                    self.fen_history.append(current_fen)
                                    
                            elif piece[-1] == "B" or piece[-1] == "b":
                                possible_moves = self.moves.bishop_possible_moves(self.validated_board, self.board_coordinates, player, from_col, from_row)
                                possible_moves = self.check_pot_check(possible_moves, self.validated_board, self.board_coordinates, player, from_row, from_col)
                                if len(possible_moves) != 0:
                                    for bishop_move in possible_moves:
                                        if self.board_coordinates[to_row][to_col] not in possible_moves:self.termination(original_move)
                                        elif self.board_coordinates[to_row][to_col] != bishop_move: pass
                                        else: break
                                    self.halfmove_count += 1
                                    self.validated_board = self.update_board(original_move, piece, possible_moves, self.board_coordinates, from_row, from_col, to_row, to_col, self.validated_board, player)
                                    self.en_passant_target = None
                                    self.status_line[7] = "-"
                                    current_fen = self.get_current_fen(self.validated_board, self.status_line[0], self.status_line[3:7], self.status_line[7])
                                    self.fen_history.append(current_fen)
                                    
                            elif piece[-1] == "P" or piece[-1] == "p":
                                possible_moves = self.moves.pawn_possible_moves(self.validated_board, self.board_coordinates, player, from_col, from_row, to_col, to_row)
                                possible_moves = self.check_pot_check(possible_moves, self.validated_board, self.board_coordinates, player, from_row, from_col)
                                if len(possible_moves) != 0:
                                    for pawn_move in possible_moves:
                                        if self.board_coordinates[to_row][to_col] not in possible_moves:self.termination(original_move)
                                        elif self.board_coordinates[to_row][to_col] != pawn_move: pass
                                        else: break
                                    if self.board_coordinates[to_row][to_col] == self.status_line[7]:
                                        en_passant_tile = self.concat_and_place(self.validated_board, to_row+forward_dir, to_col, ".")
                                        self.validated_board[to_row+forward_dir][to_col] = en_passant_tile
                                        self.status_line[7] = "-"
                                    if not self.tutorial:
                                        if abs(int(from_row) - int(to_row)) > 1:
                                            self.status_line[7] = self.board_coordinates[to_row + forward_dir][to_col]
                                    self.validated_board = self.update_board(original_move, piece, possible_moves, self.board_coordinates, from_row, from_col, to_row, to_col, self.validated_board, player)
                                    
                                    
                                    self.halfmove_count = 0
                                    self.fen_history = []
                            
                            else: self.termination(original_move)
                        else: self.termination(original_move)
                #if they want to perform promotion
                elif len(original_move) == 7:
                    promotion_piece = move[-1]
                    move = move[:5]
                    from_col, from_row, to_col, to_row = self.parse_move(move, rowswap)
                    if self.is_valid_tile(from_row, from_col):
                        piece = self.get_piece_at(self.validated_board, from_row, from_col)
                        self.gui.animation(from_col, from_row, to_col, to_row, piece[-1], self.validated_board)
                        self.promote_pawn(piece, original_move, self.validated_board, from_col, from_row, to_col, to_row, promotion_piece)
                        self.fen_history = []
                    else: self.termination(original_move)
                
                else: self.termination(original_move)
                #update player turn
                if self.status_line[0] == "w": self.status_line[0] = "b"
                else: self.status_line[0] = "w"
                if self.status_line[0] == "w": 
                    player = 0
                    rowswap = 8
                else: 
                    player = 1
                    rowswap = -8 
                turn += 1
                self.status_line[-1] = self.halfmove_count
                board = copy.deepcopy(self.validated_board)
                status = copy.deepcopy(self.status_line)
                self.board_log.append((board, status))
                #check fot stalemate, checkmate, halfmove count
                if self.king_count(self.validated_board): 
                    self.gui.write_comment("stalemate", self.validated_board, self.status_line)
                    self.gui.get_mouse_input(self.status_line, self.move_log, self.board_log[:board_index-undo_pressed], self.halfmove_count)
                if self.is_checkmate(self.validated_board, player, self.board_coordinates): 
                    if self.tutorial:
                        move = self.move_file.readline()
                        if move.startswith("%"): break
                        elif move.strip() != "": self.termination(move)
                    else: 
                        self.gui.get_mouse_input(self.status_line, self.move_log, self.board_log[:board_index-undo_pressed], self.halfmove_count)
                if self.halfmove_count >= 100: 
                    self.gui.write_comment("draw due to fifty moves", self.validated_board, self.status_line)
                    self.print_msg("draw due to fifty moves")
                stddraw.clear()
                self.gui.create_board(self.validated_board, self.status_line, self.tutorial)

    def place_obstacles(self, move, validated_board, column, row, status_line, player):
        '''
        when an obstacle is read in this function takes it in then places it on the board and updates the status line.
        it then returns the board and the status line
        '''
        obstacle_move = ''
        for char in move: obstacle_move += char
        if (obstacle_move[0] == "D" and self.is_init_status(validated_board, status_line, self.halfmove_count) and (3 <= row+1 <= 6)
        and self.TRAPDOORS[player] != 0 and self.total_obstacle_count != 0 and (self.WALLS[0] + self.WALLS[1] == 6) and 
        (status_line[3] == "+" and status_line[4] == "+" and status_line[5] == "+" and status_line[6] == "+" and status_line[7] == "-")):
            if "M" in  validated_board[row][column]:
                piece = self.concat_and_place(validated_board, row, column, "X")
                validated_board[row][column] = piece
            elif "." in validated_board[row][column]:
                piece = self.concat_and_place(validated_board, row, column, "D")
                validated_board[row][column] = piece
            elif "D" in validated_board[row][column]:
                piece = self.concat_and_place(validated_board, row, column, "D")
                validated_board[row][column] = piece
            elif "X" in validated_board[row][column]:
                piece = self.concat_and_place(validated_board, row, column, "X")
                validated_board[row][column] = piece
            else: self.termination(obstacle_move)
            self.TRAPDOORS[player] -= 1
            self.total_obstacle_count -= 1

        elif (obstacle_move[0] == "M" and self.is_init_status(validated_board, status_line, self.halfmove_count) and (4 <= row+1 <=  5) 
              and self.MINES[player] != 0 and self.total_obstacle_count != 0 and (self.WALLS[0] + self.WALLS[1] == 6)and 
        (status_line[3] == "+" and status_line[4] == "+" and status_line[5] == "+" and status_line[6] == "+" and status_line[7] == "-")):
            if "D" in validated_board[row][column]:
                piece = self.concat_and_place(validated_board, row, column, "X")
                validated_board[row][column] = piece
            elif "." in validated_board[row][column]:
                piece = self.concat_and_place(validated_board, row, column, "M")
                validated_board[row][column] = piece
            elif "M" in validated_board[row][column]:
                piece = self.concat_and_place(validated_board, row, column, "M")
                validated_board[row][column] = piece
            elif "X" in validated_board[row][column]:
                piece = self.concat_and_place(validated_board, row, column, "X")
                validated_board[row][column] = piece
            else: self.termination(obstacle_move)
            self.MINES[player] -= 1
            self.total_obstacle_count -= 1

        elif "|" in obstacle_move[0] and column != 0 and self.WALLS[player] > 0:
            if "|" in validated_board[row][column]: self.termination(obstacle_move)
            else: 
                validated_board[row][column] = self.concat_and_place(validated_board, row, column, "|")
                self.WALLS[player] -= 1
                self.status_line[player+1] = self.WALLS[player]
                self.halfmove_count = 0
                self.fen_history = []
                self.status_line[7] = "-"
                if row == 0 and column == 5: self.status_line[5] = "-"
                elif row == 0 and column == 4: self.status_line[6] = "-"
                elif row == 7 and column == 5: self.status_line[3] = "-"
                elif row == 7 and column == 4: self.status_line[4] = "-"
        
        elif obstacle_move[0] == "_" and row < 7 and self.WALLS[player] > 0:
            if "_" in validated_board[row][column]: self.termination(obstacle_move)
            else: 
                validated_board[row][column] = self.concat_and_place(validated_board, row, column, "_")
                self.WALLS[player] -= 1
                self.status_line[player+1] = self.WALLS[player]
                self.halfmove_count = 0
                self.fen_history = []
                self.status_line[7] = "-"
        else: self.termination(obstacle_move)
        return validated_board, self.status_line

    def update_board(self, original_move, piece, possible_moves, board_coordinates, from_row, from_col, to_row, to_col, validated_board, player):
        '''
        once a valid move is made this function updates the board. it then returns the board
        '''
        forward_dir = -1 if player == 0 else 1
        if board_coordinates[to_row][to_col] in possible_moves:
            #checks if it lands on a bomb or a trap
            if "M" in validated_board[to_row][to_col] or "X" in validated_board[to_row][to_col]:
                validated_board = self.Kaboom(validated_board, to_row, to_col, from_row, from_col)
                piece = self.concat_and_place(validated_board, from_row, from_col, ".")
                validated_board[from_row][from_col] = piece
                self.halfmove_count = 0
                self.fen_history = []
            elif validated_board[to_row][to_col] in ["D", "O"]:
                piece = self.concat_and_place(validated_board, from_row, from_col, ".")
                validated_board[from_row][from_col] = piece
                self.gui.falling(board_coordinates[to_row][to_col])
                piece = self.concat_and_place(validated_board, to_row, to_row, "O")
                validated_board[to_row][to_col] = piece
                self.halfmove_count = 0
                self.fen_history = []
                self.status_line[7] = "-"
            else: #check if its en passant
                if (piece == "P" or piece == "p") and board_coordinates[to_row][to_col] == self.en_passant_target:
                    piece = self.concat_and_place(validated_board, to_row, to_col, piece)
                    validated_board[to_row][to_col] = piece
                    piece = self.concat_and_place(validated_board, to_row-forward_dir, to_col, ".")
                    validated_board[from_row][from_col] = piece
                    self.en_passant_target = None
                    self.status_line[7] = "-"
                    self.fen_history = []
                else:
                    if "." not in validated_board[to_row][to_col]: 
                        self.halfmove_count = 0
                        self.fen_history = []
                    piece = self.concat_and_place(validated_board, to_row, to_col, piece)
                    validated_board[to_row][to_col] = piece
                    piece1 = self.concat_and_place(validated_board, from_row, from_col, ".")
                    validated_board[from_row][from_col] = piece1
                    if piece[-1] in ["P", "p"] and abs(int(from_row) - int(to_row)) == 1:
                        self.status_line[7] = "-"
        else: self.termination(original_move)
        return validated_board

    def perform_castling(self, move, validated_board, player):
        '''
        if a castling move is deemed valid this function performs the castling move, updates the status line and returns the board
        '''
        castling_move = ''
        for char in move: castling_move += char
        # Define the positions of the rooks for both players
        rook_positions = {
            0: {'kingside': (7, 7), 'queenside': (7, 0)},  # White player
            1: {'kingside': (0, 7), 'queenside': (0, 0)}   # Black player
        }
        # Determine if it's a kingside or queenside castling move
        is_kingside_castling = castling_move == "0-0"
        is_queenside_castling = castling_move == "0-0-0"
        # Determine the player's color
        is_white = player == 0
        # Determine the king's row and column
        king_row = 7 if is_white else  0
        king_col = 4
        # Determine the target column for castling
        target_col = 6 if is_kingside_castling else 2  # Corrected target columns
        # Determine the rook's row and column based on the castling type
        rook_row, rook_col = rook_positions[player]['kingside'] if is_kingside_castling else rook_positions[player]['queenside']
        # Check if the move is a valid castling move
        if player == 0:
            if is_kingside_castling:
                if self.status_line[3] == "-": self.termination(castling_move)
                else: pass
            else: 
                if self.status_line[4] == "-": self.termination(castling_move)
                else: pass
        else:
            if is_kingside_castling:
                if self.status_line[5] == "-": self.termination(castling_move)
                else: pass
            else: 
                if self.status_line[6] == "-": self.termination(castling_move)
                else: pass
        if validated_board[king_row][king_col] in ('K', 'k') and validated_board[rook_row][rook_col] in ('R', 'r'):
            # Check if there are no pieces between the king and rook
            if is_kingside_castling:
                # Check the squares between king and rook
                for i in range(1, abs(king_col - target_col)):
                    #check on the right for walls
                    if "|" in validated_board[king_row][min(king_col, target_col) + i]: self.termination(castling_move)
                    elif validated_board[king_row][min(king_col, target_col) + i] in ["P", "R", "N", "B", "Q", "K", "O", "p", "r", "n", "b", "q", "k"]:
                        self.termination(castling_move)
            else:
                for i in range(0, king_col-target_col):
                    if "|" in validated_board[king_row][min(king_col, target_col) - i]: self.termination(castling_move)
                    elif validated_board[king_row][min(king_col, target_col) - i] in ["P", "R", "N", "B", "Q", "K", "O", "p", "r", "n", "b", "q", "k"]:
                        self.termination(castling_move)
            if not any(
                validated_board[king_row][col] != '.'
                for col in range(min(king_col, target_col) + 1, max(king_col, target_col))
            ): # Update the board to perform castling
                
                self.gui.animation(king_col, king_row, target_col, king_row,'K' if is_white else 'k', validated_board)
                self.gui.animation(rook_col, rook_row, 5 if is_kingside_castling else 3, rook_row,'R' if is_white else 'r', validated_board)
                
                validated_board[king_row][king_col] = '.'
                validated_board[king_row][target_col] = 'K' if is_white else 'k'
                validated_board[rook_row][rook_col] = '.'
                validated_board[rook_row][5 if is_kingside_castling else 3] = 'R' if is_white else 'r'
                if player == 0:
                    self.status_line[3] = "-"
                    self.status_line[4] = "-"
                else: 
                    self.status_line[5] = "-"
                    self.status_line[6] = "-"
                self.halfmove_count += 1
        return validated_board

    def promote_pawn(self, piece, move, validated_board, from_col, from_row, to_col, to_row, promotion_piece):
        '''
        this functions checks if the promotion is valid and if so performs the promotion and updates the board
        '''
        if piece[-1] == "P":
            pieces = ["R", "N", "B", "Q"]
            if promotion_piece in pieces:  
                validated_board[to_row][to_col] = promotion_piece
                validated_board[from_row][from_col] = '.'
            else: self.termination(move)

        elif piece[-1] == "p":
            pieces = ["r", "n", "b", "q"]
            if promotion_piece in pieces:
                validated_board[to_row][to_col] = promotion_piece
                validated_board[from_row][from_col] = '.'
            else: self.termination(move)
        else: self.termination(move)

    def Kaboom(self, validated_board, to_row, to_col, from_row, from_col):
        '''
        this functions performs the explosion effect of a mine. it checks all 8 tiles around the mine and sees if the explosion will go there.
        once its done checking all tiles it carries out the explosion and returns the board
        '''
        tiles = []
        pieces = ["D", "O", "X", "."]
        if ("P" in validated_board[from_row][from_col] or "p" in validated_board[from_row][from_col]) and abs(from_row - to_row) == 2: self.status_line[7] = "-"
        if "M" in validated_board[to_row][to_col]: 
            piece = self.concat_and_place(validated_board, to_row, to_col, ".")
            validated_board[to_row][to_col] = piece
        if validated_board[to_row][to_col] == "X": 
            piece = self.concat_and_place(validated_board, to_row, to_col, "O")
            validated_board[to_row][to_col] = piece
        tiles.append(self.board_coordinates[to_row][to_col])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir_col, dir_row in directions:
            new_col = to_col + dir_col
            new_row = to_row + dir_row
            if self.is_valid_tile(new_row, new_col):
                destination_piece = self.get_piece_at(validated_board, new_row, new_col)
                #explode right
                if dir_col == 1 and dir_row == 0:
                    if "|" in destination_piece: pass
                    elif destination_piece[-1] in pieces: pass
                    else: 
                        piece = self.concat_and_place(validated_board, new_row, new_col, ".")
                        validated_board[new_row][new_col] = piece
                        tiles.append(self.board_coordinates[new_row][new_col])
                #explode up
                elif dir_row == -1 and dir_col == 0: 
                        if "_" in destination_piece: pass
                        elif destination_piece[-1] in pieces: pass
                        else: 
                            piece = self.concat_and_place(validated_board, new_row, new_col, ".")
                            validated_board[new_row][new_col] = piece      
                            tiles.append(self.board_coordinates[new_row][new_col])         
                #explode left
                elif dir_col == -1 and dir_row == 0:
                    current_position = self.get_piece_at(validated_board, new_row, new_col+1)
                    if "|" in current_position: pass
                    elif destination_piece[-1] in pieces:pass
                    else: 
                        piece = self.concat_and_place(validated_board, new_row, new_col, ".")
                        validated_board[new_row][new_col] = piece
                        tiles.append(self.board_coordinates[new_row][new_col])
                #explode down
                elif dir_row == 1 and dir_col == 0:
                    current_position = self.get_piece_at(validated_board, new_row-1, new_col)
                    if "_" in current_position: pass
                    elif destination_piece[-1] in pieces:pass
                    else: 
                        piece = self.concat_and_place(validated_board, new_row, new_col, ".")
                        validated_board[new_row][new_col] = piece
                        tiles.append(self.board_coordinates[new_row][new_col])
                #explode upright
                elif dir_row == -1 and dir_col == 1:
                    destination_pieceBelow = self.get_piece_at(validated_board, new_row+1, new_col)
                    destination_piecetoLeft = self.get_piece_at(validated_board, new_row, new_col-1)
                    if "|" in destination_piece and "_" in destination_piece: pass
                    elif destination_piece[-1] in pieces:pass
                    elif "|" in destination_piece and "|" in destination_pieceBelow: pass 
                    elif "_" in destination_piece and "_" in destination_piecetoLeft: pass
                    elif "_" in destination_piecetoLeft and "|" in destination_pieceBelow: pass
                    else: 
                        piece = self.concat_and_place(validated_board, new_row, new_col, ".")
                        validated_board[new_row][new_col] = piece
                        tiles.append(self.board_coordinates[new_row][new_col])
                #explode upleft
                elif dir_row == -1 and dir_col == -1:
                    current_position = self.get_piece_at(validated_board, new_row+1, new_col+1)
                    destination_piecetoRight = self.get_piece_at(validated_board, new_row, new_col+1)
                    destination_pieceBelow = self.get_piece_at(validated_board, new_row+1, new_col)
                    if "|" in destination_piece and "|" in destination_pieceBelow: pass
                    elif destination_piece[-1] in pieces:pass
                    elif "_" in destination_piecetoRight and "|" in current_position: pass
                    elif "_" in destination_piece and "|" in destination_piecetoRight: pass
                    elif "_" in destination_piece and "_" in destination_piecetoRight: pass
                    else: 
                        piece = self.concat_and_place(validated_board, new_row, new_col, ".")
                        validated_board[new_row][new_col] = piece
                        tiles.append(self.board_coordinates[new_row][new_col])
                #explode downleft
                elif dir_row == 1 and dir_col == -1:
                    current_position == self.get_piece_at(validated_board, new_row+1, new_col+1)
                    destination_pieceAbove = self.get_piece_at(validated_board, new_row-1, new_col)
                    destination_piecetoRight = self.get_piece_at(validated_board, new_row, new_col+1)
                    if "_" in current_position and "|" in current_position: pass
                    elif destination_piece[-1] in pieces:pass
                    elif "_" in current_position and "_" in destination_pieceAbove: pass
                    elif "|" in current_position and "|" in destination_piecetoRight: pass 
                    elif "_" in destination_pieceAbove and "|" in destination_piecetoRight: pass
                    else: 
                        piece = self.concat_and_place(validated_board, new_row, new_col, ".")
                        validated_board[new_row][new_col] = piece
                        tiles.append(self.board_coordinates[new_row][new_col])
                #explode downright
                elif dir_row == 1 and dir_col == 1:
                    current_position = self.get_piece_at(validated_board, new_row-1, new_col-1)
                    destination_pieceAbove = self.get_piece_at(validated_board, new_row-1, new_col)
                    if "|" in destination_piece and "_" in destination_pieceAbove: pass
                    elif destination_piece[-1] in pieces:pass
                    elif "|" in destination_piece and "|" in destination_pieceAbove: pass
                    elif "_" in current_position and "|" in destination_pieceAbove: pass
                    elif "_" in current_position and "_" in destination_pieceAbove: pass
                    else: 
                        piece = self.concat_and_place(validated_board, new_row, new_col, ".")
                        validated_board[new_row][new_col] = piece
                        tiles.append(self.board_coordinates[new_row][new_col])
        self.gui.explosion(tiles)
        return validated_board

    def get_board(self):
        return self.validated_board, self.status_line

    def print_board(self, board, status_line):
        self.output_file = sys.argv[2]
        self.move_file = sys.argv[3]
        self.move_file = open(self.move_file, "w")
        self.output_file = open(self.output_file, "w")
        self.output_file.write('\n')
        for i in range(9): status_line[i] = str(status_line[i])
        for row in board: self.output_file.write(''.join(row) + '\n')
        self.output_file.write(' '.join(status_line))
        self.output_file.write('\n')
        for row in self.move_log: self.move_file.write(''.join(row) + '\n')

    def is_checkmate(self, validated_board, player, board_coordinates):
        '''
        this functions checks if any player's king is in check and if they can escape check. if they can it prints check, if they cannot it prints checkmate
        '''
        # Find the king's position for the current player
        king_row, king_col = self.find_king(validated_board, player)
        # Check if the king is in check
        if self.is_in_check(validated_board, board_coordinates, player) and self.can_escape_check(validated_board, board_coordinates, player, king_col, king_row):
            self.gui.write_comment("check", validated_board, self.status_line)
            self.print_msg("check")
        elif self.is_in_check(validated_board, board_coordinates, player) and not self.can_escape_check(validated_board, board_coordinates, player, king_col, king_row):
            self.gui.write_comment("checkmate", validated_board, self.status_line)
            self.print_msg("checkmate")
            return True  # It's checkmate
        return False

    def is_in_check(self, validated_board, board_coordinates, player):
        '''
        this functions checks if the player's king's position is threatened by an opposing piece. if so he is in check and it returns true
        '''
        # Check if the opponent's pieces threaten the king
        opponent = self.get_opponent(player) # The opponent's player index
        king_row, king_col = self.find_king(validated_board, player)
        # Calculate potential moves for opponent's pieces
        opponent_moves = self.moves.calculate_all_moves(validated_board, board_coordinates, opponent)
        # Check if the king's position is in the list of opponent's moves
        king_position = board_coordinates[king_row][king_col]
        if king_position in opponent_moves: return True  # The king is in check
        return False

    def can_escape_check(self, validated_board, board_coordinates, player, king_col, king_row):
        '''
        this functions checks if the player's king can escape check. it does this by calculting the king's moves and creating a parallel board in which the king
        made that move. if by making the move the king is still in check it moves onto the kings next move. if the king has no moves left it calculates 
        all the other pieces that can protect the king with their moves via the same parallel board method
        '''
        pieces = ["P", "R", "N", "B", "Q", "K"] if player == 0 else ["p", "r", "n", "b", "q", "k"]
        # List of possible king moves (including castling)
        king_moves = self.moves.king_possible_moves(validated_board, board_coordinates, player, king_col, king_row)
        # Check if any of the king's possible moves gets it out of check
        for move in king_moves:
            to_row, to_col = self.chess_coordinates_to_index(move)
            # Simulate the move to see if the king is still in check
            temp_board = [row[:] for row in validated_board]
            temp_board[to_row][to_col], temp_board[king_row][king_col] = temp_board[king_row][king_col], '.'
            # Check if the king is still in check after the move
            if not self.is_in_check(temp_board, board_coordinates, player): return True  # King can escape check
        
        if int(self.status_line[player+1]) > 0:
            for row in range(8):
                for col in range(1, 8):
                    temp_board = [row[:] for row in validated_board]
                    temp_board[row][col] =  '|' + temp_board[row][col] if "|" not in temp_board[row][col] else temp_board[row][col]
                    # Check if the king is still in check after the move
                    if not self.is_in_check(temp_board, board_coordinates, player): return True  # King can escape check
            for row in range(1, 8):
                for col in range(8):
                    temp_board = [row[:] for row in validated_board]
                    temp_board[row][col] =  '_' + temp_board[row][col] if "|" not in temp_board[row][col] else "|_" + temp_board[row][col][-1]
                    # Check if the king is still in check after the move
                    if not self.is_in_check(temp_board, board_coordinates, player): return True  # King can escape check

        # Check if any other piece can block the check
        for row in range(8):
            for col in range(8):
                piece = validated_board[row][col]
                if piece == pieces[0]:
                    to_col = 0
                    to_row = 0
                    pawn_moves = self.moves.pawn_possible_moves(validated_board, board_coordinates, player, col, row, to_col, to_row)
                    for move in pawn_moves:
                        to_row, to_col = self.chess_coordinates_to_index(move)
                        # Simulate the move to see if the king is still in check
                        temp_board = [row[:] for row in validated_board]
                        temp_board[to_row][to_col], temp_board[row][col] = temp_board[row][col], '.'
                        
                        # Check if the king is still in check after the move
                        if not self.is_in_check(temp_board, board_coordinates, player): return True  # King can escape check
                        
                elif piece == pieces[1]:
                    rook_moves = self.moves.rook_possible_moves(validated_board, board_coordinates, player, col, row)
                    for move in rook_moves:
                        to_row, to_col = self.chess_coordinates_to_index(move)
                        # Simulate the move to see if the king is still in check
                        temp_board = [row[:] for row in validated_board]
                        temp_board[to_row][to_col], temp_board[row][col] = temp_board[row][col], '.'
                        
                        # Check if the king is still in check after the move
                        if not self.is_in_check(temp_board, board_coordinates, player): return True  # King can escape check
                        
                elif piece == pieces[2]:
                    knight_moves = self.moves.knight_possible_moves(validated_board, board_coordinates, player, col, row)
                    for move in knight_moves:
                        to_row, to_col = self.chess_coordinates_to_index(move)
                        # Simulate the move to see if the king is still in check
                        temp_board = [row[:] for row in validated_board]
                        temp_board[to_row][to_col], temp_board[row][col] = temp_board[row][col], '.'

                        # Check if the king is still in check after the move
                        if not self.is_in_check(temp_board, board_coordinates, player): return True  # King can escape check
                        
                elif piece == pieces[3]:
                    bishop_moves = self.moves.bishop_possible_moves(validated_board, board_coordinates, player, col, row)
                    for move in bishop_moves:
                        to_row, to_col = self.chess_coordinates_to_index(move)
                        # Simulate the move to see if the king is still in check
                        temp_board = [row[:] for row in validated_board]
                        temp_board[to_row][to_col], temp_board[row][col] = temp_board[row][col], '.'

                        # Check if the king is still in check after the move
                        if not self.is_in_check(temp_board, board_coordinates, player): return True  # King can escape check
                        
                elif piece == pieces[4]:
                    queen_moves = self.moves.queen_possible_moves(validated_board, board_coordinates, player, col, row)
                    for move in queen_moves:
                        to_row, to_col = self.chess_coordinates_to_index(move)
                        # Simulate the move to see if the king is still in check
                        temp_board = [row[:] for row in validated_board]
                        temp_board[to_row][to_col], temp_board[row][col] = temp_board[row][col], '.'

                        # Check if the king is still in check after the move
                        if not self.is_in_check(temp_board, board_coordinates, player): return True  # King can escape check
        return False  # No legal move for the king to escape check or for another piece to block check

    def check_stalemate(self, player, board, board_coordinates):
        '''
        this functions checks for stalemate
        '''
        king_row, king_col = self.find_king(board, player)
        if not self.is_in_check(board, board_coordinates, player) and not self.can_escape_check(board, board_coordinates, player, king_col, king_row): 
            return True
        if self.is_in_check(board, board_coordinates, player) and not self.can_escape_check(board, board_coordinates, player, king_col, king_row): 
            return False

    def is_threefold_repetition(self, fen_history):
        # Count occurrences of each FEN position in the history
        fen_count = {}
        for fen in fen_history:
            if fen in fen_count:fen_count[fen] += 1
            else: fen_count[fen] = 1
        # Check if any position occurs three or more times
        for count in fen_count.values():
            if count >= 3: return True
        return False

    def check_pot_check(self, possible_moves, validated_board, board_coordinates, player, from_row, from_col):
        valid_moves = []
        for move in possible_moves:
            pos_row, pos_col = self.chess_coordinates_to_index(move)
            temp_board = [row[:] for row in validated_board]
            temp_board[pos_row][pos_col], temp_board[from_row][from_col] = temp_board[from_row][from_col], '.'
            if not self.is_in_check(temp_board, board_coordinates, player):valid_moves.append(move)
        return valid_moves

    def resign(self):
        '''
        Thhis function handles the resiging feature
        '''
        player = 1 if self.status_line[0] == "w" else 2
        self.gui.write_comment("player" + ' ' + str(player) + " has resigned", self.validated_board, self.status_line)
        stddraw.picture(self.gui.menu, 650, 500)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontSize(50)
        stddraw.text((1300/ 3) + 220, 790, "GGs, player " + str(3 - player) + ' ' + "has won")
        stddraw.show(1000)
        sys.exit()