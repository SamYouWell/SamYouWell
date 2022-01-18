import pygame
import random
import math
from pygame import mixer

#READ ME -- This "mainSprites.py" file will eventually be the "main" file for a classic Space Invaders game.
#This implemtation utilizes pygame's sprites feature, which allow me to add different game features more easily.
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
        self.rect.center = [pos_x, pos_y]   #position rect relative to center
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
    def __init__(self, pic_path,rocket_speed,launch_point,centered_offset,bullet_y_limit= -16,pos_x=400, pos_y=465):
        super().__init__(pic_path)
        self.y_delta = rocket_speed
        self.rect.center = [pos_x, pos_y]
        self.launch_point = launch_point
        self.centered = centered_offset
        self.byl = bullet_y_limit

    def launch(self):
        if self.rect.y == self.launch_point:
            self.rect.y += self.y_delta
            
    def reload(self, x):
        self.rect.x = x
        self.rect.y = self.launch_point

    def update(self):
        if self.rect.x <= 17:
            self.rect.x = 17     #We want the bullet to be afixed to spaceship
        elif self.rect.x >= 751:
            self.rect.x = 751

        if self.rect.y < self.launch_point:
            self.rect.y += self.y_delta
            
        if rocket.rect.y <= rocket.byl:
            self.reload(spaceship.rect.x+self.centered)

        if pygame.sprite.spritecollide(rocket,enemy_sprites_lists,True) or pygame.sprite.spritecollide(rocket,enemy_ammo_lists,True):
            self.reload(spaceship.rect.x+self.centered)

#ENEMY SPRITE:
class Enemy(Player):
    delta = 5
    def __init__(self,pic_path,pos_x,pos_y):
        super().__init__(pic_path)
        self.rect.center = [pos_x, pos_y]    #positions rect relatilve from its center
        self.enemy_missile = Bullet("BusterGame\Bullet.PNG", 12,self.rect.y, 16, 716, self.rect.x, self.rect.y)
        enemy_ammo_lists.add(self.enemy_missile)

    def update(self):
        self.rect.x += self.delta   #enemy movement
        if self.rect.x <= 0:
            if self.delta < 0:
                self.delta *= -1
                self.rect.y += 20
                self.enemy_missile.launch_point += 20
        elif self.rect.x >= 800:
            if self.delta > 0:
                self.delta *= -1
                self.rect.y += 20
                self.enemy_missile.launch_point += 20
        
        if len(enemy_sprites_lists) < 2:   #ensuring that respawn works properly :) --> replace with a subscription way with sprite() method
            enemy_ammo_lists.empty()
            respawn()
            
        individual_enemy = enemy_sprites_lists.sprites()    #call so that it's updated.

        overlap_tolerance = 30

        #Preventing enemy clumping and overlapping
        for counter1, i in enumerate(individual_enemy):
            for counter2, j in enumerate(individual_enemy):
                if counter1 != counter2:
                    if i.rect.colliderect(j.rect):
                        if abs(i.rect.right - j.rect.left) > overlap_tolerance and i.delta < 0 and j.delta > 0:
                            i.delta *=-1
                            j.delta *=-1
                            if (i.rect.right - j.rect.left) < -64:
                                i.rect.y += 2
                                i.enemy_missile.launch_point += 2

                        if abs(i.rect.left - j.rect.right) > overlap_tolerance and i.delta > 0 and j.delta < 0:
                            i.delta *=-1
                            j.delta *=-1
                            if (i.rect.left - j.rect.right) < -64:
                                i.rect.y += 2
                                i.enemy_missile.launch_point += 2
                                
        #Enemy missile movement and afixing to enemy spaceship:
        self.enemy_missile.launch()
        if self.enemy_missile.rect.y > self.enemy_missile.launch_point:
            self.enemy_missile.rect.y += self.enemy_missile.y_delta
            if self.enemy_missile.rect.y >= self.enemy_missile.byl:
                self.enemy_missile.reload(self.rect.x+self.enemy_missile.centered)
        else:
            self.enemy_missile.rect.center = [self.rect.x+self.enemy_missile.centered,self.rect.y+self.enemy_missile.centered]    #updating (x,y)
            
        if pygame.sprite.spritecollide(self.enemy_missile,player_sprites_lists,False):
            self.enemy_missile.reload(self.rect.x+self.enemy_missile.centered)
            
        

#How do I get diagonal motion?
#Experiment with enumerate!

#Player image:
spaceship = Player("BusterGame\dog2.PNG")
spaceship_speed = 11

#Primary weapon settings:    
bullet_1_launch_p = 449
b1lp = 16

#Bullet Immage:
rocket_speed = -10
rocket = Bullet("BusterGame\Bullet.PNG",launch_point = bullet_1_launch_p, centered_offset = b1lp, rocket_speed = rocket_speed)

#This contains all the games sprites for easy access and updating/manipulation:
player_sprites_lists = pygame.sprite.Group()
enemy_sprites_lists = pygame.sprite.Group()
enemy_ammo_lists = pygame.sprite.Group()

#Adding sprites to Group:
player_sprites_lists.add(rocket)
player_sprites_lists.add(spaceship)

#Enemy Spawning:
def respawn():
    enemy = Enemy("BusterGame\dog2.PNG",random.randrange(0, screen_width),random.randrange(-150, 150))
    while len(enemy_sprites_lists) < 14:     #great mechanic for spawning new levels
        for hostile in enemy_sprites_lists:
            if abs(hostile.rect.x - enemy.rect.x) > 32:   #If it were less than 30, then it would clump more.
                enemy_sprites_lists.add(enemy)
                break
        enemy = Enemy("BusterGame\dog2.PNG",random.randrange(0, screen_width),random.randrange(-150,150))

for enemy in range(7):
    enemy = Enemy("BusterGame\dog2.PNG",random.randrange(0, screen_width),random.randrange(-150,150))
    enemy_sprites_lists.add(enemy)
    
#GAME OVER!    
game_over_font = pygame.font.Font('freesansbold.ttf',75)
def game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over_text,(200,250))



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
        if rocket.rect.y < bullet_1_launch_p:
            rocket.moveRight(0)     #uncoupling rocket x-coed from spaceship x-coed after firing
        else:
            rocket.moveRight(spaceship_speed)
    if pressed[pygame.K_LEFT]:
        spaceship.moveLeft(spaceship_speed)
        if rocket.rect.y < bullet_1_launch_p:
            rocket.moveLeft(0)      #uncoupling rocket x-coed from spaceship x-coed after firing
        else:
            rocket.moveLeft(spaceship_speed)
    if pressed[pygame.K_UP]:
        rocket.launch() 
    
    #Display Game Over: 
    if pygame.sprite.spritecollide(spaceship,enemy_sprites_lists, True):
        enemy_sprites_lists.empty()
        enemy_ammo_lists.empty()
    if len(enemy_sprites_lists) == 0:
        game_over_text()
    
    player_sprites_lists.update()  #game mechanics
    enemy_sprites_lists.update()   #ditto^
    enemy_ammo_lists.update()
    player_sprites_lists.draw(screen)  #drawing all sprites on screen surface
    enemy_ammo_lists.draw(screen)
    enemy_sprites_lists.draw(screen)
    pygame.display.flip()   #another way to refresh screen sort of like pygame.display.update()
    clock.tick(60)  #frame rate

#TO-DOs:
#Add Game Over
#Add Player and enemy respawning (depending on advancing mechanic)
#Add more dynamic, randomized collision animation for enemy other than bouncing off each other (e.g. in "3D" space, i.e. shrinking in size, more pronounced diagonal motion)
#Add scoring
#Replace artwork
#Add sound effects
#Add differnt types of enemies with different characteritics and weapons
#Add leveling up or levels to game
#Add different player weapons
#Maybe add some animations to the sprites including explosions and spaceship 3D/dynamic movement
#Have fun from there...maybe a dynamic bachground!
#Add ammo limit and pickup mechanism
