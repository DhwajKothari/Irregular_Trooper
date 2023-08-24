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

# # Here we load the image we want to
# # use
# Icon = pygame.image.load('gfglogo.png')
 
# # We use set_icon to set new icon
# pygame.display.set_icon(Icon)

# game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    color = (255,255,0)
   
    # Drawing Rectangle
    pygame.draw.rect(screen, color,
                    pygame.Rect(30, 30, 60, 60))
    
    # The pygame.display.flip() method is used
    # to update content on the display screen
    pygame.display.flip()


# quit pygame after closing window
pygame.quit()