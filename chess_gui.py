import pygame

WIDTH, HEIGHT = 800,800
SQUARE_SIZE = WIDTH // 8


def draw_board(screen, vision: list):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    square_vision = vision
    
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(
                col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if square_vision['w'][row][col] > 0:
                pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(
                    col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            if square_vision['b'][row][col] > 0:
                pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(
                    col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)            


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
                


def gui(board, vision):
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
        draw_board(screen, vision)
        draw_pieces(screen, board, size=SQUARE_SIZE)  # Implement this function

        pygame.display.flip()

    pygame.quit()

