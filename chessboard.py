import stdarray
import sys
from helpful import Helpful

class Chessboard(Helpful):

    def __init__(self, input_file): 
        '''
        Initializes and runs the chess game. Reads input from a file, performs piece validation, and writes the board status to an output file.
        '''
        self.TOTAL_WALLS = 0 #counts the total walls of the game
        self.TOTAL_MINES = 0 #counts the total ,ines of the game
        self.TOTAL_TRAP_DOORS = 0 #counts the total trap doors of the game
        self.CHESS_TILES = 0 #counts the total chess tiles of the game
        self.TOTAL_PIECES = [0, 0] #counts the total chess pieces of the game
        self.BOARD = stdarray.create2D(8, 8, '') #creates the board 
        self.TRAP_DOORS = [0, 0] #counts the total trap doors for both players of the game
        self.MINES = [0, 0] #counts the total mines for both players of the game
        self.WALLS = [0, 0] #counts the total walls for both players of the game
        self.KINGS = [0, 0] #counts the total kings for both players of the game
        self.QUEENS = [0, 0] #counts the total queens for both players of the game
        self.BISHOPS = [0, 0] #counts the total bishops for both players of the game
        self.ROOKS = [0, 0] #counts the total rooks for both players of the game
        self.KNIGHTS = [0, 0] #counts the total knights for both players of the game
        self.PAWNS = [0, 0] #counts the total pawns for both players of the game
        self.PAWN_POSITIONS = [0, 0] #pawn positions is a variable array that keeps track of all pawns and pawn promotions
        self.LETTERS = ["K", "k", "Q", "q", "B", "b", "R", "r", "N", "n", "P", "p", ".", "X", "D", "O", "M", "|", "_"] #contains the valid inputs
        self.input_file = input_file
        self.input_file = open(self.input_file, "r")

    def validate_game(self):
        self.piece_validation(self.input_file)

    def piece_validation(self):
        '''
        this function validates all the pieces and places it in on the board then prints the status line and board
        '''
        #create the board coordinates to name tiles
        Column = 9
        board_coordinates = stdarray.create2D(8, 8, 0)
        for Row in range(8):
            Column = Column - 1
            for tile in range(8): board_coordinates[Row][tile] = self.int_to_char(tile).lower() + str(Column)
        #row and column will be used to keep track of which row and column we are in
        row = 0
        column = 0
        #start looping through the lines
        for InputFileLine in range(10000000000):
            line = self.input_file.readline()
            len_line = []
            if line.strip() == "": 
                self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
                
            if line.startswith("%"): continue
            elif line[1] == "%": continue
            #loop through the line being read in
            else:
                for letter in line:
                    if letter == " " and column == 8: 
                        self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column-1])
                    elif letter == " ": self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
                    if letter in self.LETTERS:
                        if column == 8: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column-1])
                        #check for empty tiles
                        if letter == "." and self.CHESS_TILES < 64: 
                            self.CHESS_TILES += 1
                            self.create_board(letter, row, column, board_coordinates)
                            column +=1
                        #check for kings
                        elif letter == "K" or letter == "k": 
                            self.check_kings(letter, row, column, board_coordinates)
                            column += 1
                        #check for pawns
                        elif letter == "P" or letter == "p": 
                            self.check_pawns(letter, row, column, board_coordinates)
                            column += 1
                        #check for queens
                        elif letter == "Q" or letter == "q": 
                            self.check_queens(letter, row, column, board_coordinates)
                            column += 1
                        #check for bishops
                        elif letter == "B" or letter == "b": 
                            self.check_bishops(letter, row, column,  board_coordinates)
                            column += 1
                        #check for rooks
                        elif letter == "R" or letter == "r": 
                            self.check_rooks(letter, row, column, board_coordinates)
                            column += 1
                        #check for knights
                        elif letter == "N" or letter == "n": 
                            self.check_knights(letter, row, column, board_coordinates)
                            column += 1
                        #check for mines 
                        elif letter == "M": 
                            self.check_mines(letter, row, column, board_coordinates)
                            column += 1
                        #check for trap doors
                        elif (letter == "D" or letter == "O"): 
                            self.check_trap_doors(letter, row, column, board_coordinates)
                            column += 1
                        #check for mine on trapdoor
                        elif letter == "X": 
                            self.check_X(letter, row, column, board_coordinates)
                            column += 1
                        #checks for walls
                        elif (letter == "|") or (letter == "_"):
                            for i in range(7):
                                if line[i] == "_" and line[i+1] == "|": self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][i])
                                elif (letter == "|" and column == 0) or (letter == "_"and row == 7): self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
                            if self.TOTAL_WALLS != 6: 
                                self.BOARD[row][column] += letter
                                self.TOTAL_WALLS += 1
                            else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
                        #check for invalid characters
                        else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row-1][column-1])
                #checks the length of row to see if its equal to 8
                line = line.strip()
                line_length = 0
                for Letter in line:
                    if Letter != "|" and Letter != "_": 
                        len_line.append(Letter)
                        line_length += 1
                if line_length > 8:
                    self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][7])
                elif len(len_line) < 8:
                    self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][len(len_line)])
                else: 
                    #checks for illegal piece in line
                    for char in len_line:
                        if char.isalnum()and char not in self.LETTERS or char.isdigit() or char in ["&", "$", "@", "!", "#", "?", ">", "<", "+", "%", "-"]: 
                            self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][len_line.index(char)])

                #check if we should read in status line
                statusline_read = False
                if row == 7 and column == 8:
                    self.statusline = self.input_file.readline()
                    if self.statusline.strip() == "": self.termination("ERROR: illegal board at status line")
                    read_statusline = False
                    while not read_statusline:
                        if self.statusline.startswith("%"): self.statusline = self.input_file.readline()
                        elif self.statusline.strip() == "": self.termination("ERROR: illegal board at status line")
                        else:
                            read_statusline = True
                            break
                    if read_statusline:
                        statusline_read = self.game_status()
                        #check if there is an illegal line after the status line
                        checkLastline = False
                        while not checkLastline:
                            Lastline = self.input_file.readline()
                            if Lastline.startswith("%"): continue
                            elif Lastline.strip() == "":  checkLastline = True
                            else: self.termination("ERROR: illegal board at status line")
                    #print board with status line
                    if not statusline_read: self.termination("ERROR: illegal board at status line")
                else: column = 0
                #end the chessboard loop
                if row == 7: break
                else: row += 1
    
    def check_kings(self, chess_piece, row, column, board_coordinates): 
        '''
        this function validates the king chess pieces and places it on the board
        '''
        #checks if the piece is valid to be placed on the board
        valid_piece = False
        #checks the white kings
        if chess_piece == "K" and self.KINGS[0] < 1:
            self.KINGS[0] = 1
            self.TOTAL_PIECES[0] += 1
            self.CHESS_TILES += 1
            valid_piece = True
        #check the black kings
        elif chess_piece == "k" and self.KINGS[1] < 1:
            self.KINGS[1] = 1
            self.TOTAL_PIECES[1] += 1
            self.CHESS_TILES += 1
            valid_piece = True
        if valid_piece: self.create_board(chess_piece, row, column, board_coordinates)
        else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])

    def check_pawns(self, chess_piece, row, column, board_coordinates): 
        '''
        this function validates the pawn chess pieces and places it on the board
        '''
        #checks if the white pawn can be placed on the board
        if chess_piece == "P" and self.PAWNS[0] < 8 and self.PAWN_POSITIONS[0] < 8 and (board_coordinates[row] != board_coordinates[0] and board_coordinates[row] != board_coordinates[7]):
            self.PAWNS[0] += 1
            self.TOTAL_PIECES[0] += 1
            self.PAWN_POSITIONS[0] += 1
            self.CHESS_TILES += 1
            self.create_board(chess_piece, row, column, board_coordinates)
        #   check if the black pawn can be placed on the board
        elif chess_piece == "p" and self.PAWNS[1] < 8 and self.PAWN_POSITIONS[1] < 8 and (board_coordinates[row] != board_coordinates[0] and board_coordinates[row] != board_coordinates[7]):
            self.PAWNS[1] += 1
            self.TOTAL_PIECES[1] += 1
            self.PAWN_POSITIONS[1] += 1
            self.CHESS_TILES += 1
            self.create_board(chess_piece, row, column, board_coordinates)
        else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        
    def check_queens(self, chess_piece, row, column, board_coordinates): 
        '''
        this function validates the queen chess pieces and places it on the board
        '''
        #checks if its a normal queen or promoted queen, the same will happen for the black piece
        if chess_piece == "Q" and self.QUEENS[0] < 9:
            if self.QUEENS[0] < 1:
                self.QUEENS[0] += 1
                self.TOTAL_PIECES[0] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            #if its a promoted queens it will take up a pawn position, the same will happen for the black piece
            elif self.QUEENS[0] >= 1 and self.PAWN_POSITIONS[0] < 8:
                self.QUEENS[0] += 1
                self.TOTAL_PIECES[0] += 1
                self.PAWN_POSITIONS[0] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        elif chess_piece == "q" and self.QUEENS[1] < 9:
            if self.QUEENS[1] < 1:
                self.QUEENS[1] += 1
                self.TOTAL_PIECES[1] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            elif self.QUEENS[1] >= 1 and self.PAWN_POSITIONS[1] < 8:
                self.QUEENS[1] += 1
                self.TOTAL_PIECES[1] += 1
                self.PAWN_POSITIONS[1] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
    
    def check_bishops(self, chess_piece, row, column, board_coordinates): 
        '''
        this function validates the bishop chess pieces and places it on the board
        '''
        if chess_piece == "B" and self.BISHOPS[0] < 10:
        #checks the bishop. This function works the same as the check_queen function
            if self.BISHOPS[0] < 2:
                self.BISHOPS[0] += 1
                self.TOTAL_PIECES[0] += 1
                self.CHESS_TILES += 1
                chess_piece = self.bishop_placement(row, column, chess_piece, board_coordinates)
            elif self.BISHOPS[0] >= 2 and self.PAWN_POSITIONS[0] < 8:
                self.BISHOPS[0] += 1
                self.TOTAL_PIECES[0] += 1
                self.PAWN_POSITIONS[0] += 1
                self.CHESS_TILES += 1
                chess_piece = self.bishop_placement(row, column, chess_piece, board_coordinates)
            else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        elif chess_piece == "b" and self.BISHOPS[1] < 10:
            if self.BISHOPS[1] < 2:
                self.BISHOPS[1] += 1
                self.TOTAL_PIECES[1] += 1
                self.CHESS_TILES += 1
                chess_piece = self.bishop_placement(row, column, chess_piece, board_coordinates)
            elif self.BISHOPS[1] >= 2 and self.PAWN_POSITIONS[1] < 8:
                self.BISHOPS[1] += 1
                self.TOTAL_PIECES[1] += 1
                self.PAWN_POSITIONS[1] += 1
                self.CHESS_TILES += 1
                chess_piece = self.bishop_placement(row, column, chess_piece, board_coordinates)
            else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])    

    def check_rooks(self, chess_piece, row, column, board_coordinates): 
        '''
        this function validates the rook chess pieces and places it on the board
        '''
        #checks the rooks. This function works the same as the check_queen function
        if chess_piece == "R" and self.ROOKS[0] < 10:
            if self.ROOKS[0] < 2:
                self.ROOKS[0] += 1
                self.TOTAL_PIECES[0] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            elif self.ROOKS[0] >= 2 and self.PAWN_POSITIONS[0] < 8:
                self.ROOKS[0] += 1
                self.TOTAL_PIECES[0] += 1
                self.PAWN_POSITIONS[0] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        elif chess_piece == "r" and self.ROOKS[1] < 10:
            if self.ROOKS[1] < 2:
                self.ROOKS[1] += 1
                self.TOTAL_PIECES[1] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            elif self.ROOKS[1] >= 2 and self.PAWN_POSITIONS[1] < 8:
                self.ROOKS[1] += 1
                self.TOTAL_PIECES[1] += 1
                self.PAWN_POSITIONS[1] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        
    def check_knights(self, chess_piece, row, column, board_coordinates): 
        '''
        this function validates the knight chess pieces and places it on the board
        '''
        #checks the knights. This function works the same as the check_queen function
        if chess_piece == "N" and self.KNIGHTS[0] < 10:
            if self.KNIGHTS[0] < 2:
                self.KNIGHTS[0] += 1
                self.TOTAL_PIECES[0] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            elif self.KNIGHTS[0] >= 2 and self.PAWN_POSITIONS[0] < 8:
                self.KNIGHTS[0] += 1
                self.TOTAL_PIECES[0] += 1
                self.PAWN_POSITIONS[0] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        elif chess_piece == "n" and self.KNIGHTS[1] < 10:
            if self.KNIGHTS[1] < 2:
                self.KNIGHTS[1] += 1
                self.TOTAL_PIECES[1] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            elif self.KNIGHTS[1] >= 2 and self.PAWN_POSITIONS[1] < 8:
                self.KNIGHTS[1] += 1
                self.TOTAL_PIECES[1] += 1
                self.PAWN_POSITIONS[1] += 1
                self.CHESS_TILES += 1
                self.create_board(chess_piece, row, column, board_coordinates)
            else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])

    def check_mines(self, chess_piece, row, column, board_coordinates): 
        '''
        this function validates the king obstacle pieces and places it on the board
        '''
        #checks if the mine is within the max value and that its being placed within the valid ranks
        if (chess_piece == "M" and (self.TOTAL_MINES < 2) and (row+1 >= 4 and row+1 <= 5)):
            self.TOTAL_MINES += 1
            self.CHESS_TILES += 1
            self.create_board(chess_piece, row, column, board_coordinates)
        else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
    
    def check_trap_doors(self, chess_piece, row, column, board_coordinates): 
        '''
        this function validates the trap door obstacle pieces and places it on the board
        '''
        #checks if the trapdoors is within the max value and that its being placed within the valid ranks
        if (chess_piece == "D" or chess_piece == "O") and (self.TOTAL_TRAP_DOORS < 2) and (row+1 >= 3 and row+1 <= 6) :
            self.TOTAL_TRAP_DOORS += 1
            self.CHESS_TILES += 1
            self.create_board(chess_piece, row, column, board_coordinates)
        else:self.termination("ERROR: illegal board at "+board_coordinates[row][column])

    def check_X(self, chess_piece, row, column, board_coordinates):  
        '''
        this function validates the trapdoors on top of the mines
        '''
        #checks if the mine/trapdoors is within the max value and that its being placed within the valid ranks
        if chess_piece == "X" and (self.TOTAL_TRAP_DOORS < 2) and (self.TOTAL_MINES < 2) and (row+1 >= 4 and row+1 <= 5):
            self.TOTAL_TRAP_DOORS +=1 
            self.TOTAL_MINES += 1
            self.CHESS_TILES += 1
            self.create_board(chess_piece, row, column, board_coordinates)
        else: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])

    def game_status(self):  
        '''
        this function validates the last line and tells the game that the last line has been read
        '''
        #splits the status line into an array
        statusline = self.statusline.split()
        for index in range(9):
            #checks whether its player white or player black
            if index == 0:
                if statusline[0] in ["w", "b"]: continue
                else: 
                    self.termination("ERROR: illegal board at status line")
                    return False
            #checks white walls
            if index == 1: 
                if not statusline[index].isdigit():
                    self.termination("ERROR: illegal board at status line")
                    return False
                self.TOTAL_WALLS += int(statusline[1])
                self.WALLS[0] += int(statusline[1])
                if self.TOTAL_WALLS > 6 or self.WALLS[0] > 3 or self.WALLS[0] < 0: 
                    self.termination("ERROR: illegal board at status line")
                    return False
                else: continue
            #checks black walls
            if index == 2:
                if not statusline[index].isdigit():
                    self.termination("ERROR: illegal board at status line")
                    return False
                self.TOTAL_WALLS += int(statusline[2])
                self.WALLS[1] += int(statusline[2])
                if self.TOTAL_WALLS > 6 or self.WALLS[1] > 3 or self.WALLS[1] < 0: 
                    self.termination("ERROR: illegal board at status line")
                    return False
                else: continue
            if self.TOTAL_WALLS != 6:
                self.termination("ERROR: illegal board at status line")
                return False
            #checks castline availability for both players
            if index in [3, 4, 5, 6]:
                if statusline[index] in ["+", "-"]: continue
                else: 
                    self.termination("ERROR: illegal board at status line")
                    return False
            #checks the en passant 
            if index == 7:
                if statusline[index] == "-":continue
                elif len(statusline[index]) == 1 and statusline[index] != "-": self.termination("ERROR: illegal board at status line")
                elif len(statusline[index]) > 1:
                    enpassant = statusline[index].strip()
                    if enpassant[0] in ["a", "b", "c", "d", "e", "f", "g", "h"] and int(enpassant[1]) in [1, 2, 3, 4, 5, 6, 7, 8]:
                        if len(enpassant) > 2: self.termination("ERROR: illegal board at status line")
                        else: statusline[index] = statusline[index] + statusline[index+1]
                    else: 
                        self.termination("ERROR: illegal board at status line")
                        return False
            #checks half move clock
            if len(statusline) > 9 or len(statusline) < 9: 
                self.termination("ERROR: illegal board at status line")
                return False
            else:
                if int(statusline[-1]) < 0: 
                    self.termination("ERROR: illegal board at status line")
                    return False
        return True

    def create_board(self, chess_piece, row, column, board_coordinates): 
        '''
        this funtion creates the board and places all pieces on it
        '''
        if self.CHESS_TILES > 64: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
        king_count = 0
        #place pieces on board
        self.BOARD[row][column] += chess_piece
        if row == 7 and column == 7: 
            for Row in range(8):
                for Column in range(8):
                    #checks the king count
                    letter = self.BOARD[Row][Column]
                    if len(letter) > 1:
                        for let in letter:
                            if let == "K" or let == 'k': king_count += 1
                    elif letter == "K" or letter == 'k': king_count += 1
            if king_count < 2: self.termination("ERROR: illegal board at h1")

    def bishop_placement(self, row, column, chess_piece, board_coordinates):
        '''
        this function checks if the bishop placement is correct
        '''
        B1 = ''
        B2 = ''
        b1 = ''
        b2 = ''
        #create true and false board
        TrueFalseBoard = stdarray.create2D(8, 8, False)
        even = [0, 2, 4, 6]
        for Row in range(len(TrueFalseBoard)):
            for Column in range(len(TrueFalseBoard)):
                if Row in even and Column in even: TrueFalseBoard[Row][Column] = True
                elif Row not in even and Column not in even: TrueFalseBoard[Row][Column] = True
        #place white bishop
        if chess_piece == "B":
            if TrueFalseBoard[row][column] == True: B1 = TrueFalseBoard[row][column]
            else: B2 = TrueFalseBoard[row][column]
            if B1 == False or B2 == True : self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
            else: self.create_board(chess_piece, row, column, board_coordinates)
        #place black bishop
        elif chess_piece == "b":
            if TrueFalseBoard[row][column] == True: b1 = chess_piece
            else: b2 = chess_piece
            if b1 == b2: self.termination("ERROR: illegal board at" + ' ' + board_coordinates[row][column])
            else: self.create_board(chess_piece, row, column, board_coordinates)

    def get_board(self):
        '''
        this functions returns the board and status line
        '''
        return self.BOARD, self.statusline.strip()

    def termination(self, coordinates): #
        '''
        This function terminates the game
        '''
        sys.stderr.write(coordinates)
        sys.exit() 
