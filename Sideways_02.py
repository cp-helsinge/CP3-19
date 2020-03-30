import pygame
class PlayerInput:
    def __init__(self):
        self.stop = False
        self.left = False
        self.right = False

    def update(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.stop = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.left = True
                if e.key == pygame.K_RIGHT:
                    self.right = True
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    self.left = False
                if e.key == pygame.K_RIGHT:
                    self.right = False


class Player:
    def __init__(self):
        self.playerImage = pygame.image.load("player.png").convert_alpha()
        self.rect = self.playerImage.get_rect(bottomleft=(0, window.get_height()))
        self.alive = True 

    def move(self, player_input):
        if player_input.left and self.rect.left > window.get_rect().left:
            self.rect.x = self.rect.x - 2
        if player_input.right and self.rect.right < window.get_rect().right:
            self.rect.x = self.rect.x + 2


class GameState:
    def __init__(self):
        self.player = Player()

    def update(self, player_input):
        self.player.move(player_input)


def paint_screen(window):
    window.fill((0,0,0))
    window.blit(gameState.player.playerImage, gameState.player.rect)
    pygame.display.flip()

def main_loop():

    while not player_input.stop:
        pygame.time.delay(20)
        player_input.update()
        gameState.update(player_input)
        paint_screen(window)
    pygame.display.quit()
    pygame.quit()


pygame.init()
screen_width = 800
screen_height = 600
window = pygame.display.set_mode((screen_width,screen_height))
player_input = PlayerInput()
gameState = GameState()
main_loop()


