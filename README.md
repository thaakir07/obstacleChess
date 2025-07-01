##Obstacle Chess: Reinventing the Classic Game"

Obstacle Chess takes the timeless strategy game of chess and adds an exciting twist.
In Obstacle Chess, players not only maneuver their pieces to outwit their opponents but also strategically place obstacles on the board. Each player has the opportunity to deploy three walls, one mine, and one trapdoor. The thrilling part? The placements of these trapdoors and mines remain shrouded in mystery, known only to the respective players.

##Authors of the Application:
Thaakir Fernandez

## Project Timeline
- **Start Date:** July 2023
- **Completed:** November 2023

##Features:

    Choice between classic board, custom board "build your board", and CPU simulation
    
    Fully functional chessboard GUI.
    
    Standard Chess Rule and Features (King, Queen, Rook, Bishop, Knight, Pawn)
    
    Board Validation: Comprehensive validation of piece placement and game rules
    
    Highlight possible moves for selected pieces.
    
    Undo/Redo: Undoing and/or redoing of moves made
    
    Status Line: Game state tracking including castling rights and en passant
    
    Saving Game history: Saves move list to an output file for future playback or continuation

Obstacles:

    Vertical and Horizontal wall placement. 3 for each player
    
    Mines - explosive obstacles placed on ranks 4-5. 1 for each player
    
    Trap doors - Placeable on ranks 3-6. 1 for each player
    
    Combined obstacles - Mine and trap door combination

##Installation and Running:
1. Make sure you have Python installed (version 3.6 or higher).
2. Install the required stddraw and stdlib libraries if you haven't already.
3. Clone/download the project folder.
4. Run the program with input and output file arguments 
    python obstacleChess.py input.txt output.txt
    
    **AN INPUT FILE IS PROVIDED**
   
    Input Format:
        The input file should contain:
        8 lines representing the chess board (8x8 grid)
        Status line with game state information

    Board Representation:

       Standard pieces: K/k (King), Q/q (Queen), R/r (Rook), B/b (Bishop), N/n (Knight), P/p (Pawn)

        Uppercase = White pieces, Lowercase = Black pieces

        Empty squares: .

        Obstacles: M (Mine), D/O (Trap doors), X (Mine + Trap door), |/_ (Walls). (This is not needed for the board to be valid)

    Status Line Format

       [player] [white_walls] [black_walls] [castling] [en_passant] [halfmove_clock]

       player: w or b (whose turn)

        white_walls/black_walls: Number of walls (0-3 each, total max 6)

        castling: Four characters for castling availability (+ or -)

        en_passant: Target square or -

        halfmove_clock: Number of halfmoves since last capture/pawn move
        
##Game Rules
  
  Standard Chess Rules
        
        Each player must have exactly 1 king
        
        Pawns cannot be placed on ranks 1 or 8
        
        Maximum pieces per type (including promotions):
        
        Kings: 1 each
        
        Queens: 9 each (1 original + 8 promoted)
        
        Other pieces: 10 each (2 original + 8 promoted)
        
  Obstacle Rules
        
        Walls: Maximum 6 total, 3 per player
        
        Mines: Maximum 2 total, only on ranks 4-5
        
        Trap doors: Maximum 2 total, only on ranks 3-6
        
        Combined obstacles: Count toward both mine and trap door limits

##Development
    
    Key Classes:
        
        obstacleChess.py
        
        game_validation.py
        
        gui.py
        
        helpful.py
        
        moves.py
        
        chessboard.py

##Contact
Contact
For questions or issues, please open an issue on GitHub or contact [thaakir07@gmail.com].
