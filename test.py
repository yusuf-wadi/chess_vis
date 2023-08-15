from chessvis import Board
import chess_gui as cg
import chess.pgn

# main function
if __name__ == '__main__':

    # example fen: rnbqkb1r/ppp1p1pp/5p1n/3p4/3P1P2/3Q4/PPP1P1PP/RNB1KBNR b KQkq - 0 1

    pgn = open("games/opera.pgn")
    game = chess.pgn.read_game(pgn)
    game_fens = []
    while game.next():
        game = game.next()
        game_fens.append(game.board().fen())

    boards = [Board(fen=fen) for fen in game_fens]
    
    cg.gui(boards)
