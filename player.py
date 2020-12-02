#The MIT License (MIT)

#Copyright (c) 2012 Robin Duda, (chilimannen)

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

#Camera module will keep track of sprite offset.

#Player module, the car.
import os, sys, pygame, math, maps
from pygame.locals import *
from random import randint
from loader import load_image

GRASS_SPEED = 0.715
GRASS_GREEN = 90
CENTER_X = -1
CENTER_Y = -1
ITEM_DURATION = 640


#Rotate car.
def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

#이미지를 확대하여 리턴 하는 함수
def big_image(image, rect):
        """rotate an image while keeping its center"""
        big_image = pygame.transform.scale(image, (150, 300))
        big_rect = big_image.get_rect(center=rect.center)
        return big_image, big_rect

def findspawn():
    x = randint(0,9)
    y = randint(0,9)
    while(maps.map_1[y][x] == 5):
            x = randint(0,9)
            y = randint(0,9)
    return x * 1000 + CENTER_X, y * 1000 + CENTER_Y

#define car as Player.
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('car_player.png')
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        CENTER_X =  int(pygame.display.Info().current_w /2)
        CENTER_Y =  int(pygame.display.Info().current_h /2)
        self.x = CENTER_X
        self.y = CENTER_Y
        self.rect.topleft = self.x, self.y
        self.x, self.y = findspawn()
        self.dir = 0
        self.speed = 0.0
        self.maxspeed = 11.5
        self.minspeed = -1.85
        self.acceleration = 0.095
        self.deacceleration = 0.12
        self.softening = 0.04
        self.steering = 1.60
        self.tracks = False

        self.green_ball = False     
        self.green_timer = 0
        self.red_ball   = False
        self.red_timer = 0
        self.blue_ball  = False
        self.blue_timer = 0

        self.big = False                #현제 크기 상태
        self.temp = self.image_orig     #save orignal_image (bigger)


#Reset the car.
    def reset(self):

        #reset items
        self.green_ball = False     
        self.green_timer = 0
        self.red_ball   = False
        self.red_timer = 0
        self.blue_ball  = False
        self.blue_timer = 0

        self.bigger()

        self.x =  int(pygame.display.Info().current_w /2)
        self.y =  int(pygame.display.Info().current_h /2)
        self.speed = 0.0
        self.dir = 0
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        self.rect.topleft = self.x, self.y
        self.x, self.y = findspawn()
            
#Emit tracks..
    def emit_tracks(self):
        self.tracks = True
        
#Don't emit tracks..
    def reset_tracks(self):
        self.tracks = False

#If the car is on grass, decrease speed and emit tracks. 그린볼을 먹었을시에는 감소 x
    def grass(self, value):
            if value > GRASS_GREEN and self.green_timer == False :
                if self.speed - self.deacceleration > GRASS_SPEED * 2:
                    self.speed = self.speed - self.deacceleration * 2
                    self.emit_tracks()

#Push back on impact.
    def impact(self):
        if self.speed > 0 :
            self.speed = self.minspeed

    def soften(self):
            if self.speed > 0:
                self.speed -= self.softening
            if self.speed < 0:
                self.speed += self.softening

#Accelerate the vehicle
    def accelerate(self):
        if self.speed < self.maxspeed :
            self.speed = self.speed + self.acceleration
            if self.speed < self.maxspeed / 3:
                self.emit_tracks()
        


#Deaccelerate.
    def deaccelerate(self):
        if self.speed > self.minspeed:
            self.speed = self.speed - self.deacceleration
            self.emit_tracks()

#Steer. 레드 볼을 먹을시 핸들링 속도 증가
    def steerleft(self):
        if self.red_ball == True :
                self.dir = self.dir + (self.steering * 2)
        else :
            self.dir = self.dir+self.steering
            
        if self.dir > 360:
            self.dir = 0
        if (self.speed > self.maxspeed / 2):
            self.emit_tracks()
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

#Steer.
    def steerright(self):
        if self.red_ball == True :
                self.dir = self.dir - (self.steering * 2)
        else :
            self.dir = self.dir-self.steering

        if self.dir < 0:
            self.dir = 360
        if (self.speed > self.maxspeed / 2):
            self.emit_tracks()   
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

#fix this function 
    def update(self, last_x, last_y):
        self.x = self.x + self.speed * math.cos(math.radians(270-self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270-self.dir))
        self.reset_tracks()

        #check bigger 
        self.bigger()

        #item timer update
        if self.green_ball == True and self.green_timer > 0 :
            self.green_timer = self.green_timer - 1

        elif self.green_ball == True and self.green_timer == 0 :
            self.green_ball = False

        if self.blue_ball == True and self.blue_timer > 0 :
            self.blue_timer = self.blue_timer - 1

        elif self.blue_ball == True and self.blue_timer == 0 :
            self.blue_ball = False

        if self.red_ball == True and self.red_timer > 0 :
            self.red_timer = self.red_timer - 1

        elif self.red_ball == True and self.red_timer == 0 :
            self.red_ball = False
        
#get item
    def get_item(self, color) :
        if color == 0 :         #get red ball
            if self.red_ball == True :
                self.red_timer = ITEM_DURATION
            elif self.red_ball == False :
                self.red_ball = True
                self.red_timer = ITEM_DURATION 
        
        elif color == 1 :       #get blue ball
            if self.blue_ball == True :
                self.blue_timer = ITEM_DURATION
            elif self.blue_ball == False :
                self.blue_ball = True
                self.blue_timer = ITEM_DURATION     

        elif color == 2 :       #get green ball
            if self.green_ball == True :
                self.green_timer = ITEM_DURATION
            elif self.green_ball == False :
                self.green_ball = True
                self.green_timer = ITEM_DURATION

#bigger if get blue_ball
    def bigger(self) :
        if self.blue_ball == True and self.big ==False :
            self.big = True
            self.image_orig, self.rect = big_image(self.image_orig, self.rect)
            self.image = self.image_orig
            self.image, self.rect = rot_center(self.image, self.rect, self.dir)

        elif self.blue_ball == False and self.big == True :
            self.big = False
            self.image_orig = self.temp