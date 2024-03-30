import pygame
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, offset):
        super().__init__()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset

        # Loading image from Graphics folder (Visual representation)
        self.image = pygame.image.load("Graphics/spaceship.png")
        
        # Creating rectangle region for the loaded image and position in bottom middle of screen
        self.rect = self.image.get_rect(midbottom = ((screen_width + self.offset)/2, screen_height))

        # Creating speed
        self.speed = 6

        # Creating group for lasers
        self.lasers_group = pygame.sprite.Group()

        # Laser is initially ready to fire
        self.laser_ready = True

        # Time has passed since the last shot
        self.laser_time = 0

        # Time delay between shots
        self.laser_delay = 600

        # Laser sounds
        self.laser_sound = pygame.mixer.Sound("Sound/laser.ogg")

    def get_user_input(self):
        keys = pygame.key.get_pressed()

        # Moving spaceship right
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Moving spaceship left
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        
        # Shoots laser
        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.screen_height)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def update(self):
        self.get_user_input()
        self.contrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    # Function for keeping movement within the game screen
    def contrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < self.offset:
            self.rect.left = self.offset

    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
        self.lasers_group.empty()