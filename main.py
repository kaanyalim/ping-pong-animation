import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL1_RADIUS = 10
BALL2_RADIUS = 10
BALL1_SPEED = [1, 1]
BALL2_SPEED = [-1, -1]
BLOCK_SIZE = 50
NUM_BLOCKS_X = WIDTH // BLOCK_SIZE
NUM_BLOCKS_Y = HEIGHT // BLOCK_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL1_COLOR = BLACK
BALL2_COLOR = WHITE

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Ying Yang")

# Ball positioning setup
ball1_pos = [WIDTH // 4, HEIGHT // 2]
ball1_speed = BALL1_SPEED

ball2_pos = [3 * WIDTH // 4, HEIGHT // 2]
ball2_speed = BALL2_SPEED


# Block class to manage color attribute
class Block:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.color = color


# Block setup
blocks = []

# Creating the white blocks, top half of the screen
for i in range(NUM_BLOCKS_X):
    for j in range(NUM_BLOCKS_Y // 2):
        block = Block(i * BLOCK_SIZE, j * BLOCK_SIZE, WHITE)
        blocks.append(block)

# Creating the black blocks, bottom half of the screen
for i in range(NUM_BLOCKS_X):
    for j in range(NUM_BLOCKS_Y // 2, NUM_BLOCKS_Y):
        block = Block(i * BLOCK_SIZE, j * BLOCK_SIZE, BLACK)
        blocks.append(block)


# Drawing the balls
def draw_balls():
    pygame.draw.circle(
        screen, BALL1_COLOR, (int(ball1_pos[0]), int(ball1_pos[1])), BALL1_RADIUS
    )
    pygame.draw.circle(
        screen, BALL2_COLOR, (int(ball2_pos[0]), int(ball2_pos[1])), BALL2_RADIUS
    )


# Drawing the blocks
def draw_blocks():
    for block in blocks:
        pygame.draw.rect(screen, block.color, block.rect)


# Updating the balls' positions
def move_balls():
    global ball1_speed, ball2_speed

    ball1_pos[0] += ball1_speed[0]
    ball1_pos[1] += ball1_speed[1]

    ball2_pos[0] += ball2_speed[0]
    ball2_pos[1] += ball2_speed[1]

    # Collisions with window boundaries
    if ball1_pos[0] >= WIDTH - BALL1_RADIUS or ball1_pos[0] <= BALL1_RADIUS:
        ball1_speed[0] = -ball1_speed[0]
    if ball1_pos[1] >= HEIGHT - BALL1_RADIUS or ball1_pos[1] <= BALL1_RADIUS:
        ball1_speed[1] = -ball1_speed[1]

    if ball2_pos[0] >= WIDTH - BALL2_RADIUS or ball2_pos[0] <= BALL2_RADIUS:
        ball2_speed[0] = -ball2_speed[0]
    if ball2_pos[1] >= HEIGHT - BALL2_RADIUS or ball2_pos[1] <= BALL2_RADIUS:
        ball2_speed[1] = -ball2_speed[1]


# Collision handling with the blocks, and color changing
def handle_collisions():
    for block in blocks:
        # ball 1
        # adjusting to calculate from the edge of the ball, and not the center
        top_edge = ball1_pos[1] - BALL1_RADIUS
        bottom_edge = ball1_pos[1] + BALL1_RADIUS
        left_edge = ball1_pos[0] - BALL1_RADIUS
        right_edge = ball1_pos[0] + BALL1_RADIUS

        if (
            block.rect.collidepoint(left_edge, top_edge)
            or block.rect.collidepoint(left_edge, bottom_edge)
            or block.rect.collidepoint(right_edge, top_edge)
            or block.rect.collidepoint(right_edge, bottom_edge)
        ):
            if block.color != BALL2_COLOR:
                block.color = BALL2_COLOR
                overlap_x = BALL1_RADIUS - abs(ball1_pos[0] - block.rect.centerx)
                overlap_y = BALL1_RADIUS - abs(ball1_pos[1] - block.rect.centery)
                if overlap_x < overlap_y:
                    ball1_speed[0] = -ball1_speed[0]
                else:
                    ball1_speed[1] = -ball1_speed[1]
                break

        # ball 2
        # adjusting to calculate from the edge of the ball, and not the center
        top_edge = ball2_pos[1] - BALL2_RADIUS
        bottom_edge = ball2_pos[1] + BALL2_RADIUS
        left_edge = ball2_pos[0] - BALL2_RADIUS
        right_edge = ball2_pos[0] + BALL2_RADIUS

        if (
            block.rect.collidepoint(left_edge, top_edge)
            or block.rect.collidepoint(left_edge, bottom_edge)
            or block.rect.collidepoint(right_edge, top_edge)
            or block.rect.collidepoint(right_edge, bottom_edge)
        ):
            if block.color != BALL1_COLOR:
                block.color = BALL1_COLOR
                overlap_x = BALL2_RADIUS - abs(ball2_pos[0] - block.rect.centerx)
                overlap_y = BALL2_RADIUS - abs(ball2_pos[1] - block.rect.centery)
                if overlap_x < overlap_y:
                    ball2_speed[0] = -ball2_speed[0]
                else:
                    ball2_speed[1] = -ball2_speed[1]
                break


# Main game loop
if __name__ == "__main__":
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        move_balls()
        handle_collisions()

        # Draw everything
        screen.fill(WHITE)
        draw_blocks()
        draw_balls()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
