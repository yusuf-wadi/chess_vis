from fenparser import FenParser
import numpy as np
import chess.pgn


class Piece():

    # jacob sarratt?
    piece_values = {
        ' ': 0,
        'p': 1,
        'n': 3,
        'b': 3,
        'r': 5,
        'q': 9,
        'k': 10000
    }

    piece_vision = {
        ' ': [[], 0],
        'p': [[(1, 1), (1, -1)], 1],
        'n': [[(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (-1, -2), (1, -2)], 1],
        'b': [[(1, 1), (1, -1), (-1, 1), (-1, -1)], 7],
        'r': [[(1, 0), (-1, 0), (0, 1), (0, -1)], 7],
        'q': [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)], 7],
        'k': [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)], 1]
    }

    piece_names = {
        ' ': 'Empty',
        'p': 'Pawn',
        'n': 'Knight',
        'b': 'Bishop',
        'r': 'Rook',
        'q': 'Queen',
        'k': 'King',
    }

    def __init__(self, piece: str) -> None:
        self.type = piece
        self.value = self.piece_values[piece.lower()]
        if piece.isupper():
            self.color = 'w'
        elif piece.islower():
            self.color = 'b'
        else:
            self.color = 'Empty'

    def get_vision(self) -> list:
        return self.piece_vision[self.type.lower()]

    def __str__(self) -> str:
        return self.type if self.type != ' ' else '.'

    def __repr__(self) -> str:
        return str(self)


class Square():

    piece = None
    rank = 0
    file = 0
    X = 0
    O = 0
    king = False

    def __init__(self, piece: Piece, position: (int, int), X: int, O: int, king: bool):

        self.piece = piece
        self.rank = position[0]
        self.file = position[1]
        self.X = X
        self.O = O
        self.king = king

    def __eq__(self, other):
        return self.piece == other.piece and\
            self.rank == other.rank and\
            self.file == other.file and\
            self.X == other.X and\
            self.O == other.O and\
            self.king == other.king

    def __str__(self) -> str:
        if self.piece is None:
            return '.'
        else:
            return str(self.piece)

    def __repr__(self) -> str:
        return str(self)

    def update_vision(self, vision):
        self.X = vision[0]
        self.O = vision[1]


class Board():

    def __init__(self, fen='8/8/8/8/8/8/8/8'):
        self.isChecked = False
        self.fen = fen
        #self.vision_matrix = {'w': [[0 for x in range(8)] for _ in  range(8)], 'b': [[0 for x in range(8)] for _ in  range(8)]}
        self.vision_matrix = {'w': [[[] for x in range(8)] for _ in range(8)], 'b': [
            [[] for x in range(8)] for _ in range(8)]}
        self.board = [[Square(Piece(' '), (i, j), 0, 0, False)
                      for i in range(8)] for j in range(8)]
        self.first_color = ''
        self.parse_fen(fen)

    def get_board(self):
        return self.board

    def get_vision_matrix(self):
        return self.vision_matrix

    def parse_fen(self, fen):
        fen_parser = FenParser(fen)
        fen_board = fen_parser.parse()
        self.board = self.update_board(fen_board)
    
    def move_piece_fen(self, square, position):
        # get new fen based on move
        # update board
        self.board[square.rank][square.file] = Square(Piece(' '), (square.rank, square.file), 0, 0, False)
        self.board[position[0]][position[1]] = Square(square.piece, position, 0, 0, False)

    def update_board(self, fen_board):
        board = []
        for rank in range(8):
            board.append([])
            for file in range(8):
                piece_type = fen_board[rank][file]
                piece = Piece(piece_type)
                # check for top of board color
                if self.first_color == '':
                    self.first_color = piece.color
                board[rank].append(Square(
                    piece, (rank, file), 0, 0, False if piece.type.lower() != 'k' else True))

        # calculate vision matrix
        self.calculate_vision_matrix(board)

        return board

    def calculate_vision_matrix(self, board):

        for rank in range(8):
            for file in range(8):
                piece = board[rank][file].piece
                if piece.type != ' ':
                    vectors = piece.get_vision()
                    directions = vectors[0]
                    dist = vectors[1]
                    for direction in directions:
                        for distance in range(1, dist + 1):
                            if piece.color != self.first_color:
                                distance = -distance
                            new_rank = rank + direction[0] * distance
                            new_file = file + direction[1] * distance
                            if new_rank in range(8) and new_file in range(8):
                                target_square = board[new_rank][new_file]
                                if target_square.piece.type == ' ':
                                    # self.vision_matrix[piece.color][new_rank][new_file]+=1*piece.value
                                    self.vision_matrix[piece.color][new_rank][new_file].append(
                                        piece.value)
                                elif target_square.piece.type != ' ':
                                    if target_square.piece.type.lower() == 'k' and target_square.piece.color != piece.color:
                                        self.isChecked = True
                                        self.vision_matrix[piece.color][new_rank][new_file].append(
                                            piece.value*10)
                                        break
                                    elif target_square.piece.type.lower() == 'k' and target_square.piece.color == piece.color:
                                        # self.vision_matrix[piece.color][new_rank][new_file].append(piece.value)
                                        break
                                    # self.vision_matrix[piece.color][new_rank][new_file]+=1*piece.value
                                    self.vision_matrix[piece.color][new_rank][new_file].append(
                                        piece.value)
                                    break  # piece in the way

        # calculate O values
        #self.vision_matrix['w'] = np.array(self.vision_matrix['w']) - np.array(self.vision_matrix['b'])
        wvision = self.vision_matrix['w']
        bvision = self.vision_matrix['b']

    # define print function: print(board)

    def __str__(self):
        board_str = ''
        for rank in range(8):
            for file in range(8):
                board_str += str(self.board[rank][file]) + ' ' + str(
                    self.board[rank][file].X) + ' ' + str(self.board[rank][file].O) + '   '
            board_str += '\n'
        return board_str

    def __repr__(self) -> str:
        for rank in self.board:
            print(rank)


class util():

    def boards_from_pgn(pgn):
        game = chess.pgn.read_game(pgn)
        game_fens = []
        while game.next():
            game = game.next()
            game_fens.append(game.board().fen())
        return [Board(fen=fen) for fen in game_fens]

    def boards_from_fens(fens):
        with open(fens, 'r') as f:
            fens = f.readlines()
            
            return [Board(fen=fen) for fen in fens]
