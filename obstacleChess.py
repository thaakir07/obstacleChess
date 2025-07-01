import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ''
import stddraw
from game_validation import ChessGame

def main():
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    with open(input_file_name, 'r') as input_file:
        with open(output_file_name, 'w') as output_file:
            game = ChessGame(input_file_name, output_file_name, '')
            game.start_game()
            validated_board, status_line = game.get_board()
            ###changes made here
            for i in range(len(status_line)): status_line[i] = str(status_line[i])
            for row in validated_board: output_file.write(''.join(row) + '\n')
            output_file.write(' '.join(status_line))
                
if __name__ == '__main__':
    root = stddraw.Tkinter.Tk()
    root.withdraw()
    main()