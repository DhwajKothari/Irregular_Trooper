import pygame
import soldiers
# initializing all the imported pygame modules
pygame.init()

#set framerate
clock = pygame.time.Clock()
FPS = 60

# displaying a window (Max dimensions: 1280 x 720 px)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set title
pygame.display.set_caption('Irregular Trooper')

# # Here we load the image we want to use
# Icon = pygame.image.load('gfglogo.png')
 
# # We use set_icon to set new icon
# pygame.display.set_icon(Icon)

BG = (230, 120, 80)
def drawBG():
    screen.fill(BG)


# game loop
running = True

player = soldiers.Soldier('player', 200, 200, 3)
enemy = soldiers.Soldier('enemy', 400, 200, 3)

while running:
    clock.tick(FPS)
    drawBG()
    
    player.move()
    player.draw(screen)
    enemy.draw(screen)

    #event handler loop
    for event in pygame.event.get():

        #quit game
        if event.type == pygame.QUIT:
            running = False
        
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.moveRight = True
            if event.key == pygame.K_a:
                player.moveLeft = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.moveRight = False
            if event.key == pygame.K_a:
                player.moveLeft = False
    
    
    # The pygame.display.flip() method is used
    # to update content on the display screen
    pygame.display.flip()


# quit pygame after closing window
pygame.quit()