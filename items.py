import pygame, maps
from pygame.locals import *
from loader import load_image
from random import randint

HALF_TILE = 500
FULL_TILE = 1000



balls = []
ball_files = ['red.png', 'blue.png', 'green.png']

def initialize():
    for index in range(0, len(ball_files)):
        balls.append(load_image(ball_files[index], True))

class Items(pygame.sprite.Sprite):

#detect collid
    def collision_check(self, car):
        if self.rect.colliderect(car):
            return True
        
        return False


#Find an adequate point to spawn flag.     
    def generate_items(self):
        x = randint(0,9)
        y = randint(0,9)
        while (maps.map_1[y][x] == 5):
            x = randint(0,9)
            y = randint(0,9)
            
        self.x = x * FULL_TILE + HALF_TILE
        self.y = y * FULL_TILE + HALF_TILE
        self.rect.topleft = self.x, self.y

#Reset the item position
    def reset(self):
        self.generate_items()
        
#Initialize.. yes.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = randint(0, len(balls)-1)
        self.image = balls[self.color]
        self.rect = self.image.get_rect()
        self.x = 5
        self.y = 5
        self.generate_items()
        self.rect.topleft = self.x, self.y

#Update the timer and reposition the flag by offset.
    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        
