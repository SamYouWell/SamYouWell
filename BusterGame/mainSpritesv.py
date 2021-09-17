import pygame
import random
import math
from pygame import mixer

#READ ME -- This "mainSprites.py" file will eventually be the "main" file for a classic Space Invaders game.
#This implemtation utilizes pygame's sprites feature, which all me to add different game features more easily.
#The TO-DO list is below the following code.


pygame.init()
clock = pygame.time.Clock()

#creating the screen:
screen_width = 800
screen_height = 700
screen  = pygame.display.set_mode((screen_width,screen_height))

#Creaing Title: images are just place holders for now! I'm gonna make my own images.
pygame.display.set_caption("Sprites Invader")
icon = pygame.image.load("BusterGame\pawprint.PNG")
pygame.display.set_icon(icon)
#loading or declaring the background:
background = pygame.image.load("BusterGame\IMG_0493.PNG")

#OPTIMIZING CODE WITH SPRITES:
class Player(pygame.sprite.Sprite): #(64x64 pixals)
    def __init__(self,pic_path, pos_x=400,pos_y=480):
        super().__init__()
        self.image = pygame.image.load(pic_path)
        self.rect = self.image.get_rect()   #fetch the rectangle around image
        self.rect.center = [pos_x, pos_y]   #position rect
        self.x = pos_x
        self.y = pos_y
        #self.rocket_shot = pygame.mixer.sound("BusterGame\lazer.wav")
    def fire(self):
        #self.rocket_shot.play()
        pass
    def moveRight(self,x_delta):
        self.rect.x += x_delta
    def moveLeft(self,x_delta):
        self.rect.x -= x_delta
    def update(self):
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= 736:
            self.rect.x = 736
        

#BULLET SPRITE: (32x32 pixals)
class Bullet(Player):
    def __init__(self, pic_path,rocket_speed):
        Player.__init__(self,pic_path,pos_x=400,pos_y=465) #pass arg is co-ordinates for (topleft) center
        self.y_delta = rocket_speed

    def launch(self):
        if self.rect.y == 449:
            self.rect.y -= self.y_delta

    def update(self):
        if self.rect.x <= 17:    #How does one write this via inheritance?
            self.rect.x = 17     #We want the bullet to be afixed to spaceship
        elif self.rect.x >= 751:
            self.rect.x = 751

        if self.rect.y < 449:
            self.rect.y -= self.y_delta

        if self.rect.y <= -16:
            reload()

        if pygame.sprite.spritecollide(rocket,enemy_sprites_lists,True):
            reload()

#ENEMY SPRITE:
class Enemy(Player):
    def __init__(self,pic_path,pos_x,pos_y):
        Player.__init__(self,pic_path)
        self.x = pos_x
        self.y = pos_y
        self.rect.center = [self.x,self.y]    #positions rect relatilve from its center
        self.delta = 7
    def update(self):
        self.x += self.delta   #enemy movement
        if self.x <= 0:
            self.delta = 7
            self.y += 20
        elif self.x >= 800:
            self.delta = -7
            self.y += 20
        self.rect.center = [self.x,self.y]  #updates position

        individual_enemy = enemy_sprites_lists.sprites()

        if len(enemy_sprites_lists) <= 6:   #ensuring that respawn works properly :) --> replace with a subscription way with sprite() method
            respawn()

        overlap_tolerance = 30

        #Preventing enemy clumping and overlapping
        for i in range(len(individual_enemy)):
            for j in range(len(individual_enemy)):
                if i != j:
                    if individual_enemy[i].rect.colliderect(individual_enemy[j].rect):
                        if abs(individual_enemy[i].rect.right - individual_enemy[j].rect.left) > overlap_tolerance and individual_enemy[i].delta == -7 and individual_enemy[j].delta == 7:
                            individual_enemy[i].delta *=-1
                            individual_enemy[j].delta *=-1
                        if abs(individual_enemy[i].rect.left - individual_enemy[j].rect.right) > overlap_tolerance and individual_enemy[i].delta == 7 and individual_enemy[j].delta == -7:
                            individual_enemy[i].delta *=-1
                            individual_enemy[j].delta *=-1


#Player image:
spaceship = Player("BusterGame\dog2.PNG")
spaceship_speed = 11

#Bullet Immage:
rocket_speed = 10
rocket = Bullet("BusterGame\Bullet.PNG",rocket_speed)

#This contains all the games sprites for easy access and updating/manipulation:
player_sprites_lists = pygame.sprite.Group()
enemy_sprites_lists = pygame.sprite.Group()

#Adding sprites to Group:
player_sprites_lists.add(rocket)
player_sprites_lists.add(spaceship)

#Enemy Spawning:
def respawn():
    enemy = Enemy("BusterGame\dog2.PNG",random.randrange(0, screen_width),random.randrange(0,150))
    enemy_sprites_lists.add(enemy)

for enemy in range(7):
    enemy = Enemy("BusterGame\dog2.PNG",random.randrange(0, screen_width),random.randrange(0,150))
    enemy_sprites_lists.add(enemy)

def reload():
    rocket.rect.y = 449
    rocket.rect.x = spaceship.rect.x+16

#RUNNING THE GAME!__________________________________________________________________
running = True
while running:

    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    
    #Keyboard controlling:
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pressed[pygame.K_RIGHT]:
        spaceship.moveRight(spaceship_speed)
        if rocket.rect.y < 449:
            rocket.moveRight(0)     #uncoupling rocket x-coed from spaceship x-coed after firing
        else:
            rocket.moveRight(spaceship_speed)
    if pressed[pygame.K_LEFT]:
        spaceship.moveLeft(spaceship_speed)
        if rocket.rect.y < 449:
            rocket.moveLeft(0)      #uncoupling rocket x-coed from spaceship x-coed after firing
        else:
            rocket.moveLeft(spaceship_speed)
    if pressed[pygame.K_UP]:
        rocket.launch()

    player_sprites_lists.update()  #game mechanics
    enemy_sprites_lists.update()   #ditto^
    player_sprites_lists.draw(screen)  #drawing all sprites on screen surface
    enemy_sprites_lists.draw(screen)
    pygame.display.flip()   #another way to refresh screen sort of like pygame.display.update()
    clock.tick(60)  #frame rate

#TO-DOs:
#Add Player and enemy respawning (depending on advancing mechanic)
#Add scoring
#Replace artwork
#Add sound effects
#Add differnt types of enemies with different characteritics and weapons
#Add leveling up or levels to game
#Add different player weapons
#Maybe add some animations to the sprites including explosions and spaceship 3D/dynamic movement
#Have fun from there...maybe a dynamic bachground!
