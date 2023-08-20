import pygame

# initializing all the imported pygame modules
pygame.init()

# displaying a window (Max dimensions: 1280 x 720 px)
win_height = 500
win_width = 800
screen = pygame.display.set_mode((win_width, win_height), 
                                 pygame.RESIZABLE)

# set title
pygame.display.set_caption('Irregular Trooper')

# game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# quit pygame after closing window
pygame.quit()