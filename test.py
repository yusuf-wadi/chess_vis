import chess_gui as cg
from chessvis import util, Board


# main function
if __name__ == '__main__':

    #example fen: rnbqkb1r/ppp1p1pp/5p1n/3p4/3P1P2/3Q4/PPP1P1PP/RNB1KBNR b KQkq - 0 1
    #starting fen: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR

    pgn = open("games/opera.pgn")
    
    fens = open("games/puzzles.txt").readlines()
    
    game_pgn = util.boards_from_pgn(pgn)

    puzzles_fens = util.boards_from_fens(fens)
    
    #cust_board = Board("1KR2B1R/1BP2P2/PPN3PP/7Q/5b1p/p4nq1/1pp3p1/1k1rr3 w - - 0 1")
    
    choice = input("F:Fen, P:PGN, C:Custom -> (f/p/c): ")
    if choice == 'f':
        cg.gui(puzzles_fens, choice)
    elif choice == 'p':
        cg.gui(game_pgn, choice)
    elif choice == 'c':
        cg.gui([Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')], choice)
    
