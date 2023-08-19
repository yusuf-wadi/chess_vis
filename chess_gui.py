import pygame
import pygame_menu
from chessvis import Board, util
import math
import os
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8

##UTIL FUNCTION##


def items_from_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]


# fens folder of current directory
fen_paths = items_from_folder('fens')
# pgn folder of current directory
pgn_paths = items_from_folder('pgns')

print(fen_paths, pgn_paths)


class ChessGUI():

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((600, 400))
        self.choice = None
        # Load the knight image
        knight_image = pygame.image.load("pieces/bknight.png")
        # Set the window icon to the knight image
        pygame.display.set_icon(knight_image)
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Chess GUI")
        self.running = True
        self.board_index = 0
        self.scaler = 0
        self.delay = 200
        self.show_pieces = False
        self.selected = None
        self.view_direction = 1
        self.boards = []

    def draw_board(self, screen, board: Board, scaler=0):
        colors = [pygame.Color("white"), pygame.Color("black")]
        square_vision = board.vision_matrix
        r, g, b = int(0), int(0), int(0)
        for row in range(8):
            for col in range(8):

                square_power_w = square_vision['w'][row][col]
                square_power_b = square_vision['b'][row][col]

                len_diff = len(square_power_w) - len(square_power_b)
                value_diff = sum(square_power_w) - sum(square_power_b)
                flip = -1 if len_diff == 0 else 1
                scale = max(-10, min(scaler, 10))
                # first to define a neutral square
                if len(square_power_b) == 0 and len(square_power_w) == 0:
                    r, g, b = 100, 100, 100
                else:
                    # keep values between 0 and 255

                    r = max(0, (min(100 + math.floor(-value_diff * flip *
                            scale) - math.floor(len_diff * scale*10), 255)))
                    g = 0
                    b = max(0, (min(100 + math.floor(value_diff * flip *
                            scale) + math.floor(len_diff * scale*10), 255)))

                pygame.draw.rect(screen, pygame.Color(r, g, b), pygame.Rect(
                    col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                color = colors[(row + col) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(
                    col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

    def draw_pieces(self, screen, board, size):
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col].piece
                if piece.type != ' ':
                    piece_image = pygame.image.load(
                        f'pieces/{piece.color}{piece.piece_names[piece.type.lower()]}.png')
                    piece_image = pygame.transform.scale(
                        piece_image, (size, size))
                    screen.blit(piece_image, pygame.Rect(
                        col * size, row * size, size, size))

    def start_menu(self):
        # selection menu for user to choose between pgn or fen or custom
        menu = pygame_menu.Menu(
            width=600, height=600, title='Welcome', theme=pygame_menu.themes.THEME_DARK)
        menu.add.dropselect(
            'Select:', [('PGN', 1), ('FEN', 2), ('Custom', 3)], onchange=self.set_choice)
        menu.add.button('Play', self.mainloop, menu)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)

    def set_choice(self, choice, choice_text):
        self.choice = choice_text

    def setup_boards(self):
        if self.choice == 1:
            pgn = open(pgn_paths[0])
            return util.boards_from_pgn(pgn)
        elif self.choice == 2:
            return util.boards_from_fens(fen_paths[0])
        elif self.choice == 3:
            text = pygame_menu.Menu(title='Custom',width=600, height=600, theme = pygame_menu.themes.THEME_DARK)
            text.add.text_input('Enter FEN: ', default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
            text.add.button('Play', text.disable)
            text.mainloop(self.screen)
            fen = str(text.get_input_data().values())
            print(fen)
            return [Board(fen)]
            

    def mainloop(self, menu: pygame_menu.Menu):
        menu.disable()
        running = True
        pieces = True

        # set up boards
        boards = self.setup_boards()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(pygame.Color("white"))

            if len(boards) > 1:
                board = boards[self.board_index]
            else:
                board = boards[0]

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.board_index = max(0, self.board_index - 1)
                pygame.time.delay(self.delay)
            if keys[pygame.K_RIGHT]:
                self.board_index = min(len(boards) - 1, self.board_index + 1)
                pygame.time.delay(self.delay)
            if keys[pygame.K_UP]:
                self.scaler = self.scaler + 0.1
                pygame.time.delay(self.delay-100)
            if keys[pygame.K_DOWN]:
                self.scaler = self.scaler - 0.1
                pygame.time.delay(self.delay-100)
            if keys[pygame.K_SPACE]:
                pieces = not pieces
                pygame.time.delay(self.delay)
            if keys[pygame.K_ESCAPE]:
                menu.enable()

            if self.choice == 3:
                # check if user clicked on a piece, if so, highlight it, then check if user clicked on a valid move, if so, move the piece
                if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // SQUARE_SIZE
                    row = pos[1] // SQUARE_SIZE

                    print(board.vision_matrix['w'][row][col], board.vision_matrix['b']
                          [row][col], board.board[row][col].piece)

                    if self.selected is None:
                        self.selected = board.board[row][col]

                    else:
                        if self.selected.piece.color != 'Empty' and self.selected.piece.value in board.vision_matrix[self.selected.piece.color][row][col]:
                            new_fen = board.move_piece_fen(
                                self.selected, (row, col))
                            self.selected = None
                            boards.append(Board(new_fen))
                            print(boards)
                            pygame.time.delay(self.delay)

            self.draw_board(self.screen, board, self.scaler)

            if pieces:
                self.draw_pieces(self.screen, board, SQUARE_SIZE)

            pygame.display.flip()

        pygame.quit()
