# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 23:43:22 2020

@author: sunidhi
"""

import pygame
import random
import math
from pygame import mixer
from pygame.locals import*



#intialize the pygame
pygame.init()

#to create screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load("background.png")

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and icon
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)


#player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append( random.randint(50,150))
    enemyX_change.append(10)
    enemyY_change.append(40)

#bullet
#ready = you cant see the bullet on screen
#fire = the bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"

#score value
score_value = 0
font = pygame.font.Font('freesansbold.ttf' , 32)
textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

#game over text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

#show the score on screen
def show_score(x,y):
    score = font.render("SCORE : " + str(score_value) , True , (255 ,255 ,255))
    screen.blit(score , (x, y))

#to show player -spaceship
def player(x , y):
    screen.blit(playerImg , (x, y))
    
#to show enemy    
def enemy(x , y , i):
    screen.blit(enemyImg[i] , (x, y))    
 
#to show bullet    
def fire_bullet(x,y):
    global bullet_state
    bullet_state ="fire"
    screen.blit(bulletImg , (x+16 , y+10))  #coordinate so bullet comes from the centre of the spaceship  

#if collision occured or not  
def isCollision(enemyX , enemyY , bulletX , bulletY) :
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))    
    if distance < 27:
        return True
    else:
        return False
    
    
    
#Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background , (0,0))
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
         #if key stroke is pressed whether its right or left
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change = -12
            if event.key==pygame.K_RIGHT:
                playerX_change = 12
            if event.key==pygame.K_SPACE:
                if bullet_state =="ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    #get the current/intial value of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX , bulletY )
        if event.type==pygame.KEYUP:
             if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                 playerX_change = 0
            
    playerX += playerX_change
   
    #Boundaries for x axis png size is 64px so we subtract 800-64=736
    if playerX <=0:
        playerX = 0
        
    elif playerX >=736:
        playerX = 736
        
    #enemy movement
    for i in range(num_of_enemies):
        
        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        
        
        enemyX[i] += enemyX_change[i]  
       
        if enemyX[i] <=0:
            enemyX_change[i] = 10
            enemyY[i] += enemyY_change[i]
            
        elif enemyX[i] >=736:
            enemyX_change[i] = -10
            enemyY[i] += enemyY_change[i]

        #collision
        collision = isCollision(enemyX[i] , enemyY[i] , bulletX , bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
            
        enemy(enemyX[i] , enemyY[i] , i)
        
        
    #bullet movement  
    if bulletY <=0:
        bulletY =480
        bullet_state = "ready"  
    if bullet_state =="fire":
        fire_bullet(bulletX , bulletY)
        bulletY -= bulletY_change
        
        
   
        
    player(playerX , playerY) 
    show_score(textX , textY)
    pygame.display.update()      