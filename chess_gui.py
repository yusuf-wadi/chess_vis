import pygame
from chessvis import Board
import math
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8


def draw_board(screen, board: Board):
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
            scale = 10
            # first to define a neutral square
            if len(square_power_b) == 0 and len(square_power_w) == 0:
                r, g, b = 100, 100, 100
            else:
                # keep values between 0 and 255
                
                r = max(0,(min(140 + math.floor(-value_diff *flip* scale) - (len_diff * scale*10), 255)))
                g = 0 
                b = max(0,(min(140 + math.floor(value_diff * flip * scale) + (len_diff * scale*10), 255)))
            

            
            pygame.draw.rect(screen, pygame.Color(r, g, b), pygame.Rect(
                col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(
                col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)


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
    i = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.Color("white"))

        board = boards[i]
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            i = max(0, i - 1)
            pygame.time.delay(250)
        if keys[pygame.K_RIGHT]:
            i = min(len(boards) - 1, i + 1)
            pygame.time.delay(250)
        draw_board(screen, board)
        draw_pieces(screen, board, SQUARE_SIZE)
        pygame.display.flip()

    pygame.quit()
