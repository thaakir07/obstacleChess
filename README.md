# Obstacle Chess: Reinventing the Classic Game

Obstacle Chess takes the timeless strategy game of chess and adds an exciting twist. In addition to maneuvering pieces to outwit opponents, players strategically place obstacles on the board. Each player can deploy three walls, one mine, and one trapdoor, with mines and trapdoors remaining hidden from the opponent, adding a thrilling element of mystery and surprise to every game.

## Author

**Thaakir Fernandez**

## Project Timeline

- **Start Date:** July 2023
- **Completed:** November 2023

## Features

### Game Modes
- **Classic Board:** Traditional chess setup with obstacles
- **Custom Board:** "Build your board" mode for custom configurations
- **CPU Simulation:** Play against computer opponent

### Chess Mechanics
- **Fully Functional GUI:** Interactive chessboard interface
- **Standard Chess Rules:** Complete implementation of all piece types (King, Queen, Rook, Bishop, Knight, Pawn)
- **Board Validation:** Comprehensive validation of piece placement and game rules
- **Move Highlighting:** Visual indication of possible moves for selected pieces
- **Undo/Redo System:** Full move history with undo and redo capabilities
- **Status Tracking:** Real-time game state including castling rights and en passant
- **Game History:** Automatic saving of move sequences to output file for replay or continuation

### Obstacle System
- **Walls:** Vertical and horizontal barriers (3 per player, 6 total maximum)
- **Mines:** Explosive obstacles placeable on ranks 4-5 (1 per player, hidden from opponent)
- **Trap Doors:** Hidden traps on ranks 3-6 (1 per player, secret placement)
- **Combined Obstacles:** Mine and trap door combinations for advanced strategy

## Installation and Setup

### Prerequisites
- Python 3.6 or higher
- Required libraries: `stddraw` and `stdlib`

### Installation Steps
1. Ensure Python is installed on your system
2. Install required libraries:
   ```
   pip install stddraw stdlib
   ```
3. Clone or download the project folder
4. Navigate to the project directory

## Usage

### Running the Game
```
python obstacleChess.py input.txt output.txt game.txt
```

**Note:** An input file is provided with the project for immediate testing. The game.txt file is optional and is only used in cases of simulation play.

### Input File Format

The input file must contain:
- **8 lines:** Representing the 8x8 chess board
- **Status line:** Game state information

#### Board Representation
- **Standard Pieces:**
  - `K/k` - King (White/Black)
  - `Q/q` - Queen (White/Black)
  - `R/r` - Rook (White/Black)
  - `B/b` - Bishop (White/Black)
  - `N/n` - Knight (White/Black)
  - `P/p` - Pawn (White/Black)
- **Special Symbols:**
  - `.` - Empty square
  - `M` - Mine
  - `D/O` - Trap doors
  - `X` - Combined mine + trap door
  - `|/_` - Walls

#### Status Line Format
```
[player] [white_walls] [black_walls] [castling] [en_passant] [halfmove_clock]
```

- **player:** `w` or `b` (current turn)
- **white_walls/black_walls:** Number of walls used (0-3 each)
- **castling:** Four characters indicating castling availability (`+` or `-`)
- **en_passant:** Target square or `-` if not available
- **halfmove_clock:** Halfmoves since last capture or pawn move

## Game Rules

### Standard Chess Rules
- Each player must have exactly **1 king**
- **Pawn restrictions:** Cannot be placed on ranks 1 or 8
- **Piece limits** (including promotions):
  - Kings: 1 each
  - Queens: 9 each (1 original + 8 promoted)
  - Other pieces: 10 each (2 original + 8 promoted)

### Obstacle Rules
- **Walls:** Maximum 6 total (3 per player)
- **Mines:** Maximum 2 total, restricted to ranks 4-5
- **Trap Doors:** Maximum 2 total, restricted to ranks 3-6
- **Combined Obstacles:** Count toward both mine and trap door limits

## Development Structure

### Core Components
- **`obstacleChess.py`** - Main game controller
- **`game_validation.py`** - Rule validation and game state checking
- **`gui.py`** - Graphical user interface implementation
- **`helpful.py`** - Utility functions and helpers
- **`moves.py`** - Move generation and validation logic
- **`chessboard.py`** - Board representation and manipulation

## Strategy Tips

1. **Wall Placement:** Use walls to control key squares and limit opponent mobility
2. **Hidden Obstacles:** Place mines and trap doors strategically to surprise opponents
3. **Timing:** Consider when to reveal obstacle locations for maximum impact
4. **Defense:** Use obstacles to protect your king and important pieces
5. **Offense:** Create tactical combinations using obstacles to trap opponent pieces


## Contact

For questions, issues, or suggestions:
- **Email:** thaakir07@gmail.com

*Experience chess like never before with Obstacle Chess - where strategy meets mystery!*
