import pygame
import sys
import random

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PIPE_WIDTH = 80
PIPE_GAP = 200
BIRD_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 204, 0)

class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vel = 0
        self.size = BIRD_SIZE
        self.image = pygame.image.load('bird.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def update(self):
        self.vel += 0.5
        self.y += self.vel

    def jump(self):
        self.vel = -10

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vel = 0

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.gap_y = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.width = PIPE_WIDTH

    def update(self):
        self.x -= 2

def draw_text(screen, text, font_size, x, y):
    font = pygame.font.SysFont('Arial', font_size)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    bird = Bird()
    pipes = [Pipe()]
    score = 0
    high_score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_r:
                    bird.reset()
                    score = 0
                    pipes = [Pipe()]

        bird.update()
        for pipe in pipes:
            pipe.update()
            if pipe.x < bird.x + bird.size and pipe.x + pipe.width > bird.x:
                if bird.y < pipe.gap_y or bird.y + bird.size > pipe.gap_y + PIPE_GAP:
                    # Game over
                    if score > high_score:
                        high_score = score
                    score = 0
                    pipes = [Pipe()]
                    bird.reset()
            if pipe.x < -pipe.width:
                pipes.remove(pipe)
                score += 1
                pipes.append(Pipe())

        screen.fill(WHITE)
        for pipe in pipes:
            pygame.draw.rect(screen, BLACK, (pipe.x, 0, pipe.width, pipe.gap_y))
            pygame.draw.rect(screen, BLACK, (pipe.x, pipe.gap_y + PIPE_GAP, pipe.width, SCREEN_HEIGHT - pipe.gap_y - PIPE_GAP))
        screen.blit(bird.image, (bird.x, bird.y))
        draw_text(screen, f'Score: {score}', 32, 10, 10)
        draw_text(screen, f'High Score: {high_score}', 32, 10, 50)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()