

# - Player 1 (Yellow Jet):
#   - Move Up: W
#   - Move Down: S
#   - Move Left: A
#   - Move Right: D
#   - Fire Bullets: Left Shift

# - Player 2 (Blue Jet):
#   - Move Up: Up Arrow
#   - Move Down: Down Arrow
#   - Move Left: Left Arrow
#   - Move Right: Right Arrow
#   - Fire Bullets: Right Alt

import pygame
import os

pygame.font.init()
#Sound
pygame.mixer.init()
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join('Sounds','Fire.mp3'))
BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join('Sounds','Hit.mp3'))

WIDTH,HEIGHT=900,500

FPS=60
VELOCITY=3

HEALTH_FONT=pygame.font.SysFont('comicsans',30)
WINNER_FONT=pygame.font.SysFont('comicsans',100)

WHITE=((255,255,255))
BLUE=((11, 223, 255))
YELLOW=((255,255,0))

YELLOW_HIT=pygame.USEREVENT+1
BLUE_HIT=pygame.USEREVENT+2

MID_BORDER=pygame.Rect((WIDTH/2-2.5,0,5,HEIGHT))
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("CodeRunner Jet Fighters")

BLUEJET=pygame.image.load(os.path.join('Images','BlueJet.png'))
BJET=pygame.transform.rotate(BLUEJET,90)
YELLOWJET=pygame.image.load(os.path.join('Images','YellowJet.png'))
YJET=pygame.transform.rotate(YELLOWJET,270)
SKY=pygame.transform.scale(pygame.image.load(os.path.join('Images','Sky2.png')),(WIDTH,HEIGHT))

BULLET_SPEED=5
BULLET_NUMBER=5

def draw(yellow,blue,yellow_bullets,blue_bullets,yellow_health,blue_health):
    WINDOW.blit(SKY,(0,0))
    pygame.draw.rect(WINDOW,WHITE,MID_BORDER)
    WINDOW.blit(YJET,(yellow.x,yellow.y))
    WINDOW.blit(BJET,(blue.x,blue.y))
    for bullet in blue_bullets:
        pygame.draw.rect(WINDOW,BLUE,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW,YELLOW,bullet)
    yellow_health_txt=HEALTH_FONT.render("Health: "+str(yellow_health),1,WHITE)
    blue_health_txt=HEALTH_FONT.render("Health: "+str(blue_health),1,WHITE)
    WINDOW.blit(yellow_health_txt,(10,10))
    WINDOW.blit(blue_health_txt,(WIDTH-blue_health_txt.get_width()-10,10))
    pygame.display.update()

def winner_draw(text):
    draw_text= WINNER_FONT.render(text,1,WHITE)
    WINDOW.blit(draw_text,(WIDTH/2-draw_text.get_width()/2,HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_moves(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x-VELOCITY>0:   #Left
        yellow.x-=VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x+VELOCITY+yellow.width < MID_BORDER.x:   #Right
        yellow.x+=VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y-VELOCITY>0:  #Up
        yellow.y-=VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y+VELOCITY+yellow.height < HEIGHT:   #Down
        yellow.y+=VELOCITY

def blue_moves(keys_pressed,blue):
    if keys_pressed[pygame.K_LEFT] and blue.x-VELOCITY>MID_BORDER.x+MID_BORDER.width:   #Left
        blue.x-=VELOCITY
    if keys_pressed[pygame.K_RIGHT] and blue.x+VELOCITY+blue.width < WIDTH:   #Right
        blue.x+=VELOCITY
    if keys_pressed[pygame.K_UP] and blue.y-VELOCITY>0:  #Up
        blue.y-=VELOCITY
    if keys_pressed[pygame.K_DOWN] and blue.y+VELOCITY+blue.height < HEIGHT:   #Down
        blue.y+=VELOCITY

def bullet_handle(yellow_bullets,blue_bullets,yellow,blue):
    for bullet in yellow_bullets:
        bullet.x+=BULLET_SPEED
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x>WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x-=BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x<0:
            blue_bullets.remove(bullet)



def main():
    yellow=pygame.Rect(200,250,32,32)
    blue=pygame.Rect(650,250,32,32)
    yellow_bullets=[]
    blue_bullets=[]

    yellow_health=100
    blue_health=100

    run=True
    clock=pygame.time.Clock()
    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run=False
                pygame.quit

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LSHIFT and len(yellow_bullets)<BULLET_NUMBER:
                bullet=pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2 -2,10,5)
                yellow_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()
            if event.key==pygame.K_RALT and len(blue_bullets)<BULLET_NUMBER:
                bullet=pygame.Rect(blue.x,blue.y+blue.height//2 -2,10,5)
                blue_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()
        
        if event.type==YELLOW_HIT:
            yellow_health-=10
            BULLET_HIT_SOUND.play()

        if event.type==BLUE_HIT:
            blue_health-=10
            BULLET_HIT_SOUND.play()

        winner_msg=""
        if(yellow_health<=0):
            winner_msg='Blue Wins!'
        if(blue_health<=0):
            winner_msg='Yellow Wins!'

        if(winner_msg!=""):
            winner_draw(winner_msg)
            break

        keys_pressed=pygame.key.get_pressed()
        yellow_moves(keys_pressed,yellow)
        blue_moves(keys_pressed,blue)
        bullet_handle(yellow_bullets,blue_bullets,yellow,blue)
        draw(yellow,blue,yellow_bullets,blue_bullets,yellow_health,blue_health)
    
            
if __name__ == "__main__":
    main()
