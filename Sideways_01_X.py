import pygame
class PlayerInput:
    def __init__(self):
        self.stop = False
        self.effect = False

    def update(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.stop = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.effect = True
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE:
                    self.effect = False

def play_effect(crash_sound):
    pygame.mixer.Sound.play(crash_sound)

    


def paint_screen(window, start_ticks):
    ticks = pygame.time.get_ticks()-start_ticks
    if ticks < 1000 and ticks > 0:
        remainder = ticks % 3
        if remainder == 0:
            window.fill(black)
        elif remainder == 1:
            window.fill(white)
        elif remainder == 2:
            window.fill(lilla)
    else:
        window.fill(black)
    pygame.display.flip()

def main_loop():
    pygame.init()
    crash_sound = pygame.mixer.Sound("Flashbang-Kibblesbob-899170896.wav")
    screen_width = 800
    screen_height = 600
    window = pygame.display.set_mode((screen_width,screen_height))
    player_input = PlayerInput()
    start_ticks = 10000000
    while not player_input.stop:
        if player_input.effect:
            start_ticks=pygame.time.get_ticks()
            play_effect(crash_sound)
        pygame.time.delay(5)
        player_input.update()
        paint_screen(window, start_ticks)
    pygame.display.quit()
    pygame.quit()

black = (0,0,0)
white = (255, 255, 255)
lilla = (255, 0, 255)
main_loop()

