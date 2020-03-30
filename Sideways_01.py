import pygame
class PlayerInput:
    def __init__(self):
        self.stop = False

    def update(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.stop = True

def paint_screen(window):
    window.fill((0,0,0))
    pygame.display.flip()

def main_loop():
    pygame.init()
    screen_width = 800
    screen_height = 600
    window = pygame.display.set_mode((screen_width,screen_height))
    player_input = PlayerInput()

    while not player_input.stop:
        pygame.time.delay(5)
        player_input.update()
        paint_screen(window)
    pygame.display.quit()
    pygame.quit()

main_loop()


