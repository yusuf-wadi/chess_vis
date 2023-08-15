import pygame
from chessvis import Board
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8


def draw_board(screen, board: Board):
    colors = [pygame.Color("white"), pygame.Color("dark gray")]
    square_vision = board.vision_matrix
    r, g, b = int(0), int(0), int(0)
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(
                col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            square_power = square_vision['w'][row][col]
            if square_power > 0:
                r = 0
                g = 0
                b = 200
            elif square_power < 0:
                r = 200
                g = 0
                b = 0
            else:
                r = 100
                g = 100
                b = 100

            pygame.draw.rect(screen, pygame.Color(r, g, b), pygame.Rect(
                col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board, size):
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col].piece
            if piece.type != ' ':
                piece_image = pygame.image.load(
                    f'assets/{piece.color}{piece.piece_names[piece.type.lower()]}.png')
                piece_image = pygame.transform.scale(piece_image, (size, size))
                screen.blit(piece_image, pygame.Rect(
                    col * size, row * size, size, size))


def gui(boards):
    pygame.init()
    # width = 400
    # height = 400
    # square_size = width // 8
    # Load the knight image
    knight_image = pygame.image.load("assets/bknight.png")
    # Set the window icon to the knight image
    pygame.display.set_icon(knight_image)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Chess GUI")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.Color("white"))
        for board in boards:
            draw_board(screen, board)
            draw_pieces(screen, board, SQUARE_SIZE)
            pygame.display.flip()
            pygame.time.wait(2000)

    pygame.quit()
