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

import sqlite3
import os, sys, pygame, random, array, gamemode
import direction,  bounds, timeout, menu
from pygame.locals import *

#Import game modules.
from loader import load_image
import player, maps, traffic, camera, tracks, items


TRAFFIC_COUNT = 45
ITEM_COUNT = 10
CENTER_W = -1
CENTER_H = -1

#맵을 바꾸기 위한 함수
def change_map(map_s, maps, type) :
    map_s.empty()
    maps.map_files.clear()
    for tile_num in range (0, len(maps.map_tile[type])):
        maps.map_files.append(load_image(maps.map_tile[type][tile_num], False))
    for x in range (0, 10):
        for y in range (0, 10):
            map_s.add(maps.Map(maps.map_1[x][y], x * 1000, y * 1000, maps.map_1_rot[x][y]))


#Main function.
def main():

#database
    record_switch = False
    text_rank = []
    textpos_rank = []

#start music
    pygame.mixer.music.load('./media/background.wav')
    pygame.mixer.music.play(-1)

#initialize objects.
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 32)
    car = player.Player()
    cam = camera.Camera()
    target = gamemode.Finish()
    item = []
    traffics = []
    bound_alert = bounds.Alert()
    time_alert = timeout.Alert()
    info = menu.Alert()
    pointer = direction.Tracker(int(CENTER_W * 2), int(CENTER_H * 2))
#create sprite groups.
    map_s     = pygame.sprite.Group()
    player_s  = pygame.sprite.Group()
    traffic_s = pygame.sprite.Group()
    tracks_s  = pygame.sprite.Group()
    target_s  = pygame.sprite.Group()
    item_s    = pygame.sprite.Group()
    pointer_s = pygame.sprite.Group()
    timer_alert_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()
    menu_alert_s = pygame.sprite.Group()

#generate tiles     기본 맵 초원
    for tile_num in range (0, len(maps.map_tile[0])):
        maps.map_files.append(load_image(maps.map_tile[0][tile_num], False))
    for x in range (0, 10):
        for y in range (0, 10):
            map_s.add(maps.Map(maps.map_1[x][y], x * 1000, y * 1000, maps.map_1_rot[x][y]))

#load tracks
    tracks.initialize()
#load finish
    target_s.add(target)
#load items
    items.initialize()
    for count in range(0, ITEM_COUNT):
        item.append(items.Items())
        item_s.add(item[count])
#load direction
    pointer_s.add(pointer)
#load alerts
    timer_alert_s.add(time_alert)
    bound_alert_s.add(bound_alert)
    menu_alert_s.add(info)
#load traffic
    traffic.initialize(CENTER_W, CENTER_H)
    for count in range(0, TRAFFIC_COUNT):
        traffics.append(traffic.Traffic())
        traffic_s.add(traffics[count])

    player_s.add(car)

    cam.set_pos(car.x, car.y)

    while running:
#Render loop.

#Check for menu/reset, (keyup event - trigger ONCE)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if keys[K_m]:
                    if (info.visibility == True):
                        info.visibility = False
                    else:
                        info.visibility = True

                if info.visibility == True :
                    if (keys[K_p]):
                        car.reset()
                        target.reset()
                        for i in range(0 ,ITEM_COUNT) :
                            item[i].reset
                        record_switch = False

                    if (keys[K_q]):
                        pygame.quit()
                        sys.exit(0)
                
                    if (keys[K_1]):
                        change_map(map_s, maps, 0)
                        car.reset()
                        target.reset()
                        for i in range(0 ,ITEM_COUNT) :
                            item[i].reset

                    if (keys[K_2]):
                        change_map(map_s, maps, 1)
                        car.reset()
                        target.reset()
                        for i in range(0 ,ITEM_COUNT) :
                            item[i].reset
                        
                    if (keys[K_3]):
                        change_map(map_s, maps, 2)
                        car.reset()
                        target.reset()
                        for i in range(0 ,ITEM_COUNT) :
                            item[i].reset        

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

#Check for key input. (KEYDOWN, trigger often)
        keys = pygame.key.get_pressed()
        if (target.timeleft > 0):
            if keys[K_LEFT]:
                car.steerleft()
            if keys[K_RIGHT]:
                car.steerright()
            if keys[K_UP]:
                car.accelerate()
            else:
                car.soften()
            if keys[K_DOWN]:
                car.deaccelerate()

        cam.set_pos(car.x, car.y)

#Show text data.
        text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (224, 16, 16))
        textpos_fps = text_fps.get_rect(centery=175, centerx=260)

        text_score = font.render('Score: ' + str(target.score), 1, (224, 16, 16))
        textpos_score = text_fps.get_rect(centery=205, centerx=260)

        text_timer = font.render('Timer: ' + str(int((target.timeleft / 60)/60)) + ":" + str(int((target.timeleft / 60) % 60)), 1, (224, 16, 16))
        textpos_timer = text_fps.get_rect(centery=235, centerx=260)

        text_red_ball = font.render('Red Ball: ' + str(int(car.red_timer / 64)), 1, (224, 16, 16))
        textpos_red_ball = text_fps.get_rect(centery=265, centerx=260)

        text_blue_ball = font.render('Blue Ball: ' + str(int(car.blue_timer / 64)), 1, (224, 16, 16))
        textpos_blue_ball = text_fps.get_rect(centery=295, centerx=260)

        text_green_ball = font.render('Green Ball: ' + str(int(car.green_timer / 64)), 1, (224, 16, 16))
        textpos_green_ball = text_fps.get_rect(centery=325, centerx=260)

        text_ranking = font.render('TOP 5 Ranking', 1, (16, 224, 16))
        textpos_ranking = text_fps.get_rect(centery=CENTER_H, centerx=CENTER_W-20)

        text_boundtimer = font.render('Game over After ' + str(int(bound_alert.timeleft / 64)) + ' Second.', 1, (224,16,16))
        textpos_boundtimer = text_fps.get_rect(centery=CENTER_H+30, centerx=CENTER_W-100)

#Render Scene.
        screen.blit(background, (0,0))

        #cam.set_pos(car.x, car.y)

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)
        
#Conditional renders/effects
        car.grass(screen.get_at(((int(CENTER_W-5), int(CENTER_H-5)))).g)
        if (car.tracks):
            tracks_s.add(tracks.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

#Just render..
        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)
        
        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        traffic_s.update(cam.x, cam.y)
        traffic_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        item_s.update(cam.x, cam.y)
        item_s.draw(screen)

        pointer_s.update(car.x + CENTER_W, car.y + CENTER_H, target.x, target.y)
        pointer_s.draw(screen)

#Conditional renders.

        if (bounds.breaking(car.x+CENTER_W, car.y+CENTER_H) == True):
            bound_alert_s.update()
            bound_alert_s.draw(screen)
            bound_alert.update()
            screen.blit(text_boundtimer, textpos_boundtimer)
            if(bound_alert.timeleft == 0):
                target.timeleft = 0

        else :
            bound_alert.timeleft = 640


        if (target.timeleft == 0):
            timer_alert_s.draw(screen)
            car.speed = 0
            text_score = font.render('Your Score: ' + str(target.score), 1, (224, 16, 16))
            textpos_score = text_fps.get_rect(centery=CENTER_H-56, centerx=CENTER_W-20)


            if record_switch == False:
                cur.execute("SELECT * From rank ORDER BY Point DESC")
                dataList = []
                dataList = cur.fetchall()
                rank = 0

                if len(dataList) == 0:
                    cur.execute("INSERT INTO rank VALUES(?,?)", (1, target.score))

                elif len(dataList) < 5:
                    for i in dataList:
                        if i[1] < target.score :
                            rank = i[0]
                            break
                    
                    if rank!=0:
                        cur.execute("UPDATE rank SET Rank=Rank+1 WHERE Point < %d" %(target.score))
                        cur.execute("INSERT INTO rank VALUES(?,?)", (rank, target.score))

                    else :
                        cur.execute("INSERT INTO rank VALUES(?,?)", (len(dataList)+1, target.score))

                
                elif len(dataList) >= 5:
                    for i in dataList:
                        if i[1] < target.score :
                            rank = i[0]
                            break

                    if rank != 0 :
                        cur.execute("UPDATE rank SET Rank=Rank+1 WHERE Point<%d" % (target.score))
                        cur.execute("INSERT INTO rank VALUES(?,?)", (rank, target.score))
                        cur.execute("DELETE FROM rank WHERE Rank > 5")
                
                con.commit()
                cur.execute("SELECT * From rank ORDER BY Rank ASC")
                dataList = cur.fetchall()

                cnt = 0

                text_rank.clear()
                textpos_rank.clear()
                
                for i in dataList:
                    cnt=cnt+1
                    text_rank.append(font.render(str(i[0]) + '. ' + str(i[1]), 1, (16, 224, 16)))
                    textpos_rank.append(text_fps.get_rect(centery=CENTER_H+25+cnt*25, centerx=CENTER_W-20))

                record_switch = True

        if (info.visibility == True):
            menu_alert_s.draw(screen)
            
#Blit Blit..       
        screen.blit(text_fps, textpos_fps)
        screen.blit(text_score, textpos_score)
        screen.blit(text_timer, textpos_timer)
        screen.blit(text_red_ball, textpos_red_ball)
        screen.blit(text_blue_ball, textpos_blue_ball)
        screen.blit(text_green_ball, textpos_green_ball)
        if record_switch == True :

            screen.blit(text_ranking, textpos_ranking)
            for i in range(0, cnt):
                screen.blit(text_rank[i], textpos_rank[i])
        pygame.display.flip()

#Check collision!!!

        #traffic 과의 충돌 확인. 블루볼 먹었을 시에는 충돌 없음
        for i in range(0, TRAFFIC_COUNT):
            if traffics[i].collision_check(car) == True :
                if car.blue_ball == True:
                    pygame.mixer.Sound.play(point_sound)
                    traffics[i].respawn()
                else :
                    car.impact()
                    target.car_crash()

        if pygame.sprite.spritecollide(car, target_s, True):
            pygame.mixer.Sound.play(point_sound)
            target.claim_flag()
            target.generate_finish()
            target_s.add(target)


        for i in range(0, ITEM_COUNT):
            if item[i].collision_check(car) == True :
                 pygame.mixer.Sound.play(point_sound)
                 car.get_item(item[i].color)           
                 item[i].generate_items()
                 item_s.add(item[i])


            
        clock.tick(64)
        

#initialization
pygame.init()

screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),
                                pygame.FULLSCREEN)


pygame.display.set_caption('Race of Math.')
pygame.mouse.set_visible(False)
font = pygame.font.Font(None, 32)

CENTER_W =  int(pygame.display.Info().current_w /2)
CENTER_H =  int(pygame.display.Info().current_h /2)

#new background surface
background = pygame.Surface(screen.get_size())
background = background.convert_alpha()
background.fill((26, 26, 26))

#sound effects
global point_sound
point_sound = pygame.mixer.Sound('./media/point.wav')

#database for rank system
con = sqlite3.connect("rank.db")
cur = con.cursor()
record_switch = False


#Enter the mainloop.
main()

con.close()
pygame.quit()
sys.exit(0)













        

