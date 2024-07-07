import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Game settings
clock = pygame.time.Clock()
speed = 15

def reset_game():
    global snake_pos, snake_body, snake_direction, change_to, food_pos, food_spawn, score
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    snake_direction = 'RIGHT'
    change_to = snake_direction
    food_pos = [random.randrange(1, (width//10)) * 10,
                random.randrange(1, (height//10)) * 10]
    food_spawn = True
    score = 0

# Initial reset
reset_game()

def show_score():
    font = pygame.font.SysFont('times new roman', 20)
    score_surface = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    window.blit(score_surface, score_rect)

def welcome_screen():
    window.fill(BLACK)
    font = pygame.font.SysFont('times new roman', 40)
    title = font.render('Welcome to Snake Game', True, GREEN)
    title_rect = title.get_rect()
    title_rect.midtop = (width/2, height/4)
    window.blit(title, title_rect)

    font = pygame.font.SysFont('times new roman', 30)
    instruction = font.render('Press SPACE to start', True, WHITE)
    instruction_rect = instruction.get_rect()
    instruction_rect.midtop = (width/2, height/2)
    window.blit(instruction, instruction_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_over():
    window.fill(BLACK)
    font = pygame.font.SysFont('times new roman', 40)
    game_over_surface = font.render(f'Your Score is: {score}', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width/2, height/4)
    window.blit(game_over_surface, game_over_rect)

    font = pygame.font.SysFont('times new roman', 30)
    instruction = font.render('Press SPACE to play again or ESC to quit', True, WHITE)
    instruction_rect = instruction.get_rect()
    instruction_rect.midtop = (width/2, height/2)
    window.blit(instruction, instruction_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
    return False

# Main game loop
def game_loop():
    global snake_direction, change_to, food_spawn, score, snake_pos, snake_body, food_pos

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    change_to = 'UP'
                if event.key == pygame.K_DOWN and snake_direction != 'UP':
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    change_to = 'RIGHT'

        # Validate direction
        if change_to == 'UP' and snake_direction != 'DOWN':
            snake_direction = 'UP'
        if change_to == 'DOWN' and snake_direction != 'UP':
            snake_direction = 'DOWN'
        if change_to == 'LEFT' and snake_direction != 'RIGHT':
            snake_direction = 'LEFT'
        if change_to == 'RIGHT' and snake_direction != 'LEFT':
            snake_direction = 'RIGHT'

        # Move the snake
        if snake_direction == 'UP':
            snake_pos[1] -= 10
        if snake_direction == 'DOWN':
            snake_pos[1] += 10
        if snake_direction == 'LEFT':
            snake_pos[0] -= 10
        if snake_direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawn food
        if not food_spawn:
            food_pos = [random.randrange(1, (width//10)) * 10,
                        random.randrange(1, (height//10)) * 10]
        food_spawn = True

        # Draw everything
        window.fill(BLACK)
        for pos in snake_body:
            pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(window, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        show_score()

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] > width-10:
            return game_over()
        if snake_pos[1] < 0 or snake_pos[1] > height-10:
            return game_over()
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                return game_over()

        pygame.display.update()
        clock.tick(speed)

# Main game execution
while True:
    welcome_screen()
    if not game_loop():
        break

pygame.quit()