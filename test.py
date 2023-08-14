from chessvis import Board
import chess_gui as cg

# main function
if __name__ == '__main__':
    
    # example fen: rnbqkb1r/ppp1p1pp/5p1n/3p4/3P1P2/3Q4/PPP1P1PP/RNB1KBNR b KQkq - 0 1
    # example fen: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
    
    # create board
    
    board = Board()
    
    fen = input("Enter FEN: ")
    
    board.parse_fen(fen)
    
    cg.gui(board, board.vision_matrix)
    
    
    
    
    
    
    
    
    

    

    
    