import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Enhanced Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Game settings
clock = pygame.time.Clock()
cell_size = 20
difficulty_speeds = {"Easy": 10, "Medium": 15, "Hard": 20}

class Snake:
    def __init__(self):
        self.body = [[width // 2, height // 2]]
        self.direction = "RIGHT"
        self.color = GREEN

    def move(self):
        head = self.body[0].copy()
        if self.direction == "UP":
            head[1] -= cell_size
        elif self.direction == "DOWN":
            head[1] += cell_size
        elif self.direction == "LEFT":
            head[0] -= cell_size
        elif self.direction == "RIGHT":
            head[0] += cell_size
        self.body.insert(0, head)

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, pygame.Rect(segment[0], segment[1], cell_size, cell_size))

class Food:
    def __init__(self):
        self.position = self.randomize_position()
        self.color = RED

    def randomize_position(self):
        return [random.randrange(0, width, cell_size), random.randrange(0, height, cell_size)]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], cell_size, cell_size))

class PowerUp:
    def __init__(self):
        self.position = self.randomize_position()
        self.color = BLUE
        self.active = False
        self.timer = 0

    def randomize_position(self):
        return [random.randrange(0, width, cell_size), random.randrange(0, height, cell_size)]

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], cell_size, cell_size))

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.power_up = PowerUp()
        self.score = 0
        self.high_score = self.load_high_score()
        self.difficulty = "Medium"
        self.game_over = False

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                    self.snake.direction = "UP"
                elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                    self.snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                    self.snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                    self.snake.direction = "RIGHT"

    def update(self):
        self.snake.move()

        # Check collision with food
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food = Food()
            self.score += 1

            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

            # Spawn power-up with 20% chance
            if random.random() < 0.2:
                self.power_up = PowerUp()
                self.power_up.active = True

        # Check collision with power-up
        if self.power_up.active and self.snake.body[0] == self.power_up.position:
            self.score += 5
            self.power_up.active = False
            self.power_up.timer = pygame.time.get_ticks()

        # Check if power-up effect should end
        if not self.power_up.active and pygame.time.get_ticks() - self.power_up.timer > 5000:
            self.power_up = PowerUp()

        # Check collision with walls or self
        if (self.snake.body[0][0] < 0 or self.snake.body[0][0] >= width or
            self.snake.body[0][1] < 0 or self.snake.body[0][1] >= height or
            self.snake.body[0] in self.snake.body[1:]):
            self.game_over = True

        # Remove tail if snake hasn't eaten
        if len(self.snake.body) > self.score + 1:
            self.snake.body.pop()

    def draw(self):
        window.fill(BLACK)
        self.snake.draw(window)
        self.food.draw(window)
        if self.power_up.active:
            self.power_up.draw(window)
        self.draw_score()
        pygame.display.update()

    def draw_score(self):
        font = pygame.font.SysFont('arial', 20)
        score_surface = font.render(f'Score: {self.score}  High Score: {self.high_score}', True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        window.blit(score_surface, score_rect)

    def show_game_over(self):
        window.fill(BLACK)
        font = pygame.font.SysFont('arial', 40)
        game_over_surface = font.render(f'Game Over! Your Score: {self.score}', True, RED)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (width // 2, height // 4)
        window.blit(game_over_surface, game_over_rect)

        font = pygame.font.SysFont('arial', 30)
        instruction = font.render('Press SPACE to play again or ESC to quit', True, WHITE)
        instruction_rect = instruction.get_rect()
        instruction_rect.midtop = (width // 2, height // 2)
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
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

    def show_difficulty_selection(self):
        window.fill(BLACK)
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Select Difficulty', True, WHITE)
        title_rect = title.get_rect()
        title_rect.midtop = (width // 2, height // 4)
        window.blit(title, title_rect)

        difficulties = list(difficulty_speeds.keys())
        for i, diff in enumerate(difficulties):
            font = pygame.font.SysFont('arial', 30)
            diff_surface = font.render(f"{i+1}. {diff}", True, WHITE)
            diff_rect = diff_surface.get_rect()
            diff_rect.midtop = (width // 2, height // 2 + i * 50)
            window.blit(diff_surface, diff_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.difficulty = "Easy"
                        waiting = False
                    elif event.key == pygame.K_2:
                        self.difficulty = "Medium"
                        waiting = False
                    elif event.key == pygame.K_3:
                        self.difficulty = "Hard"
                        waiting = False

    def run(self):
        self.show_difficulty_selection()
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(difficulty_speeds[self.difficulty])

        self.show_game_over()

if __name__ == "__main__":
    while True:
        game = Game()
        game.run()