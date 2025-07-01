import os
import sys
import stddraw
import stdarray
import copy
from color import Color
from picture import Picture
from moves import Moves
from helpful import Helpful

class Gui(Helpful):
    
    def __init__(self):
        self.WALL_COLOR = stddraw.RED
        self.TRAPDOOR_COLOR = stddraw.BLACK
        self.tile1 = Color(141, 145, 141)
        self.tile2 = Color(37, 56, 60)
        self.pen_rad = 2.0
        self.highlighted_squares = []
        self.TILE_POSITIONS = []
        self.CANVAS_HEIGHT = 1000
        self.CANVAS_WIDTH = 1300
        self.BOARD_SIZE = 850
        self.TILE_SIZE = 100
        self.MID_TILE = 50
        self.TO_MID = 150
        self.ADJUST = 25
        self.PIECES = ["R", "N", "B", "Q", "K", "P", "r", "n", "b", "q", "k", "p"]
        self.tile_names_to_positions = {}
        stddraw.setCanvasSize(self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.read_pics()
        
    def get_mouse_input(self, status_line, move_log, board_log, halfmove):
        '''
        this function handles getting the mouse input and determining the moves. It does this by checking where the clicks are and sending that command to the game class
        '''
        self.moves = Moves(status_line)
        board_index = len(board_log)
        self.status_line = status_line
        player = 0 if self.status_line[0] == "w" else 1
        pieces = ["P", "R", "N", "B", "Q", "K"] if player == 0 else ["p", "r", "n", "b", "q", "k"]
        destination_sel = False
        possible_moves = []
        piece = ''
        while not destination_sel:
            #waits till the mouse is clicked
            while not stddraw.mousePressed():
                stddraw.show(100)
                if stddraw.mousePressed():
                    player = 0 if self.status_line[0] == "w" else 1
                    castling_moves = []
                    if len(self.highlighted_squares) != 0:
                        self.highlighted_squares = self.clear_highlights(self.highlighted_squares)
                        stddraw.clear()
                        self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                    x, y = stddraw.mouseX(), stddraw.mouseY()
                    if x < 50 or x > 813 and y < 75 or y > 875: 
                        
                        stddraw.clear()
                        self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                        starting_row = int((y-950) // self.TILE_SIZE)  # Calculate the clicked row
                        starting_col = int((x-814) // 53.3)  # Calculate the clicked column
                        #check if its home 
                        if starting_row == 0 and starting_col == 0: return "Home"
                        #check if its undo
                        if starting_row == 0 and starting_col == 1: return "Undo"
                        #check if its redo 
                        if starting_row == 0 and starting_col == 2: return "Redo"
                        #check if its walls 
                        if starting_row == 0 and starting_col == 3: 
                            if int(self.status_line[int(player)+1])> 0:
                                piece = self.wall_options(self.CHESSBOARD, self.status_line)
                                if piece == None: 
                                    stddraw.clear()
                                    self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                                    pass
                                else: break
                        #check if its a mine
                        if starting_row == 0 and starting_col == 4: 
                            if self.is_init_status(self.CHESSBOARD, self.status_line, halfmove):
                                piece = "M"
                                possible_moves = self.moves.obstacle_possible_moves(piece, self.board_coordinates)
                                for move in possible_moves:
                                    x, y = self.tile_names_to_positions[move]
                                    self.highlighted_squares.append((y, x))
                                self.print_possible_moves(possible_moves)
                                break
                        #check if its door
                        if starting_row == 0 and starting_col == 5: 
                            if self.is_init_status(self.CHESSBOARD, self.status_line, halfmove):
                                piece = "D"
                                possible_moves = self.moves.obstacle_possible_moves(piece, self.board_coordinates)
                                for move in possible_moves:
                                    x, y = self.tile_names_to_positions[move]
                                    self.highlighted_squares.append((y, x))
                                self.print_possible_moves(possible_moves)
                                break
                        #check if its the game log
                        if starting_row == 0 and starting_col == 6: 
                            choice = self.move_log_options()
                            #if choice is to view then we print the move log to screen
                            if choice == "View":
                                self.move_log_area()
                                self.print_moves(move_log[0:board_index-1])
                            #if choice is to print then we pprint to an output file
                            elif choice == "Print":
                                return choice
                            elif choice == None: 
                                stddraw.clear()
                                self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                                pass
                        #check if its resign
                        if starting_row == 0 and starting_col == 7: return "resign"
                        #check if its the draw
                        if starting_row == 0 and starting_col == 8: 
                            if halfmove > 100: 
                                self.write_comment("player" + ' ' + str(player+1) + " has claimed a draw", self.CHESSBOARD, self.status_line)
                                stddraw.picture(self.menu, 650, 500)
                                stddraw.setPenColor(stddraw.WHITE)
                                stddraw.setFontSize(50)
                                stddraw.text((1300/ 3) + 220, 790, "GGs, Draw")
                                stddraw.show(1000)
                                sys.exit()
                            else:
                                choice = self.draw_game(self.CHESSBOARD, self.status_line)
                                if choice == "yes": 
                                    self.write_comment("player" + ' ' + str(2 - player) + " has acccepted", self.CHESSBOARD, self.status_line)
                                    stddraw.picture(self.menu, 650, 500)
                                    stddraw.setPenColor(stddraw.WHITE)
                                    stddraw.setFontSize(50)
                                    stddraw.text((1300/ 3) + 220, 790, "GGs, Draw")
                                    stddraw.show(1000)
                                    sys.exit()
                                if choice == "no":
                                    self.write_comment("player" + ' ' + str(2 - player) + " has rejected", self.CHESSBOARD, self.status_line)
                    
                    else:
                        #check which piece was selected
                        stddraw.clear()
                        self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                        starting_row = 7 - int((y-75) // self.TILE_SIZE)  # Calculate the clicked row
                        starting_col = int((x-50) // self.TILE_SIZE)  # Calculate the clicked column
                        #get the selected piece
                        piece = self.moves.get_piece_at(self.CHESSBOARD, starting_row, starting_col)
                        if piece != None:
                            if piece[-1] == ".": 
                                if len(self.highlighted_squares) != 0: self.highlighted_squares = self.clear_highlights(self.highlighted_squares)
                            #if its a king, calculate his moves and display it on the board
                            elif piece[-1] == "K" or piece[-1] == "k":
                                if piece[-1] in pieces:
                                    possible_moves = self.moves.king_possible_moves(self.CHESSBOARD, self.board_coordinates, player, starting_col, starting_row)
                                    if not self.is_in_check(self.CHESSBOARD, self.board_coordinates, player):
                                        castling_moves = self.get_castling_moves(self.status_line, player, self.CHESSBOARD)
                                    for move in castling_moves:
                                        if move not in possible_moves: possible_moves.append(move)
                                    possible_moves = self.move(possible_moves, player, starting_row, starting_col)
                                    break
                            elif piece[-1] == "Q" or piece[-1] == "q":
                                #if its a queen, calculate her moves and display it on the board
                                if piece[-1] in pieces:
                                    possible_moves = self.moves.queen_possible_moves(self.CHESSBOARD, self.board_coordinates, player,starting_col, starting_row)
                                    possible_moves = self.move(possible_moves, player, starting_row, starting_col)
                                    break
                            elif piece[-1] == "N" or piece[-1] == "n":
                                #if its a knight, calculate his moves and display it on the board
                                if piece[-1] in pieces:
                                    possible_moves = self.moves.knight_possible_moves(self.CHESSBOARD, self.board_coordinates, player, starting_col, starting_row)
                                    possible_moves = self.move(possible_moves, player, starting_row, starting_col)
                                    break
                            elif piece[-1] == "R" or piece[-1] == "r":
                                #if its a rook, calculate his moves and display it on the board
                                if piece[-1] in pieces:
                                    possible_moves = self.moves.rook_possible_moves(self.CHESSBOARD, self.board_coordinates, player, starting_col, starting_row)
                                    possible_moves = self.move(possible_moves, player, starting_row, starting_col)
                                    break
                            elif piece[-1] == "B" or piece[-1] == "b":
                                #if its a bishop, calculate his moves and display it on the board
                                if piece[-1] in pieces:
                                    possible_moves = self.moves.bishop_possible_moves(self.CHESSBOARD, self.board_coordinates, player, starting_col, starting_row)
                                    possible_moves = self.move(possible_moves, player, starting_row, starting_col)
                                    break
                            elif piece[-1] == "P" or piece[-1] == "p":
                                #if its a pawn, calculate his moves and display it on the board
                                if piece[-1] in pieces:
                                    possible_moves = self.moves.gui_pawn_moves(self.CHESSBOARD, self.board_coordinates, player, starting_col, starting_row)
                                    possible_moves = self.move(possible_moves, player, starting_row, starting_col)
                                    break
            
            while not stddraw.mousePressed():
                stddraw.show(100)
                if piece == None: break
                if stddraw.mousePressed():
                    x, y = stddraw.mouseX(), stddraw.mouseY()
                    if x < 50 or x > 850 or y < 75 or y > 875: 
                        stddraw.clear()
                        self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                        break
                    else:
                        ending_row = 7 - int((y-75) // self.TILE_SIZE)  # Calculate the clicked row
                        ending_col = int((x-50) // self.TILE_SIZE)  # Calculate the clicked column
                        #if he is moving then break and return move, else keep waiting for move
                        if len(piece) > 0:
                            if piece[-1] in pieces:
                                #check if its a promotion move
                                if piece[-1] == "P" and ending_row == 0 and self.board_coordinates[ending_row][ending_col] in possible_moves:
                                    self.highlighted_squares = self.clear_highlights(self.highlighted_squares)
                                    stddraw.clear()
                                    self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                                    #show promo options and return promo move
                                    promotion = self.show_promotion(player, ending_col, ending_row)
                                    return self.board_coordinates[starting_row][starting_col] + "-" + self.board_coordinates[ending_row][ending_col] + "=" + promotion
                                if piece[-1] == "p" and ending_row == 7 and self.board_coordinates[ending_row][ending_col] in possible_moves:
                                    self.highlighted_squares = self.clear_highlights(self.highlighted_squares)
                                    stddraw.clear()
                                    self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                                    #show promo options and return promo move
                                    promotion = self.show_promotion(player, ending_col, ending_row)
                                    return self.board_coordinates[starting_row][starting_col] + "-" + self.board_coordinates[ending_row][ending_col] + "=" + promotion
                            #check if its a castling move
                            if self.board_coordinates[ending_row][ending_col] in castling_moves: 
                                if self.board_coordinates[ending_row][ending_col] in ["g1", "g8"]: return "0-0"
                                else: return "0-0-0"
                            #check if its a wall
                            if piece == "|" and ending_col != 0 or piece == "_" and ending_row != 7:
                                return piece + self.board_coordinates[ending_row][ending_col]
                            #check if its a mine or trapdoor
                            if piece == "M" and 3 <= ending_row <= 4 or piece == "D" and 2 <= ending_row <= 5:
                                return piece + self.board_coordinates[ending_row][ending_col]
                            #check if its a normal move
                            if self.board_coordinates[ending_row][ending_col] in possible_moves:
                                final_move = self.board_coordinates[starting_row][starting_col] + "-" + self.board_coordinates[ending_row][ending_col]
                                self.highlighted_squares = self.clear_highlights(self.highlighted_squares)
                                return final_move
                        
                        self.highlighted_squares = self.clear_highlights(self.highlighted_squares)
                        stddraw.clear()
                        self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                        break

    def create_board(self, board, status_line, automation):
        '''
        Thhis function creates the board and initializes a few other functions like read pics()
        '''
        self.automation = automation#this checks whether its an autonatic game (getting input from a file)
        #now we draw the canvas and set the backgound image
        stddraw.filledRectangle(0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        stddraw.setXscale(0, self.CANVAS_WIDTH)
        stddraw.setYscale(0, self.CANVAS_HEIGHT)
        #we check which player turn and that will decide the colour of the chessboard
        if status_line[0] == "w": stddraw.setPenColor(stddraw.WHITE)
        else: stddraw.setPenColor(stddraw.BLACK)
        #initialize the images we going to use
        self.read_pics()
        stddraw.picture(self.background, self.CANVAS_WIDTH/ 2, self.CANVAS_HEIGHT/2)
        stddraw.filledSquare(450, 475, 440)
        #now we draw the chessboard
        self.draw_boarders(status_line)
        self.CHESSBOARD = board
        self.status_line = status_line
        TILE_POSITIONS = self.draw_chessboard()
        tile_locations = stdarray.create2D(8, 8, '')
        self.board_coordinates = stdarray.create2D(8, 8, '')
        col = 0
        for i in range(8):
            for j in range(8):
                self.board_coordinates[i][j] = self.int_to_char(j).lower() + str(8-i)
                tile_locations[j][i] = TILE_POSITIONS[col]
                col += 1
        for row in range(8):
            for col in range(8): self.tile_names_to_positions[self.board_coordinates[7-row][col]] = tile_locations[row][col]
        #we draw the comment box and place the pieces in the board as well as the castling availability
        self.comment_area()
        self.place_pieces(self.CHESSBOARD)
        self.castling_availability()
        if status_line[7] != "-":
            x, y = self.tile_names_to_positions[status_line[7]]
            stddraw.picture(self.en_passant, x, y)
        #display halfmoves
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(self.BOARD_SIZE+ 245, 195, str(status_line[-1]))
        if automation:
            stddraw.show(100)

    def draw_chessboard(self):
        '''
        This function draws the chessboard using colours defined in the initializer
        '''
        tile_positions = []
        for row in range(1, 9):
            for col in range(1, 9):
                if (row + col) % 2 == 0: stddraw.setPenColor(self.tile2)
                else: stddraw.setPenColor(self.tile1)
                stddraw.filledSquare(self.TILE_SIZE*col, self.TILE_SIZE*row +25, self.MID_TILE-2)
                tile_positions.append((self.TILE_SIZE*row, self.TILE_SIZE*col + 25))
        return tile_positions

    def draw_boarders(self, status_line):
        '''
        This function draws the outer part of the chessboard
        '''
        stddraw.setFontSize(18)
        stddraw.setFontFamily('Serif')
        #choose color based on which player's turn it is
        if status_line[0] == "w": stddraw.setPenColor(stddraw.BLACK)
        else: stddraw.setPenColor(stddraw.WHITE)
        stddraw.line(self.MID_TILE-40, self.MID_TILE-16, self.BOARD_SIZE+40, self.MID_TILE-16)
        stddraw.line(self.MID_TILE-40, self.MID_TILE-16, self.MID_TILE-40, self.BOARD_SIZE+65)
        stddraw.line(self.BOARD_SIZE+40, self.MID_TILE-16, self.BOARD_SIZE+40, self.BOARD_SIZE+65)
        stddraw.line(self.MID_TILE-40, self.BOARD_SIZE+65, self.BOARD_SIZE+40, self.BOARD_SIZE+65)
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
        column = self.TILE_SIZE
        row = self.MID_TILE/2
        for i in range(1, 9):
            stddraw.text(column*i, row+25, letters[i-1])
            stddraw.text(column*i, row+self.BOARD_SIZE+25, letters[i-1])
        column = self.MID_TILE/2
        row = self.TILE_SIZE
        for i in range(1, 9):
            stddraw.text(column, row*i +25, numbers[i-1])
            stddraw.text(column+self.BOARD_SIZE, row*i +25, numbers[i-1])

    def print_buttons(self):
        '''
        this function prints the buttons in the top right of the screen as well the halfmove clock ontop of the comment box
        '''
        buttons = [self.home, self.undo, self.redo, self.wall, self.mine, self.trap, self.move_log, self.resign, self.draw]
        for i in range(9): stddraw.picture(buttons[i],  self.BOARD_SIZE - 10  + i*53, self.BOARD_SIZE+120)
        stddraw.picture(self.clock,  self.BOARD_SIZE+ 245, 195)
    
    def comment_area(self):
        '''
        This function draws the comment box in the bottom right of the screen
        '''
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.filledRectangle(self.BOARD_SIZE + self.TILE_SIZE-28, 35, 350, 100)
        stddraw.setPenColor(stddraw.GRAY)
        stddraw.filledRectangle(self.BOARD_SIZE + self.TILE_SIZE-28, 135, 350, 40)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.setPenRadius(1.5)
        stddraw.line(self.BOARD_SIZE + self.TILE_SIZE-28, 35, self.BOARD_SIZE + self.TILE_SIZE-28, 175)
        stddraw.line(self.BOARD_SIZE + self.TILE_SIZE-28, 175, self.BOARD_SIZE + self.TILE_SIZE-27+350, 175)
        stddraw.setFontSize(20)
        stddraw.text(self.BOARD_SIZE + self.TILE_SIZE-28 + 175, 155, "Comments")

    def write_comment(self, msg, board, status_line):
        '''
        This function writes any comments to the comment box
        '''
        stddraw.clear()
        self.create_board(board, status_line, self.automation)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.filledRectangle(self.BOARD_SIZE + self.TILE_SIZE-28, 35, 350, 100)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.setFontSize(30)
        stddraw.text(self.BOARD_SIZE + self.TILE_SIZE-28 + 175, 85, msg + "!")
        stddraw.show(800)

    def move_log_options(self):
        '''
        This function displays 2 move log options: Print and View and returns the user's choice
        '''
        stddraw.setPenColor(self.tile2)
        stddraw.filledSquare(1055, 885, 50)
        stddraw.filledSquare(1185, 885, 50)
        stddraw.setPenColor(self.tile1)
        stddraw.filledSquare(1050, 880, 50)
        stddraw.filledSquare(1180, 880, 50)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.setPenRadius((self.pen_rad))
        stddraw.picture(self.view, 1050, 880)
        stddraw.picture(self.printer, 1180, 880)
        while not stddraw.mousePressed():
            stddraw.show(100)
            if stddraw.mousePressed():
                x, y = stddraw.mouseX(), stddraw.mouseY()
                if 1000 < x < 1100 and 830 < y < 930:
                    stddraw.clear()
                    self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                    return "View"
                elif 1130 < x < 1230 and 830 < y < 930:
                    stddraw.clear()
                    self.create_board(self.CHESSBOARD, self.status_line, self.automation)
                    return "Print"
                else: return None

    def move_log_area(self):
        '''
        this function displays the viewing move log area
        '''
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.filledRectangle(self.BOARD_SIZE + self.TILE_SIZE-28, 225, 350, 650)
        stddraw.setPenColor(stddraw.GRAY)
        stddraw.filledRectangle(self.BOARD_SIZE + self.TILE_SIZE-28, 835, 350, 40)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.setPenRadius(1.5)
        stddraw.line(self.BOARD_SIZE + self.TILE_SIZE-28, 225, self.BOARD_SIZE + self.TILE_SIZE-28, 875)
        stddraw.line(self.BOARD_SIZE + self.TILE_SIZE-28, 875, self.BOARD_SIZE + self.TILE_SIZE-27+350, 875)
        stddraw.setFontSize(20)
        stddraw.text(self.BOARD_SIZE + self.TILE_SIZE-28 + 175, 855, "Move Log")

    def move(self, possible_moves, player, starting_row, starting_col):
        '''
        This function takes in possible moves, scans to see if it put the player's king in check the adds the remaining possible moves to the hihglighting variable
        and then returns the new possible moves
        '''
        possible_moves = self.check_pot_check(possible_moves, self.CHESSBOARD, self.board_coordinates, player, starting_row, starting_col)
        for move in possible_moves:
            x, y = self.tile_names_to_positions[move]
            self.highlighted_squares.append((y, x))
        self.print_possible_moves(possible_moves)
        return possible_moves

    def print_moves(self, move_log):
        '''
        This function prints the moves to the move log if the player wishes to see it
        '''
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.setFontSize(17)
        col = 0
        row = 0
        if len(move_log) > 0:
            for move in range(len(move_log)):
                if move_log[move][0] in ["M", "D"]:
                    pass
                else:
                    stddraw.text((self.BOARD_SIZE + self.TILE_SIZE + 7) + (col*55), (825) - (row*20), move_log[move]+ ',' )
                col+=1
                if col > 5: 
                    col = 0
                    row += 1
        else: pass

    def place_pieces(self, board):
        '''
        This function loops throught the board, reads in the piece and places its corresponding ppicture onto the graphical interface
        '''
        stddraw.setFontSize(70)
        stddraw.setFontFamily('Serif')
        stddraw.setPenRadius(self.pen_rad)
        Row = 8
        for row in range(8):
            Row -= 1
            for col in range(8):
                stddraw.setPenColor(self.WALL_COLOR)
                #If its 1 piece being read in
                if len(board[Row][col]) == 1:
                    #if its a wall the draw the corresponding lines
                    if "|" in board[Row][col]:
                        stddraw.line((self.MID_TILE+(col*self.TILE_SIZE)), (self.TO_MID+(row*self.TILE_SIZE)) + self.ADJUST, (self.MID_TILE+(col*self.TILE_SIZE)), ((self.TO_MID+self.TILE_SIZE)+(row*self.TILE_SIZE)) + self.ADJUST)
                    elif "_" in board[Row][col]:
                        stddraw.line((self.MID_TILE+(col*self.TILE_SIZE)), (self.TO_MID-(row*self.TILE_SIZE)) + self.ADJUST, (self.TO_MID+(col*self.TILE_SIZE)), (self.TO_MID-(row*self.TILE_SIZE)) + self.ADJUST)
                    #If its a trapdoor then draw its picture
                    elif "O" in board[Row][col]: stddraw.picture(self.open, (self.TILE_SIZE+(col*self.TILE_SIZE)), (self.TILE_SIZE+(row*self.TILE_SIZE)) + self.ADJUST)
                    elif "." in board[Row][col]: pass
                    else:
                        #if its a piece then draw its picture
                        piece = self.return_image(board[Row][col][-1])
                        if piece == ".": pass
                        else: stddraw.picture(piece, (self.TILE_SIZE+(col*self.TILE_SIZE)), (self.TILE_SIZE+(row*self.TILE_SIZE)) + self.ADJUST)
        #The same is done for the rest of the function
                elif len(board[Row][col]) == 2:
                    if "|" in board[Row][col]:
                        stddraw.line((self.MID_TILE+(col*self.TILE_SIZE)), (self.MID_TILE+(row*self.TILE_SIZE)) + self.ADJUST, (self.MID_TILE+(col*self.TILE_SIZE)), (self.TO_MID+(row*self.TILE_SIZE)) + self.ADJUST)
                        if "_" in board[row][col]:
                            stddraw.line((self.MID_TILE+(col*self.TILE_SIZE)), (self.TO_MID+(row*self.TILE_SIZE)) + self.ADJUST, (self.TO_MID+(col*self.TILE_SIZE)), (self.TO_MID+(row*self.TILE_SIZE)) + self.ADJUST)
                        elif "O" in board[Row][col]: stddraw.picture(self.open, (self.TILE_SIZE+(col*self.TILE_SIZE)), (self.TILE_SIZE+(row*self.TILE_SIZE)) + self.ADJUST)
                        elif "." in board[Row][col]: pass
                        else:
                            piece = self.return_image(board[Row][col][-1])
                            if piece == ".": pass
                            else: stddraw.picture(piece, (self.TILE_SIZE+(col*self.TILE_SIZE)), (self.TILE_SIZE+(row*self.TILE_SIZE)) + self.ADJUST)
                    else:
                        tile = [char for char in board[Row][col]]
                        stddraw.line((self.MID_TILE+(col*self.TILE_SIZE)), (self.MID_TILE+(row*self.TILE_SIZE)) + self.ADJUST, (self.TO_MID+(col*self.TILE_SIZE)), (self.MID_TILE+(row*self.TILE_SIZE)) + self.ADJUST)
                        if "|" in board[Row][col]:
                            stddraw.line((self.MID_TILE+(col*self.TILE_SIZE)), (self.TO_MID+(row*self.TILE_SIZE)) + self.ADJUST, (self.MID_TILE+(col*self.TILE_SIZE)), ((self.TO_MID+self.TILE_SIZE)+(row*self.TILE_SIZE)) + self.ADJUST)
                        elif "O" in board[Row][col]: stddraw.picture(self.open, (self.TILE_SIZE+(col*self.TILE_SIZE)), (self.TILE_SIZE+(row*self.TILE_SIZE)) + self.ADJUST)
                        elif "." in board[Row][col]: pass
                        elif tile[-1] in self.PIECES:
                            piece = self.return_image(board[Row][col][-1])
                            if piece == ".": pass
                            else:stddraw.picture(piece, (self.TILE_SIZE+(col*self.TILE_SIZE)), (self.TILE_SIZE+(row*self.TILE_SIZE)) + self.ADJUST)
                        else: pass
                else:
                    tile = [char for char in board[Row][col]]
                    stddraw.line((self.MID_TILE+(col*self.TILE_SIZE)), (self.MID_TILE+(row*self.TILE_SIZE)) + self.ADJUST, (self.MID_TILE+(col*self.TILE_SIZE)), (self.TO_MID+(row*self.TILE_SIZE)) + self.ADJUST)
                    stddraw.line((self.MID_TILE+(col*self.TILE_SIZE)), (self.MID_TILE+(row*self.TILE_SIZE)) + self.ADJUST, (self.TO_MID+(col*self.TILE_SIZE)), (self.MID_TILE+(row*self.TILE_SIZE)) + self.ADJUST)
                    if "." in board[Row][col]: pass
                    elif "O" in board[Row][col]: stddraw.picture(self.open, (self.TILE_SIZE+(col*self.TILE_SIZE)), (self.TILE_SIZE+(row*self.TILE_SIZE)) + self.ADJUST)
                    elif tile[-1] in self.PIECES:
                        piece = self.return_image(board[Row][col][-1])
                        if piece == ".": pass
                        else:stddraw.picture(piece, (self.TILE_SIZE+(col*self.TILE_SIZE)), (self.TILE_SIZE+(row*self.TILE_SIZE)) + self.ADJUST)
                    else: pass
                        
    def print_possible_moves(self, possible_moves):
        '''
        This function highlights the possible moves
        '''
        for move in possible_moves:
            x, y = self.tile_names_to_positions[move]
            stddraw.setPenColor(stddraw.WHITE)
            stddraw.filledCircle(x, y, 20)

    def clear_highlights(self, highlighted_squares):
        '''
        This function clears the hightlighted moves
        '''
        for square in highlighted_squares:
            # Clear the highlight by drawing the square with the original color
            row, col = square
            starting_row = (int((row-75) // self.TILE_SIZE))  # Calculate the clicked row
            starting_col = int((col-50) // self.TILE_SIZE)  # Calculate the clicked column
            if starting_row in [0, 2, 4, 6] and starting_col in [0, 2, 4, 6] or starting_row == starting_col or starting_row in [1, 3, 5, 7] and starting_col in [1, 3, 5, 7]:
                stddraw.setPenColor(self.tile2)
            if starting_row in [0, 2, 4, 6] and starting_col in [1, 3, 5, 7] or starting_col in [0, 2, 4, 6] and starting_row in [1, 3, 5, 7]:
                stddraw.setPenColor(self.tile1)
            stddraw.filledSquare(col, row, self.MID_TILE)

        # After clearing, remove all highlighted squares from the original list
        highlighted_squares = []
        return highlighted_squares

    def explosion(self, tiles):
        '''
        this function shows the explosion
        '''
        for tile in tiles:
            x, y = self.tile_names_to_positions[tile]
            stddraw.setPenColor(stddraw.RED)
            stddraw.filledSquare(x, y, 50)
            stddraw.picture(self.exploded, x, y)
        stddraw.show(300)

    def falling(self, tile):
        '''
        This function shows falling through the trapdoor
        '''
        x, y = self.tile_names_to_positions[tile]
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.filledCircle(x, y, 45)
        stddraw.picture(self.Falling, x, y)
        stddraw.show(300)

    def wall_options(self, board, status_line):
        '''
        This function displays the wall options once the player clicks on the wall icon and returns the choice or removes the options from the screen if the choice is None
        '''
        stddraw.setPenColor(self.tile2)
        stddraw.filledSquare(1055, 885, 50)
        stddraw.filledSquare(1185, 885, 50)
        stddraw.setPenColor(self.tile1)
        stddraw.filledSquare(1050, 880, 50)
        stddraw.filledSquare(1180, 880, 50)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.setPenRadius((self.pen_rad))
        stddraw.picture(self.v_wall, 1050, 880)
        stddraw.picture(self.s_wall, 1180, 880)
        while not stddraw.mousePressed():
            stddraw.show(100)
            if stddraw.mousePressed():
                x, y = stddraw.mouseX(), stddraw.mouseY()
                if 1000 < x < 1100 and 830 < y < 930:
                    stddraw.clear()
                    self.create_board(board, status_line, self.automation)
                    return "|"
                elif 1130 < x < 1230 and 830 < y < 930:
                    stddraw.clear()
                    self.create_board(board, status_line, self.automation)
                    return "_"
                else: return None

    def show_promotion(self, player, x, y):
        '''
        This function displays the promotion options once a pawn reaches the other side of the board
        '''
        pieces = [self.white_queen, self.white_bishop, self.white_rook, self.white_knight] if player == 0 else [self.black_queen, self.black_bishop, self.black_rook, self.black_knight]
        letters = ["Q", "B", "R", "N"] if player == 0 else ["q", "b", "r", "n"]
        ending_rows = [0, 1, 2, 3] if player == 0 else [7, 6, 5, 4]
        stddraw.setPenColor(stddraw.BOOK_LIGHT_BLUE)
        if player == 0:
            #Draw squares
            stddraw.square(x+100 + (x*99), y+825, 48)
            stddraw.square(x+100 + (x*99), y+725, 48)
            stddraw.square(x+100 + (x*99), y+625, 48)
            stddraw.square(x+100 + (x*99), y+525, 48)
            #draw pictures in the squares
            stddraw.picture(pieces[0], x+100 + (x*99), y+825)
            stddraw.picture(pieces[1], x+100 + (x*99), y+725)
            stddraw.picture(pieces[2], x+100 + (x*99), y+625)
            stddraw.picture(pieces[3], x+100 + (x*99), y+525)
        else:
            stddraw.square(x+100 + (x*99), y+119, 48)
            stddraw.square(x+100 + (x*99), y+219, 48)
            stddraw.square(x+100 + (x*99), y+319, 48)
            stddraw.square(x+100 + (x*99), y+419, 48)
            stddraw.picture(pieces[0], x+100 + (x*99), y+119)
            stddraw.picture(pieces[1], x+100 + (x*99), y+219)
            stddraw.picture(pieces[2], x+100 + (x*99), y+319)
            stddraw.picture(pieces[3], x+100 + (x*99), y+419)
        while not stddraw.mousePressed():
            stddraw.show(100)
            if stddraw.mousePressed(): 
                x1, y1 = stddraw.mouseX(), stddraw.mouseY()
                ending_row = 7 - int((y1-75) // self.TILE_SIZE)  # Calculate the clicked row
                ending_col = int((x1-50) // self.TILE_SIZE)  # Calculate the clicked column
                if ending_row in ending_rows and ending_col == x: return letters[abs((7*player) - ending_row)]
                else: pass

    def read_pics(self):
        '''
        This functions creates all the instance variables for the images being used in the game
        '''
        self.view = Picture(os.path.join("./assets_gui/", "view.png"))
        self.home = Picture(os.path.join("./assets_gui/", "home.png"))
        self.redo = Picture(os.path.join("./assets_gui/", "redo.png"))
        self.undo = Picture(os.path.join("./assets_gui/", "undo.png"))
        self.wall = Picture(os.path.join("./assets_gui/", "wall.png"))
        self.mine = Picture(os.path.join("./assets_gui/", "mine.png"))
        self.trap = Picture(os.path.join("./assets_gui/", "trap.png"))
        self.open = Picture(os.path.join("./assets_gui/", "open.png"))
        self.menu = Picture(os.path.join("./assets_gui/", "menu.jpg"))
        self.draw = Picture(os.path.join("./assets_gui/", "draw.png"))
        self.clock = Picture(os.path.join("./assets_gui/", "clock.png"))
        self.resign = Picture(os.path.join("./assets_gui/", "surrender.png"))
        self.s_wall = Picture(os.path.join("./assets_gui/", "southwall.png"))
        self.v_wall = Picture(os.path.join("./assets_gui/", "verticalwall.png"))
        self.printer = Picture(os.path.join("./assets_gui/", "printer.png"))
        self.Falling = Picture(os.path.join("./assets_gui/", "falling_icon.png"))
        self.move_log = Picture(os.path.join("./assets_gui/", "move_log.png"))
        self.exploded = Picture(os.path.join("./assets_gui/", "mine_explodes.png"))
        self.en_passant = Picture(os.path.join("./assets_gui/", "en passant.png"))
        self.background = Picture(os.path.join("./assets_gui/", "background.png"))
        
        self.white_king = Picture(os.path.join("./assets_gui/", "wking.png"))
        self.white_rook = Picture(os.path.join("./assets_gui/", "wrook.png"))
        self.white_pawn = Picture(os.path.join("./assets_gui/", "wpawn.png"))
        self.white_queen = Picture(os.path.join("./assets_gui/", "wqueen.png"))
        self.white_bishop = Picture(os.path.join("./assets_gui/", "wbishop.png"))
        self.white_knight = Picture(os.path.join("./assets_gui/", "wknight.png"))
        
        self.black_king = Picture(os.path.join("./assets_gui/", "bking.png"))
        self.black_rook = Picture(os.path.join("./assets_gui/", "brook.png"))
        self.black_pawn = Picture(os.path.join("./assets_gui/", "bpawn.png"))
        self.black_queen = Picture(os.path.join("./assets_gui/", "bqueen.png"))
        self.black_bishop = Picture(os.path.join("./assets_gui/", "bbishop.png"))
        self.black_knight = Picture(os.path.join("./assets_gui/", "bknight.png"))
        
    def return_image(self, piece):
        '''
        This function returns the image of the corresponding piece
        '''
        piece_to_image = {
            "K": self.white_king,
            "k": self.black_king,
            "Q": self.white_queen,
            "q": self.black_queen,
            "N": self.white_knight,
            "n": self.black_knight,
            "B": self.white_bishop,
            "b": self.black_bishop,
            "R": self.white_rook,
            "r": self.black_rook,
            "P": self.white_pawn,
            "p": self.black_pawn,
            "O": self.open,
            "M": ".",
            "D": ".",
            "X": "."
        }
        return piece_to_image.get(piece, None)  # Returns None if piece is not found in the dictionary

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
    
    def check_pot_check(self, possible_moves, validated_board, board_coordinates, player, from_row, from_col):
        '''
        This function checks if the move being made potentially put the king in check
        '''
        valid_moves = []
        for move in possible_moves:
            pos_row, pos_col = self.chess_coordinates_to_index(move)
            #Create a temporary copy of the board
            temp_board = [row[:] for row in validated_board]
            #loop through the moves on the temporary board and check if it puts king in check
            temp_board[pos_row][pos_col], temp_board[from_row][from_col] = temp_board[from_row][from_col], '.'
            if not self.is_in_check(temp_board, board_coordinates, player): valid_moves.append(move)
        return valid_moves
    
    def castling_availability(self):
        '''
        This functions draws the castling availablity in th corners of the board
        '''
        stddraw.setPenRadius(self.pen_rad/2)
        stddraw.setFontSize(35)
        if self.status_line[0] == "w":stddraw.setPenColor(stddraw.BLACK)
        else: stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontFamily('Serif')
        stddraw.text(25, 50, str(self.status_line[4]))
        stddraw.text(875, 50, str(self.status_line[3]))
        stddraw.text(25, 903, str(self.status_line[6]))
        stddraw.text(875, 903, str(self.status_line[5]))
        self.print_buttons()

    def can_castle(self, status_line, player, validated_board):
        '''
        This function checks if the players can castle based off the status line
        '''
        kingside_castle = False
        queenside_castle = False
        king_row = 7 if player == 0 else 0
        king_col = 4
        target_col_kingside = 6 
        target_col_queenside = 2 
        if player == 0:
            if status_line[3] == "+": kingside_castle = self.check_castling_path(validated_board, king_row, king_col, target_col_kingside)
            if status_line[4] == "+": queenside_castle = self.check_castling_path(validated_board, king_row, king_col, target_col_queenside)
        elif player == 1:
            if status_line[5] == "+": kingside_castle = self.check_castling_path(validated_board, king_row, king_col, target_col_kingside)
            if status_line[6] == "+": queenside_castle = self.check_castling_path(validated_board, king_row, king_col, target_col_queenside)
        return kingside_castle, queenside_castle

    def check_castling_path(self, validated_board, king_row, king_col, target_col):
        '''
        This function loops through the corresponding castling path and checks if there are obstacles or pieces in the way
        '''
        if target_col < king_col: distance = abs(king_col - target_col)+1
        else: distance = abs(king_col - target_col)
        for i in range(1, distance):
            col = min(king_col, target_col-1) + i
            if "|" in validated_board[king_row][col] or validated_board[king_row][col][-1] in ["P", "R", "N", "B", "Q", "K", "O", "p", "r", "n", "b", "q", "k"]:
                return False
        return True

    def get_castling_moves(self, status_line, player, validated_board):
        '''
        This function returns the castling moves if they re valid
        '''
        kingside_castle, queenside_castle = self.can_castle(status_line, player, validated_board)
        castling_moves = []
        if kingside_castle: castling_moves.append("g1" if player == 0 else "g8")
        if queenside_castle: castling_moves.append("c1" if player == 0 else "c8")
        return castling_moves
    
    def menu_screen(self):
        '''
        This function creates the menu screen and returns for the player's game mode choice
        '''
        self.menu = Picture(os.path.join("./assets_gui/", "menu.jpg"))
        stddraw.picture(self.menu, 650, 500)
        stddraw.setFontFamily('Serif')
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(650, 900, ' "To avoid losing a piece, many a person has lost the game." ')
        stddraw.text(1300/3, 790, "Classic")
        stddraw.text((1300/ 3) + 220, 790, "Custom")
        stddraw.text(880, 790, "Automated")
        while True:
            stddraw.show(100)
            if stddraw.mousePressed():
                x, y = stddraw.mouseX(), stddraw.mouseY()
                if 385 < x < 485 and 775 < y < 805:
                    return "classic"
                elif 600 < x < 705 and 775 < y < 805:
                    custom = self.custom_choice()
                    return custom
                elif 830 < x < 935 and 775 < y < 805:
                    return "tutorial"
    
    def custom_choice(self):
        '''
        If the player chooses to use a custom board they are given the choice of loading a board and creating a board
        '''
        stddraw.picture(self.menu, 650, 500)
        stddraw.text(1300/3, 790, "create board")
        stddraw.text(880, 790, "load board")
        while True:
            stddraw.show(100)
            if stddraw.mousePressed():
                x, y = stddraw.mouseX(), stddraw.mouseY()
                if 346 < x < 522 and 775 < y < 805:
                    return "create board"
                elif 801 < x < 958 and 775 < y < 805:
                    return "load board"

    def custom_board(self, board):
        '''
        If the player chooses to create a board this function creates a "custom board desiging screen
        '''
        pieces = [self.white_king, self.white_queen, self.white_rook, self.white_bishop, self.white_knight, self.white_pawn, self.black_king, self.black_queen, self.black_rook, self.black_bishop, self.black_knight, self.black_pawn]
        stddraw.setPenColor(stddraw.LIGHT_GRAY)
        stddraw.filledRectangle(0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        stddraw.setXscale(0, self.CANVAS_WIDTH)
        stddraw.setYscale(0, self.CANVAS_HEIGHT)
        self.read_pics()
        stddraw.picture(self.background, self.CANVAS_WIDTH/ 2, self.CANVAS_HEIGHT/2)
        stddraw.filledSquare(450, 475, 440)
        stddraw.setPenColor(stddraw.GRAY)
        #Draw the outer chessboard and the done and delete buttons
        self.draw_boarders("w 3 3 + + + + - 0")
        stddraw.setPenColor(stddraw.GRAY)
        stddraw.filledRectangle(self.BOARD_SIZE + self.TILE_SIZE + 75, 100, 100, 40)
        stddraw.filledRectangle(self.BOARD_SIZE + self.TILE_SIZE + 75, 880, 100, 40)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.setFontSize(20)
        stddraw.text(self.BOARD_SIZE + self.TILE_SIZE + 125, 120, "Done")
        stddraw.text(self.BOARD_SIZE + self.TILE_SIZE + 125, 900, "Delete")
        #draw the chessboard
        TILE_POSITIONS = self.draw_chessboard()
        self.print_buttons()
        #prints pieces on the right
        for row in range(6):
            stddraw.setPenColor(self.tile2)
            stddraw.filledSquare(1000, 825 - (row*120), 50)
            stddraw.setPenColor(self.tile1)
            stddraw.filledSquare(1150, 825 - (row*120), 50)
            stddraw.picture(pieces[row], 1000, 825 - (row*120))
            stddraw.picture(pieces[row+6], 1150, 825 - (row*120))
        self.place_pieces(board)

    def create_custom(self, board):
        '''
        This function places the pieces on the custom board and when the player clicks done returns the custom board to the game class for validation
        '''
        done = False
        wpieces = [0, 0, 0, 0, 0, 0]
        bpieces = [0, 0, 0, 0, 0, 0]
        pawn_position = [0,0]
        mine_count = 2
        door_count = 2
        while not done:
            while not stddraw.mousePressed():
                stddraw.show(100)
                piece = "."
                if stddraw.mousePressed():
                    x, y = stddraw.mouseX(), stddraw.mouseY()
                    starting_row = int((y-950) // self.TILE_SIZE)  # Calculate the clicked row
                    starting_col = int((x-814) // 53.3)  # Calculate the clicked column
                    if starting_row == 0 and starting_col == 3: 
                        piece = self.wall_options(board, "w33++++-0")
                        break
                    #check if its a mine
                    if starting_row == 0 and starting_col == 4: 
                        if mine_count > 0:
                            piece = "M"
                            mine_count -= 1
                            break
                    #check if its door
                    if starting_row == 0 and starting_col == 5: 
                        if door_count > 0:
                            piece = "D"
                            door_count -= 1
                            break
                    #check if the player selects done
                    if 1025 < x < 1125 and 100 < y < 140:
                        status_line = self.custom_status(board)
                        input_file_path = sys.argv[1]
                        with open(input_file_path, "w") as input_file:
                            for i in range(9):
                                status_line[i] = str(status_line[i])
                            for row in board:
                                input_file.write(''.join(row) + '\n')
                            input_file.write(' '.join(status_line))
                        return input_file_path
                    #check if the player wants to delete a square
                    if 880 < y < 920 and 1025 < x < 1125:
                        break
                    #Take the piece the player selects
                    if 175 < y < 275 and 950 < x < 1050: 
                        piece = "P"
                        break
                    if 175 < y < 275 and 1100 < x < 1200:
                        piece = "p"
                        break
                    if 292 < y < 392 and 950 < x < 1050:
                        piece = "N"
                        break
                    if 292 < y < 392 and 1100 < x < 1200:
                        piece = "n"
                        break
                    if 412 < y < 512 and 950 < x < 1050:
                        piece = "B"
                        break
                    if 412 < y < 512 and 1100 < x < 1200:
                        piece = "b"
                        break
                    if 532 < y < 632 and 950 < x < 1050:
                        piece = "R"
                        break
                    if 532 < y < 632 and 1100 < x < 1200:
                        piece = "r"
                        break
                    if 653 < y < 753 and 950 < x < 1050:
                        piece = "Q"
                        break
                    if 653 < y < 753 and 1100 < x < 1200:
                        piece = "q"
                        break
                    if 773 < y < 873 and 950 < x < 1050:
                        piece = "K"
                        break
                    if 773 < y < 873 and 1100 < x < 1200:
                        piece = "k"
                        break
                    
            while not stddraw.mousePressed():
                stddraw.show(100)
                if stddraw.mousePressed():
                    x, y = stddraw.mouseX(), stddraw.mouseY()
                    if x < 50 or x > 850 or y < 75 or y > 875: break
                    else:
                        if piece == "K": 
                            if self.king_count(board): pass
                            else: break

                        elif piece == "k": 
                            if self.king_count(board): pass
                            else: break

                        elif piece == "Q": 
                            if wpieces[1] < 2: wpieces[1] += 1
                            else:
                                if pawn_position[0] < 8:
                                    pawn_position[0] += 1
                                    wpieces[1] += 1
                                else: break

                        elif piece == "q": 
                            if bpieces[1] < 2: bpieces[1] += 1
                            else:
                                if pawn_position[1] < 8:
                                    pawn_position[1] += 1
                                    bpieces[1] += 1
                                else: break
                        
                        elif piece == "B": 
                            if wpieces[2] < 2: wpieces[2] += 1
                            else:
                                if pawn_position[0] < 8:
                                    pawn_position[0] += 1
                                    wpieces[2] += 1
                                else: break

                        elif piece == "b": 
                            if bpieces[2] < 2: bpieces[2] += 1
                            else:
                                if pawn_position[1] < 8:
                                    pawn_position[1] += 1
                                    bpieces[2] += 1
                                else: break
                        
                        elif piece == "N": 
                            if wpieces[3] < 2: wpieces[3] += 1
                            else:
                                if pawn_position[0] < 8:
                                    pawn_position[0] += 1
                                    wpieces[3] += 1
                                else: break
                        
                        elif piece == "n": 
                            if bpieces[3] < 2: bpieces[3] += 1
                            else:
                                if pawn_position[1] < 8:
                                    pawn_position[1] += 1
                                    bpieces[3] += 1
                                else: break
                        
                        elif piece == "R": 
                            if wpieces[4] < 2: wpieces[4] += 1
                            else:
                                if pawn_position[0] <8:
                                    pawn_position[0] += 1
                                    wpieces[4] += 1
                                else: break

                        elif piece == "r": 
                            if bpieces[4] < 2: bpieces[4] += 1
                            else:
                                if pawn_position[1] < 8:
                                    pawn_position[1] += 1
                                    bpieces[4] += 1
                                else: break

                        elif piece == "P": 
                            if pawn_position[0] < 8: pawn_position[0] += 1
                            else: break
                        
                        elif piece == "p": 
                            if pawn_position[1] < 8: pawn_position[1] += 1
                            
                        starting_row = 7 - int((y-75) // self.TILE_SIZE)  # Calculate the clicked row
                        starting_col = int((x-50) // self.TILE_SIZE)  # Calculate the clicked column
                        if piece != ".":
                            piece = self.concat_and_place(board, starting_row, starting_col, piece)
                        #Place piece on the board
                        board[starting_row][starting_col] = piece
                        self.custom_board(board)
                        break

    def custom_status(self, board):
        '''
        This function creates the custom status line
        '''
        status_line = ['w', '', '', '-', '-', '-', '-', '-', 0]
        while True:
            #choose the player
            self.write_comment("Please enter current player: ", board, status_line)
            while not stddraw.mousePressed():
                stddraw.show(100)
                self.write_comment("White or Black", board, status_line)
                if stddraw.mousePressed():
                    x, y = stddraw.mouseX(), stddraw.mouseY()
                    if 1002 < x < 1183 and 77 < y < 99:
                        if 1002 < x < 1075 and 77 < y < 99: status_line[0] = "w"
                        elif 1116 < x < 1183 and 77 < y < 99: status_line[0] = "b"
                        break
            #choose player 1 walls
            self.write_comment("Please enter player 1 walls: ", board, status_line)
            while not stddraw.mousePressed():
                stddraw.show(100)
                self.write_comment("1,  2,  3", board, status_line)
                if stddraw.mousePressed():
                    x, y = stddraw.mouseX(), stddraw.mouseY()
                    if 1045 < x < 1139 and 75 < y < 95:
                        if 1045 < x < 1060 and 75 < y < 95: status_line[1] = 1
                        elif 1084 < x < 1104 and 75 < y < 95: status_line[1] = 2
                        elif 1124 < x < 1139 and 75 < y < 95: status_line[1] = 3
                    else: status_line[1] = 0
                    break
            #chooseplayer 2 walls
            self.write_comment("Please enter player 2 walls: ", board, status_line)
            while not stddraw.mousePressed():
                stddraw.show(100)
                self.write_comment("1,  2,  3", board, status_line)
                if stddraw.mousePressed():
                    x, y = stddraw.mouseX(), stddraw.mouseY()
                    if 1045 < x < 1139 and 75 < y < 95:
                        if 1045 < x < 1060 and 75 < y < 95: status_line[2] = 1
                        elif 1084 < x < 1104 and 75 < y < 95: status_line[2] = 2
                        elif 1124 < x < 1139 and 75 < y < 95: status_line[2] = 3
                    else: status_line[2] = 0
                    break
            #choose the en passant tile
            self.write_comment("Please enter en passant tile: ", board, status_line)
            while not stddraw.mousePressed():
                stddraw.show(100)
                self.write_comment("Outside board = '-'", board, status_line)
                if stddraw.mousePressed():
                    x, y = stddraw.mouseX(), stddraw.mouseY()
                    if x < 50 or x > 813 or y < 75 or y > 875: break
                    else:
                        starting_row = 7 - int((y-75) // self.TILE_SIZE)  # Calculate the clicked row
                        starting_col = int((x-50) // self.TILE_SIZE)  # Calculate the clicked column
                        status_line[7] = self.board_coordinates[starting_row][starting_col]
                        break
            #choose the halfmove count
            self.write_comment("Enter halfmove(terminal)", board, status_line)
            status_line[8] = int(input("Please enter halfmove count: " + '\n'))
            #Scan the board to check the castling
            if board[7][4] == "K" and board[7][7] == "R": status_line[3] = "+"
            if board[7][4] == "K" and board[7][0] == "R": status_line[4] = "+"
            if board[0][4] == "k" and board[0][7] == "r": status_line[5] = "+"
            if board[0][4] == "k" and board[0][0] == "r": status_line[6] = "+"
            return status_line
    
    def draw_game(self, board, status_line):
        '''
        This function handles the draw game feature. If player 1 requests a draw player 2 will be prompted with a choice and thier choice will be returned
        '''
        player = 1 if self.status_line[0] == "w" else 2
        self.write_comment("Player " + str(player) + " has offered a draw", board, status_line)
        self.write_comment("Do you accept?", board, status_line)
        stddraw.setPenColor(stddraw.BLACK)
        self.write_comment("Yes or No?", board, status_line)
        while not stddraw.mousePressed():
            stddraw.show(100)
            if stddraw.mousePressed():
                x, y = stddraw.mouseX(), stddraw.mouseY()
                if 1025 < x < 1069 and 74 < y < 100:
                    return "yes"
                elif 1112 < x < 1148 and 74 < y < 100:
                    return "no"
                
    def animation(self, starting_col, starting_row, ending_col, ending_row, piece, chessboard):
        '''
        This function handles the animation of the movement of the pieces
        '''
        stddraw.clear()
        board = copy.deepcopy(chessboard)
        tile = [char for char in board[starting_row][starting_col]]
        tile[-1] = "."
        board[starting_row][starting_col] = tile
        self.create_board(board, self.status_line, self.automation)
        stddraw.save("screenshot.jpg")
        background = Picture("screenshot.jpg")
        piece = self.return_image(piece)
        x1 = 100 + 100*starting_col
        y1 = 825 - 100*starting_row
        x2 = 100 + 100*ending_col
        y2 = 825 - 100*ending_row
        dx = int((x2-x1)/100)
        dy = int((y2-y1)/100)
        x = x1
        y = y1
        while x != x2 or y != y2:
            stddraw.picture(background, 650, 500)
            stddraw.picture(piece, x, y)
            stddraw.show(1)
            x += dx
            y += dy