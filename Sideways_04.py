import pygame
import math

def calculate_x_velocity(position, target, velocity):
    direction = math.atan2(target[1] - position[1], target[0] - position[0])
    return velocity * math.cos(direction)


def calculate_y_velocity(position, target, velocity):
    direction = math.atan2(target[1] - position[1], target[0] - position[0])
    return velocity * math.sin(direction)




class PlayerInput:
    def __init__(self):
        self.stop = False
        self.left = False
        self.right = False
        self.fire = False

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
        self.fire = pygame.mouse.get_pressed()[0]

class Player:
    def __init__(self):
        self.playerImage = pygame.image.load("player.png").convert_alpha()
        self.playerShotImage = pygame.image.load("shot.png").convert_alpha()
        self.crosshairImage = pygame.image.load("crosshair.png").convert_alpha()
        self.rect = self.playerImage.get_rect(bottomleft=(0, window.get_height()))
        self.alive = True 
        self.shots = []
        self.player_has_fired = False


    def move(self, player_input):
        if player_input.left and self.rect.left > window.get_rect().left:
            self.rect.x = self.rect.x - 2
        if player_input.right and self.rect.right < window.get_rect().right:
            self.rect.x = self.rect.x + 2


        for shot in list(self.shots):
            shot.move()
            if not shot.rect.colliderect(window.get_rect()):
                self.shots.remove(shot)



        if not player_input.fire:
            self.player_has_fired = False





    def hit(self):
        self.alive = False



class Shot:
    def __init__(self, rect, x_speed, y_speed):
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self.x_speed = x_speed
        self.y_speed = y_speed

    def move(self):
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y


class Alien:
    def __init__(self, speed_x):
        self.alienImage = pygame.image.load("alien.png").convert_alpha()
        self.rect = self.alienImage.get_rect(topright=(0,0))
        self.x = self.rect.x
        self.speed_x = speed_x
        self.bounds = window.get_rect()
        self.direction = 1
        self.alive = True


    def move(self):
        self.x = self.x + self.direction * self.speed_x
        self.rect.x = self.x
        if self.rect.right > self.bounds.right:
            self.direction = -1
        if self.rect.left < self.bounds.left:
            self.direction = 1

    def hit(self):
        self.alive = False


class GameState:
    def __init__(self):
        self.player = Player()
        self.alien = Alien(1.0)
        self.player_shots = []
        self.player_has_fired = False

    def update(self, player_input):
        self.player.move(player_input)
        self.alien.move()
        for shot in list(self.player_shots):
            shot.move()
            if not shot.rect.colliderect(window.get_rect()):
                self.player_shots.remove(shot)


        for shot in list(self.player_shots):
            if self.alien.rect.colliderect(shot.rect):
                self.alien.hit()                            

        print(player_input.fire , self.player_has_fired , len(self.player_shots) < 3 , self.player.alive)

        if player_input.fire and not self.player_has_fired and len(self.player_shots) < 3 and self.player.alive:
            self.player_has_fired = True
            self.add_shot()
        if not player_input.fire:
            self.player_has_fired = False



    def add_shot(self):
        pos = self.player.rect.center
        new_shot_rect = self.player.playerShotImage.get_rect(center=pos)
        target = pygame.mouse.get_pos()
        velocity = 1.5
        velocity_x = calculate_x_velocity(pos, target, velocity)
        velocity_y = calculate_y_velocity(pos, target, velocity)
        new_shot = Shot(new_shot_rect, velocity_x, velocity_y)
        self.player_shots.append(new_shot)



def paint_screen(window):
    window.fill((0,0,0))
    window.blit(game_state.player.playerImage, game_state.player.rect)
    if game_state.alien.alive:
        window.blit(game_state.alien.alienImage, game_state.alien.rect)
    for shot in game_state.player_shots:
        window.blit(game_state.player.playerShotImage, shot.rect)
    window.blit(game_state.player.crosshairImage, 
        game_state.player.crosshairImage.get_rect(center=pygame.mouse.get_pos()))
    pygame.display.flip()

def main_loop():
    pygame.mouse.set_visible(False)
    while not player_input.stop:
        pygame.time.delay(20)
        player_input.update()
        game_state.update(player_input)
        paint_screen(window)
    pygame.display.quit()
    pygame.quit()


pygame.init()
screen_width = 800
screen_height = 600
window = pygame.display.set_mode((screen_width,screen_height))
player_input = PlayerInput()
game_state = GameState()
main_loop()


