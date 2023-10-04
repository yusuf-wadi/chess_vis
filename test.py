import chess_gui as cg
from chessvis import util, Board
import fenparser
import os
# main function
if __name__ == '__main__':

    fen_path = r'C:\Users\thewa\Desktop\projects\computational_neuroscience\AI_ML\chess\chess_vis_cli\fens'
    pgn_path = r'C:\Users\thewa\Desktop\projects\computational_neuroscience\AI_ML\chess\chess_vis_cli\pgns'
    

    while True:
        
        choice = input("F:Fen, P:PGN, C:Custom -> (f/p/c): ")

        match(choice):
        
            case 'f':
                fens_path = os.listdir(fen_path)
                for i, fen in enumerate(fens_path):
                    print('-'*(len(fen)+7))
                    print('|',i,'|', fen, '|')
                    print('-'*(len(fen)+7))
                fen_choice = int(input("Choose a fen: "))
                fen = fens_path[fen_choice]
                fens = os.path.join(fen_path, fen)
                boards = util.boards_from_fens(fens)
                cg.gui(boards, 'f')
                
            case 'p':
                pgns_path = os.listdir(pgn_path)
                for i, pgn in enumerate(pgns_path):
                    print('-'*(len(pgn)+7))
                    print( '|',i,'|', pgn, '|')
                    print('-'*(len(pgn)+7))
                pgn_choice = int(input("Choose a pgn: "))
                pgn = pgns_path[pgn_choice]
                pgn = os.path.join(pgn_path, pgn)
                pgn = open(pgn)
                boards = util.boards_from_pgn(pgn)
                cg.gui(boards, 'p')
                
            case 'c':
                fen = input("Enter a fen: ")
                boards = [Board(fen)]
                cg.gui(boards, 'c')
                
    
