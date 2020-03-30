# Indsæt score tæller

# Definer scoretæller og sæt til 0
class GameState:
  def __init__(self):
    ...
    self.score = 0

# Tæl score
class GameState:
  def update(self, player_input):
    ...
    for shot in list(self.player_shots):
      if self.alien.rect.colliderect(shot.rect):
        ...
        self.score += 100
        self.player_shots.remove(shot)  

    for bomb in list(self.bombs):
      for shot in self.player_shots:
        if bomb.rect.colliderect(shot.rect):
          ...
          self.score += 10
          self.player_shots.remove(shot) 

    for bomb in list(self.bombs):
      else:
        for city in list(self.cities):
          if bomb.rect.colliderect(city.rect):
            self.score -= 50

# Put score på skærmen
def paint_screen(window, start_ticks):
  ...
  scoreStr = font.render("Score: " + str(game_state.score), True, (0,0,0),(128,128,128))
  scoreRect = scoreStr.get_rect()  
  scoreRect.bottomleft = (0, screen_height) 
  window.blit(scoreStr, scoreRect)   

  pygame.display.flip()

# Giv vinduet et navn
def main_loop():
  ...
  pygame.display.set_caption('Sideways') 

# Vælg bogstavtyper
font = pygame.font.Font('freesansbold.ttf', 32) 

