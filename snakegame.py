import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up game variables
BLOCK_SIZE = 20
SNAKE_SPEED = 5

# Load images
snake_head_img = pygame.image.load('snake_head.png')
snake_body_img = pygame.image.load('snake_body.png')
food_img = pygame.image.load('food.png') 

# Resize images to fit the block size
snake_head_img = pygame.transform.scale(snake_head_img, (BLOCK_SIZE, BLOCK_SIZE))
snake_body_img = pygame.transform.scale(snake_body_img, (BLOCK_SIZE, BLOCK_SIZE))
food_img = pygame.transform.scale(food_img, (BLOCK_SIZE, BLOCK_SIZE)) 

# Set up the display
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DaGuy Snake Game")

# Set up font
font = pygame.font.SysFont(None, 30)

# Set up initial score and highest score
score = 0
highest_score = 0

# Function to display text
def display_message(msg, color, y_offset=0):
    screen_text = font.render(msg, True, color)
    win.blit(screen_text, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3 + y_offset])

# Function to draw the snake with images
def draw_snake(snake_list):
    for index, (x, y) in enumerate(snake_list):
        if index == len(snake_list) - 1:               
            win.blit(snake_head_img, (x, y))
        else:
            win.blit(snake_body_img, (x, y))

# Function to draw the food with image
def draw_food(x, y):
    win.blit(food_img, (x, y))

# Function to draw the score
def draw_score(current_score, highest_score):
    score_text = font.render(f"Score: {current_score}", True, WHITE)
    high_score_text = font.render(f"High Score: {highest_score}", True, WHITE)
    win.blit(score_text, [10, 10])
    win.blit(high_score_text, [10, 40])

# Function for the main game loop
def game_loop():
    global score, highest_score

    game_over = False
    game_close = False

    x1 = SCREEN_WIDTH // 2
    y1 = SCREEN_HEIGHT // 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0  # Reset score at the start of the game

    # Initial position of food
    foodx = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    clock = pygame.time.Clock()

    while not game_over:

        while game_close:
            win.fill(BLACK)
            display_message("You Lost! Press Q-Quit or C-Play Again", RED)
            display_message(f"Score: {score}", WHITE, 40)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        win.fill(BLACK)

        # Draw the food with the image
        draw_food(foodx, foody)

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        draw_score(score, highest_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            foody = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            length_of_snake += 1
            global SNAKE_SPEED
            SNAKE_SPEED += 0.25
            score += 10
            if score > highest_score:
                highest_score = score

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    sys.exit()


game_loop()
