import pygame
pygame.init() 
display_surface = pygame.display.set_mode((800, 600 )) 
pygame.display.set_caption('Show Text') 
font = pygame.font.Font('freesansbold.ttf', 32) 
count = 0

while True : 
    count += 1
    display_surface.fill((0,0,0))
    text = font.render(str(count), True, (128,128,128), (0,0,0)) 
    textRect = text.get_rect() 
    display_surface.blit(text, textRect) 
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit() 
            quit() 
        pygame.display.update() 
