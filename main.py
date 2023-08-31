import pygame
import os
# import gameVariables as gv

# initializing all the imported pygame modules
pygame.init()

#set framerate
clock = pygame.time.Clock()
FPS = 60

# Game Variables
GRAVITY = 0.75

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

# player action variable
shoot = False
grenade = False

# load images
# bullet & grenade
bullet_img = pygame.image.load('resources/images/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('resources/images/icons/grenade.png').convert_alpha()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        #move bullet 
        self.rect.x += (self.speed * self.direction) 
        # check if bullet has gone off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        
        #check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                self.kill()
                player.health -= 10

        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                self.kill()
                enemy.health -= 25

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer  = 80
        self.vel_y = -10
        self.speed = 8
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        # parabolic throw of grenade 
        self.vel_y += GRAVITY
        dx = (self.speed * self.direction)
        dy= self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            dx = 0

        # check collision with walls & bounce the bomb
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = (self.speed * self.direction)
        
        # #check collision with characters
        # if pygame.sprite.spritecollide(player, bullet_group, False):
        #     if player.alive:
        #         self.kill()
        #         player.health -= 10

        # if pygame.sprite.spritecollide(enemy, bullet_group, False):
        #     if enemy.alive:
        #         self.kill()
        #         enemy.health -= 25
        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'resources/images/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width()*scale),int(img.get_height()*scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    # def update(self):
    #     # parabolic throw of grenade 
    #     self.vel_y += GRAVITY
    #     dx = (self.speed * self.direction)
    #     dy= self.vel_y

    #     # check collision with floor
    #     if self.rect.bottom + dy > 300:
    #         dy = 300 - self.rect.bottom
    #         dx = 0

    #     # check collision with walls & bounce the bomb
    #     if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
    #         self.direction *= -1
    #         dx = (self.speed * self.direction)
        
    #     # #check collision with characters
    #     # if pygame.sprite.spritecollide(player, bullet_group, False):
    #     #     if player.alive:
    #     #         self.kill()
    #     #         player.health -= 10

    #     # if pygame.sprite.spritecollide(enemy, bullet_group, False):
    #     #     if enemy.alive:
    #     #         self.kill()
    #     #         enemy.health -= 25
    #     # update grenade position
    #     self.rect.x += dx
    #     self.rect.y += dy


# create sprite groups
bullet_group = pygame.sprite.Group()    
grenade_group = pygame.sprite.Group()    
explosion_group = pygame.sprite.Group()    

BG = (230, 120, 80)
RED = (255, 0, 0)

def drawBG():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        # Image for soldier
        self.char_type = char_type
        self.alive = True
        self.speed = 2
        self.ammo = ammo
        self.start_ammo = ammo
        self.grenades = grenades
        self.start_grenades = grenades
        self.grenade_thrown = False
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.vel_y = 0
        self.direction = 1
        self.jump = False
        self.in_air = True 
        self.flip = False
        self.moveRight = False
        self.moveLeft = False   
        # Hardcoded action values, make action string value and parse it dynamically.    
        self.animation_list = []
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
        # load all images for the player animation
        animation_types = ["Idle", "Run", "Jump", "Death"]
        for animation in animation_types:
            temp_list = []
            # count of number of files in folder
            num_of_frames = len(os.listdir(f'resources/images/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'resources/images/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width()*scale),int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1      
        if self.grenade_thrown:
            pass

    def move(self):
        dx = 0
        dy = 0
        if self.moveLeft:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if self.moveRight:
            dx = +self.speed
            self.flip = False
            self.direction = 1
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

        def shoot(self):
            if self.shoot_cooldown == 0 and self.ammo > 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                bullet_group.add(bullet)
                #reduce ammo
                self.ammo -= 1

    def shoot(self):
        if self.shoot_cooldown==0 and self.ammo > 0:
            bullet = Bullet((self.rect.centerx + (0.6 * self.rect.size[0] * self.direction)), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.shoot_cooldown = 20
            self.ammo -= 1

    def throw_grenade(self):
        if not self.grenade_thrown and self.grenades > 0:
            grenade = Grenade((self.rect.centerx + (0.5 * self.rect.size[0] * self.direction)), self.rect.top, self.direction)
            grenade_group.add(grenade)
            self.grenade_thrown = True
            self.grenades -= 1

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #delay between updates.
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #resetting animation loop
        if self.frame_index >= len(self.animation_list[self.action]):
            # check if action is Death, then dont loop
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, self.rect)
    


# game loop
running = True

player = Soldier('player', 200, 200, 3, 20, 8)
enemy = Soldier('enemy', 400, 200, 3, 40, 0)

while running:
    clock.tick(FPS)
    drawBG()
    
    player.update()
    player.draw(screen)
    enemy.update()
    enemy.draw(screen)

    # update and draw groups
    bullet_group.update()
    grenade_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)

    # update player actions 
    if player.alive:
        if shoot:
            player.shoot()
        if grenade:
            player.throw_grenade()
        if player.in_air:
            player.update_action(2) #2:jump
        elif player.moveLeft or player.moveRight:
            player.update_action(1) #1:run
        else:
            player.update_action(0) #0:Idle
    # else:
    #     pass
        # player.update_action(3)
    player.move()

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
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_ESCAPE:
                running = False

        # keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.moveRight = False
            if event.key == pygame.K_a:
                player.moveLeft = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
    
    # The pygame.display.flip() method is used
    # to update content on the display screen
    pygame.display.flip()


# quit pygame after closing window
pygame.quit()