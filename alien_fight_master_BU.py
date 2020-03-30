import pygame
import math
import random
import time

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
        for this_event in events:
            if this_event.type == pygame.QUIT:
                self.stop = True
            elif this_event.type == pygame.KEYDOWN:
                if this_event.key == pygame.K_a:
                    self.left = True
                if this_event.key == pygame.K_d:
                    self.right = True
            elif this_event.type == pygame.KEYUP:
                if this_event.key == pygame.K_a:
                    self.left = False
                if this_event.key == pygame.K_d:
                    self.right = False
        self.fire = pygame.mouse.get_pressed()[0]


class Images:
    def __init__(self):
        self.player = pygame.image.load("player.png").convert_alpha()
        self.city = pygame.image.load("grey_city.png").convert_alpha()
        self.enemy_bomb = pygame.image.load("enemy_bomb.png").convert_alpha()
        self.shot = pygame.image.load("shot.png").convert_alpha()
        self.crosshair = pygame.image.load("crosshair.png").convert_alpha()
        self.alien = pygame.image.load("alien.png").convert_alpha()
        self.alien_shot = pygame.image.load("alien_shot.png").convert_alpha()


class Player:
    def __init__(self, rect, bounds):
        self.rect = rect
        self.bounds = bounds
        self.alive = True

    def move(self, player_input):
        if player_input.left and self.rect.left > self.bounds.left:
            self.rect.x = self.rect.x - 1
        if player_input.right and self.rect.right < self.bounds.right:
            self.rect.x = self.rect.x + 1

    def hit(self):
        self.alive = False


class City:
    def __init__(self, rect):
        self.rect = rect


class Alien:
    def __init__(self, rect, speed_x, bounds, shot_image):
        self.rect = rect
        self.x = rect.x
        self.speed_x = speed_x
        self.bounds = bounds
        self.shot_image = shot_image
        self.direction = 1
        self.time_to_shoot = random.randint(100, 1000)

    def move(self):
        self.x = self.x + self.direction * self.speed_x
        self.rect.x = self.x
        if self.rect.right > self.bounds.right:
            self.direction = -1
        if self.rect.left < self.bounds.left:
            self.direction = 1

    def maybe_shoot(self, player, shot_list):
        self.time_to_shoot = self.time_to_shoot - 1
        if self.time_to_shoot <= 0 and player.alive:
            self.time_to_shoot = random.randint(100, 1000)
            rect = self.shot_image.get_rect(center=self.rect.midbottom)
            speed = 1
            x_speed = calculate_x_velocity(self.rect.midbottom, player.rect.center, speed)
            y_speed = calculate_y_velocity(self.rect.midbottom, player.rect.center, speed)
            shot = Shot(rect, x_speed, y_speed)
            shot_list.append(shot)


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


class Bomb:
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


class GameState:
    def __init__(self, images, screen):
        self.images = images
        self.screen = screen
        cities_top = images.city.get_height()
        player_rect = images.player.get_rect(bottomleft=(0, screen.get_height() - cities_top))
        self.player = Player(player_rect, screen.get_rect())

        self.bombs = []
        self.cities = []
        self.aliens = []
        self.alien_shots = []
        number_of_cities = 5
        city_distance = screen.get_width() // (number_of_cities + 1)
        for city_number in range(number_of_cities):
            left = (city_number + 1) * city_distance - images.city.get_width() / 2
            rect = images.city.get_rect(bottomleft=(left, screen.get_height()))
            new_city = City(rect)
            self.cities.append(new_city)

        self.shots = []
        self.player_has_fired = False

    def update(self, player_input):
        self.player.move(player_input)

        if self.cities and random.randint(1, 1000) > 999:
            x = random.randint(0, self.screen.get_width())
            y = 0
            pos = (x, y)
            target = random.choice(self.cities).rect.midbottom
            velocity = random.uniform(0.1, 0.5)
            velocity_x = calculate_x_velocity(pos, target, velocity)
            velocity_y = calculate_y_velocity(pos, target, velocity)
            rect = self.images.enemy_bomb.get_rect(center=pos)
            new_bomb = Bomb(rect, velocity_x, velocity_y)
            self.bombs.append(new_bomb)

        for bomb in self.bombs:
            bomb.move()

        for shot in list(self.shots):
            shot.move()
            if not shot.rect.colliderect(self.screen.get_rect()):
                self.shots.remove(shot)

        for shot in list(self.alien_shots):
            shot.move()

        if player_input.fire and not self.player_has_fired and len(self.shots) < 3 and self.player.alive:
            self.player_has_fired = True
            self.add_shot()
        if not player_input.fire:
            self.player_has_fired = False

        for alien in list(self.aliens):
            for shot in list(self.shots):
                if alien.rect.colliderect(shot.rect):
                    self.aliens.remove(alien)

        for shot in self.alien_shots:
            if shot.rect.colliderect(self.player.rect):
                self.player.hit()

        for bomb in list(self.bombs):
            for shot in self.shots:
                if bomb.rect.colliderect(shot.rect):
                    self.bombs.remove(bomb)

        for bomb in list(self.bombs):
            for city in list(self.cities):
                if bomb.rect.colliderect(city.rect):
                    self.cities.remove(city)
                    self.bombs.remove(bomb)
            if bomb.rect.colliderect(self.player.rect):
                self.player.hit()
                self.bombs.remove(bomb)

        for alien in self.aliens:
            alien.move()
            alien.maybe_shoot(self.player, self.alien_shots)

        if self.aliens == []:
            if random.randint(1, 1000) > 999:
                alien_rect = self.images.alien.get_rect(topright=(0,0))
                new_alien = Alien(alien_rect, 0.1, self.screen.get_rect(), self.images.alien_shot)
                self.aliens.append(new_alien)

    def add_shot(self):
        pos = self.player.rect.center
        new_shot_rect = self.images.shot.get_rect(center=pos)
        target = pygame.mouse.get_pos()
        velocity = 1.5
        velocity_x = calculate_x_velocity(pos, target, velocity)
        velocity_y = calculate_y_velocity(pos, target, velocity)
        new_shot = Shot(new_shot_rect, velocity_x, velocity_y)
        self.shots.append(new_shot)


def paint_screen(screen, game_state, images):
    screen.fill((0, 0, 0))
    if game_state.player.alive:
        screen.blit(images.player, game_state.player.rect)
    for city in game_state.cities:
        screen.blit(images.city, city.rect)
    for bomb in game_state.bombs:
        screen.blit(images.enemy_bomb, bomb.rect)
    for shot in game_state.shots:
        screen.blit(images.shot, shot.rect)
    for shot in game_state.alien_shots:
        screen.blit(images.alien_shot, shot.rect)
    for alien in game_state.aliens:
        screen.blit(images.alien, alien.rect)
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(images.crosshair, images.crosshair.get_rect(center=mouse_pos))
    pygame.display.flip()


def main_loop(screen):
    pygame.mouse.set_visible(False)
    player_input = PlayerInput()
    images = Images()
    game_state = GameState(images, screen)
    while not player_input.stop:
        paint_screen(screen, game_state, images)
        player_input.update()
        game_state.update(player_input)
        time.sleep(.0050)


pygame.init()
s = pygame.display.set_mode((800, 600))
main_loop(s)
pygame.quit()
