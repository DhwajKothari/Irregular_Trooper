import pygame
import os
import random
# import gameVariables as gv

# initializing all the imported pygame modules
pygame.init()

#set framerate
clock = pygame.time.Clock()
FPS = 60

# Game Variables
GRAVITY = 0.75
TILE_SIZE = 40

# displaying a window (Max dimensions: 1280 x 720 px)
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 400

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
grenade_thrown = False

# load images
# bullet & grenade
bullet_img = pygame.image.load('resources/images/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('resources/images/icons/grenade.png').convert_alpha()
# Itemboxes
health_box_img = pygame.image.load('resources/images/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('resources/images/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('resources/images/icons/grenade_box.png').convert_alpha()
itemboxes = {
    "Health": health_box_img,
    "Ammo": ammo_box_img,
    "Grenade": grenade_box_img
}

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        # Image for soldier
        self.char_type = char_type
        self.alive = True
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.grenades = grenades
        self.start_grenades = grenades
        # self.grenade_thrown = False
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
        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0
        
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
        # if grenade_thrown:
        #     pass

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
            bullet = Bullet((self.rect.centerx + (0.7 * self.rect.size[0] * self.direction)), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.shoot_cooldown = 20
            self.ammo -= 1

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50
        #check if the player is in vision range
            if self.vision.colliderect(player.rect):
                #stop running
                self.update_action(0)#0: idle
                #shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        self.moveRight = True
                    else:
                        self.moveRight = False
                    self.moveLeft = not self.moveRight
                    self.move()
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    # Attach and update vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False


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
        for enemy in enemy_group:
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
        
        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

        #countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
			#do damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and	\
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                        enemy.health -= 50


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
    
    def update(self):
        EXPLOSION_SPEED = 4
        #update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #if explosion animation is complete, delete it
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]


class ItemBox(pygame.sprite.Sprite):
    def __init__ (self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = itemboxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()))

    def update(self): 
        #check collision with characters
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == "Health":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
                self.kill()
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == "Ammo":
                player.ammo += 15
                self.kill()
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == "Grenade":
                player.grenades += 5
                self.kill()


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    
    def draw(self, health):
        self.health = health
        ratio = 150 * (self.health / self.max_health)
        pygame.draw.rect(screen, BLACK, (self.x - 2 , self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y , 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y , ratio, 20))

# create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()    
grenade_group = pygame.sprite.Group()    
explosion_group = pygame.sprite.Group()    
item_box_group = pygame.sprite.Group()

BG = (230, 120, 80)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# define font
font = pygame.font.SysFont("Futura", 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def drawBG():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

# game loop
running = True
player = Soldier('player', 200, 200, 1.8, 3, 20, 8)
enemy = Soldier('enemy', 400, 250, 1.8, 2, 40, 0)
enemy2 = Soldier('enemy', 300, 250, 1.8, 2, 40, 0)
enemy_group.add(enemy)
enemy_group.add(enemy2)

health_bar = HealthBar(20, 10, player.health, player.max_health)
healthbox = ItemBox("Health", 500, 200)
item_box_group.add(healthbox)
ammobox = ItemBox("Ammo", 600, 200)
item_box_group.add(ammobox)
grenadebox = ItemBox("Grenade", 700, 200)
item_box_group.add(grenadebox)

while running:
    clock.tick(FPS)
    drawBG()
    # Display health bar
    health_bar.draw(player.health)
    # show ammo
    draw_text(f'Ammo: ', font, WHITE, 20, 35)
    for i in range(player.ammo):
        screen.blit(bullet_img, (100 + (i * 10), 40))
    # show grenade
    draw_text(f'Grenade: ', font, WHITE, 20, 60)
    for i in range(player.grenades):
        screen.blit(grenade_img, (120 + (i * 15), 65))

    player.update()
    player.draw(screen)
    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.draw(screen)

    # update and draw groups
    bullet_group.update()
    grenade_group.update()
    explosion_group.update()
    item_box_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)
    item_box_group.draw(screen)

    # update player actions 
    if player.alive:
        if shoot:
            player.shoot()
        if grenade and not grenade_thrown and player.grenades > 0:
            grenade = Grenade((player.rect.centerx + (0.5 * player.rect.size[0] * player.direction)), player.rect.top, player.direction)
            grenade_group.add(grenade)
            grenade_thrown = True
            player.grenades -= 1

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
                grenade_thrown = False
    
    # The pygame.display.flip() method is used
    # to update content on the display screen
    pygame.display.flip()


# quit pygame after closing window
pygame.quit()