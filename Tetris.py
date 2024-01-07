import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [1]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [0, 1]],
    [[1, 1, 1], [1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
]

# Initialize game variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

class Tetris:
    def __init__(self):
        self.grid = [[0] * (WIDTH // GRID_SIZE) for _ in range(HEIGHT // GRID_SIZE)]
        self.current_shape = self.new_shape()
        self.x, self.y = self.starting_position()

    def new_shape(self):
        return random.choice(SHAPES)

    def starting_position(self):
        return (len(self.grid[0]) // 2 - len(self.current_shape[0]) // 2, 0)

    def draw_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, WHITE, (self.x * GRID_SIZE + x * GRID_SIZE, self.y * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def move_down(self):
        self.y += 1

    def move_left(self):
        if not self.collision(-1, 0):
            self.x -= 1

    def move_right(self):
        if not self.collision(1, 0):
            self.x += 1

    def rotate(self):
        rotated_shape = list(zip(*self.current_shape[::-1]))
        if not self.collision(0, 0, rotated_shape):
            self.current_shape = rotated_shape

    def collision(self, offset_x, offset_y, shape=None):
        shape = shape or self.current_shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x, grid_y = self.x + x + offset_x, self.y + y + offset_y
                    if grid_x < 0 or grid_x >= len(self.grid[0]) or grid_y >= len(self.grid):
                        return True
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return True
        return False

    def merge(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.y + y][self.x + x] = 1

    def check_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0] * len(self.grid[0]))

    def game_over(self):
        return any(self.grid[0])

# Initialize the game
tetris = Tetris()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                tetris.move_down()
            elif event.key == pygame.K_LEFT:
                tetris.move_left()
            elif event.key == pygame.K_RIGHT:
                tetris.move_right()
            elif event.key == pygame.K_UP:
                tetris.rotate()

    # Move down at a fixed rate
    if not tetris.collision(0, 1):
        tetris.move_down()
    else:
        tetris.merge()
        tetris.check_lines()
        tetris.current_shape = tetris.new_shape()
        tetris.x, tetris.y = tetris.starting_position()

        if tetris.game_over():
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the shape and grid
    tetris.draw_shape()
    tetris.draw_grid()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(5)

# Quit Pygame
pygame.quit()
