import pygame
from chessvis import Board, Piece
import math
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8


def draw_board(screen, board: Board, scaler=0):
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
            scale = max(-10,min(scaler, 10))
            # first to define a neutral square
            if len(square_power_b) == 0 and len(square_power_w) == 0:
                r, g, b = 100, 100, 100
            else:
                # keep values between 0 and 255
                
                r = max(0,(min(100 + math.floor(-value_diff *flip* scale) - math.floor(len_diff * scale*10), 255)))
                g = 0 
                b = max(0,(min(100 + math.floor(value_diff * flip * scale) + math.floor(len_diff * scale*10), 255)))
            

            
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
                    f'pieces/{piece.color}{piece.piece_names[piece.type.lower()]}.png')
                piece_image = pygame.transform.scale(piece_image, (size, size))
                screen.blit(piece_image, pygame.Rect(
                    col * size, row * size, size, size))


def gui(boards, state):
    pygame.init()
    # width = 400
    # height = 400
    # square_size = width // 8
    # Load the knight image
    knight_image = pygame.image.load("pieces/bknight.png")
    # Set the window icon to the knight image
    pygame.display.set_icon(knight_image)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Chess GUI")
    running = True
    i = 0
    scaler = 0
    delay = 200
    pieces = False
    selected = None
    valid_moves_from_selected = []
    d = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.Color("white"))

        if len(boards) > 1:
            board = boards[i]
        else:
            board = boards[0]
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            i = max(0, i - 1)
            pygame.time.delay(delay)
        if keys[pygame.K_RIGHT]:
            i = min(len(boards) - 1, i + 1)
            pygame.time.delay(delay)
        if keys[pygame.K_UP]:
            scaler = scaler + 0.1
            pygame.time.delay(delay-100)
        if keys[pygame.K_DOWN]:
            scaler = scaler - 0.1
            pygame.time.delay(delay-100)
        if keys[pygame.K_SPACE]:
            pieces = not pieces
            pygame.time.delay(delay)
        
        
        if state == 'c':
            #check if user clicked on a piece, if so, highlight it, then check if user clicked on a valid move, if so, move the piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                
                print(board.vision_matrix['w'][row][col], board.vision_matrix['b'][row][col], board.board[row][col].piece)
                
                if selected is None:
                    selected = board.board[row][col]
                
                else:
                    if selected.piece.color != 'Empty' and selected.piece.value in board.vision_matrix[selected.piece.color][row][col]:
                        new_fen = board.move_piece_fen(selected, (row, col))
                        selected = None
                        boards.append(Board(new_fen))
                        print(boards)
                        pygame.time.delay(delay)
                        
        draw_board(screen, board, scaler)
        if pieces:
            draw_pieces(screen, board, SQUARE_SIZE)
                
        pygame.display.flip()

    pygame.quit()
