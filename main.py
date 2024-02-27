import pygame

pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 600

TEXT_FONT = pygame.font.SysFont("Arial", 36)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Main game loop
running = True
while running:
    pygame.display.set_caption('Yasuo')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((000, 255, 255))

    pygame.draw.rect(screen, (0, 255, 0), (400, 400, 200, 100))

    draw_text('Yasuo Game', TEXT_FONT, (255, 255, 255), 420, 420)

    pygame.time.delay(1000)

    pygame.display.flip()

pygame.quit()