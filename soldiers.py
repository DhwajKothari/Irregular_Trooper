import pygame

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        # Image for soldier
        self.char_type = char_type
        self.speed = 2
        self.direction = 1 
        self.flip = False
        self.moveRight = False
        self.moveLeft = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(5):
            img = pygame.image.load(f'resources/images/{self.char_type}/Idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width()*scale),int(img.get_height()*scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)



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

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, self.rect)
    
