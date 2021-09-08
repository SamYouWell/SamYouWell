import pygame
import random
import math
from pygame import mixer

#READ ME -- This Space Invaders game is simply a quick and dirty sketch. The images are just place holders and I will not improve upon this file:
#The file that I will improve upon, and will actually be the real "main" file going forward, is called "mainSprites.py."

pygame.init()

#creating the screen:
screen  = pygame.display.set_mode((800,700))

#Creaing Title: images are just place holders for now! I'm gonna make my own.
pygame.display.set_caption("Buster Invader")
icon = pygame.image.load("BusterGame\pawprint.PNG")
pygame.display.set_icon(icon)

#Player loaded and coordinated
Playerdog = pygame.image.load("BusterGame\dog2.PNG")
p_x = 370
p_y = 480
PlayerdogX_change = 0

#loading or declaring the background:
background = pygame.image.load("BusterGame\IMG_0493.PNG")

#Background sound:
#mixer.music.load('background.wave')
#mixer.music.play(-1)

#Opponant loaded and coordinated
Opponant = []
o_x = []
o_y = []
oppX_change = []
oppY_change = []
num_of_opp = 7
for i in range(num_of_opp):
    Opponant.append(pygame.image.load("BusterGame\dog2.PNG"))
    o_x.append(random.randint(0,735)) #random position
    o_y.append(random.randint(0,150))
    oppX_change.append(4)   #change to a higher value with load of the background or use a rect function (you don't need to append constant variables, but for simplicity we will)
    oppY_change.append(20)

def Opp(x,y, i):
    screen.blit(Opponant[i],(x,y))

def isCollision(o_x, o_y, bulletX, bulletY):
    distance = math.sqrt(math.pow(o_x-bulletX,2)+(math.pow(o_y-bulletY,2)))
    if distance < 27 and bullet_state is not "ready":
        print("enemy: ",o_x,o_y)
        print("bullet: ",bulletX,bulletY)
        return True
    else:
        return False

#Bullet
bulletImg = pygame.image.load("BusterGame\Bullet.PNG")
bulletX = 0
bulletY = 480 #starts at the top of PlayerDogX
bulletY_change = -4
bullet_state = "ready"  #"ready" means you cannot see the bullet, and "fire" means you currently see the bullet
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10)) #the additional values just center the bullet against the dog

#Displaying score:
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
def display_score(x,y):
    score = font.render("Score : " + str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

#Creating GAME OVER:
game_over_font = pygame.font.Font('freesansbold.ttf',75)

def game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over_text,(200,250))

ammo_rounds = 100

#calling player into game
def Player(x,y):
    screen.blit(Playerdog,(x,y))

playing = True
#keeping the window/screen open: Game Loop
while playing:
    #standard for RGB
    screen.fill((0,0,0))
    screen.blit(background, (0,0))     #loading background into loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    # Keyboard controlling: in the x-axis
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            PlayerdogX_change = 5       #changed to a higher value due to background load 
        if event.key == pygame.K_LEFT:
            PlayerdogX_change = -5
    #Keyboard Control of bullet:
        if event.key == pygame.K_UP:
            #bullet_sound = mixer.Sound('lazer.wave')
            #bullet_sound.play()
            if bullet_state is "ready":
                bulletX = p_x
                fire_bullet(bulletX,bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            PlayerdogX_change = 0

    p_x += PlayerdogX_change    #storing new player x postion

    Player(p_x,p_y) #calling player into loop
    
    #creating boundaries for p_x:
    if p_x <= 0:
        p_x = 0
    elif p_x >= 736:
        p_x = 736

    #Bullet motion:
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY += bulletY_change
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

    #creating boundaries for o_x AND creating movement:
    for i in range(num_of_opp):
        #displaying GAME OVER:
        if o_y[i] > 480:
            for j in range(num_of_opp):     #This removes all the enemies from the screen by "teleporting" them far below the screen.
                o_y[j] = 2000
            game_over_text()
            break

        o_x[i] += oppX_change[i]          #storing new opp x position
        if o_x[i] <=0:
            oppX_change[i]=4
            o_y[i] += oppY_change[i]
        elif o_x[i] >= 736:
            oppX_change[i]=-4
            o_y[i] += oppY_change[i]
        Opp(o_x[i],o_y[i], i)
        #Collision:
        collision = isCollision(o_x[i],o_y[i],bulletX,bulletY)    #maybe simplify by turning this block into another function:
        if collision:
            #explosion_sound = mixer.Sound('explosion.wav')
            #explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            o_x[i] = random.randint(0,735) #random position, and it's 735 so that opp does not glitch down when shot at.
            o_y[i] = random.randint(0,150)

    display_score(textX,textY)
    pygame.display.update()

