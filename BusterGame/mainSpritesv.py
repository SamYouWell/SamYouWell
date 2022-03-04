from ast import Pass
from re import S
import pygame
import random
from pygame import mixer

#READ ME -- This "mainSprites.py" file will eventually be the "main" file for a classic Space Invaders game.
#This implemtation utilizes pygame's sprites feature, which allow me to add different game features more easily.
#The TO-DO list is below the following code.


pygame.init()
clock = pygame.time.Clock()

#creating the screen and Game variables:
screen_width = 800
screen_height = 700
screen  = pygame.display.set_mode((screen_width,screen_height))
last_enemy_shot = pygame.time.get_ticks()
last_player_shot = pygame.time.get_ticks()
one_sec = 1000
quart_sec = 250
milli_sec = 100
cool_down = quart_sec
red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)
light_blue_white = (204, 255, 255)

#Creaing Title: images are just place holders for now! I'm gonna make my own images.
pygame.display.set_caption("Sprites Invader")
icon = pygame.image.load("BusterGame\pawprint.PNG")
pygame.display.set_icon(icon)
#loading or declaring the background:
background = pygame.image.load("BusterGame\IMG_0493.PNG")

#OPTIMIZING CODE WITH SPRITES:
class Player(pygame.sprite.Sprite): #(64x64 pixals)
    screen = pygame.display.get_surface()
    area = screen.get_rect()
    
    def __init__(self,pic_path, pos_x=400,pos_y=480,health = 3):
        super().__init__()
        self.image = pygame.image.load(pic_path)
        self.rect = self.image.get_rect()   #fetch the rectangle around image
        self.rect.center = [pos_x, pos_y]   #position rect relative to center
        self.starting_health = health
        self.remaining_health = health
        self.score = 0
        self.ammo_limit = 1
        self.add_ammo = 0
        self.mag = 1
        self.add_health = 0
        self.time = pygame.time.get_ticks()
        self.resupply_limit = 1
        self.ammo_timer = pygame.time.get_ticks()
        self.med_timer = pygame.time.get_ticks()
        self.rapid_fire = False
        self.simple_blaster_recharge = 10
        self.full = 10
        
        #self.rocket_shot = pygame.mixer.sound("BusterGame\lazer.wav")
    def moveRight(self,x_delta):
        self.rect.x += x_delta
    def moveLeft(self,x_delta):
        self.rect.x -= x_delta
    
    def update(self):
        doggy_space()
        display_ammo(self.ammo_limit)

        now_time = pygame.time.get_ticks()
        
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= 736:
            self.rect.x = 736
            
        #mask image from rect:    
        self.mask = pygame.mask.from_surface(self.image)
        
        #Drop supllies like bullets:
        if spaceship.score % 25 == 0 and now_time - self.ammo_timer > 5000 and spaceship.score != 0 or now_time - self.ammo_timer > 15000 and spaceship.score > 25:
            if len(ammo_sprites) <= self.resupply_limit and self.resupply_limit < 2:
                resupply(64)
            elif len(ammo_sprites) >= 2:
                resupply(32)
            
            if spaceship.score % 40 == 0:
                self.resupply_limit += 1
            self.ammo_timer = now_time
        
        #Drop med packs or soon coming spaceshiop upgrades.    
        if spaceship.score % 14 == 0 and now_time - self.med_timer > 5000 and spaceship.score != 0:
            if len(med_packs) <= self.resupply_limit and self.resupply_limit < 2:
                health(64)
            elif len(med_packs) >= 2:
                health(32)
            self.med_timer = now_time
        
        if pygame.sprite.spritecollide(self, ammo_sprites, True):
            self.ammo_limit += self.add_ammo
            self.mag = self.ammo_limit
            self.rapid_fire = True
        if self.ammo_limit < 1:
            self.mag = 1
            self.add_ammo = 0
            self.rapid_fire = False
            
        if pygame.sprite.spritecollide(self, med_packs, True):
            self.remaining_health = self.add_health
            
        pygame.draw.rect(screen,red, (self.area.x, (self.area.bottom - 5), self.area.width, 4))
        if self.rapid_fire == True:
            pygame.draw.rect(screen,green, (self.area.x, (self.area.bottom - 5), int(self.area.width * (self.ammo_limit/self.mag)), 4))
            self.simple_blaster_recharge = 0
        elif self.rapid_fire == False:
            pygame.draw.rect(screen,yellow, (self.area.x, (self.area.bottom - 5), int(self.area.width * (self.simple_blaster_recharge/self.full)), 4))
            
        pygame.draw.rect(screen,red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 10))
        if self.remaining_health > 0:
            pygame.draw.rect(screen,green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.remaining_health/self.starting_health)), 10))
            
class Supplies(pygame.sprite.Sprite):
    screen = pygame.display.get_surface()
    area = screen.get_rect()
    
    def __init__(self, pic_path, pos_x, pos_y, drop_rate, scale = 64):
        super().__init__()
        self.image = pygame.image.load(pic_path)
        self.rect = self.image.get_rect()   #fetch the rectangle around image
        self.rect.center = [pos_x, pos_y]   #position rect relative to center
        self.size = scale
        self.image = pygame.transform.scale(self.image, (self.size,self.size))
        self.drop_rate = drop_rate
        
    def _size_check(self):
        if self.size == 64:
            spaceship.add_ammo = 50
            spaceship.add_health = spaceship.starting_health
        elif self.size == 32:
            spaceship.add_ammo = 25
            spaceship.add_health = 1
        
    def _drop(self):
        en_pos = self.rect.move((0, self.drop_rate))
        if not self.area.contains(en_pos):
            if (self.rect.top >= (self.area.bottom)):
                self.kill()
        self.rect = en_pos
    
    def update(self):
        self._size_check()
        self._drop()

#BULLET SPRITE: (32x32 pixals)
class Bullet(pygame.sprite.Sprite):
    timer = pygame.time.get_ticks()
    def __init__(self, pic_path,rocket_speed,launch_point,bullet_y_limit= -16,pos_x=400, pos_y=465):
        super().__init__()
        self.y_delta = rocket_speed
        self.image = pygame.image.load(pic_path)
        self.rect = self.image.get_rect()   #fetch the rectangle around image
        self.rect.center = [pos_x, pos_y]   #position rect relative to center
        self.launch_point = launch_point
        self.byl = bullet_y_limit

    def launch(self):
        if self.rect.centery == self.launch_point:
            self.rect.y += self.y_delta
            if self in simple_blaster_bullet:
                spaceship.ammo_limit = 0
            else: spaceship.ammo_limit -= 1
        
    def update(self):
        #shooting enemy_missile instance:    
        if self in enemy_ammo_lists:
            self.rect.y += self.y_delta
            if self.rect.y > self.byl:
                self.kill()
            elif pygame.sprite.spritecollide(self, player_sprites_lists, False, pygame.sprite.collide_mask):
                spaceship.remaining_health -= 1
                self.kill()
        
        if self.rect.x <= 17:
            self.rect.x = 17     #We want the bullet to be afixed to spaceship
        elif self.rect.x >= 751:
            self.rect.x = 751
            
        #Moves bullet after launch or afix to spaceship:
        if self in simple_blaster_bullet or self in player_ammo_lists:          #It MIGHT be beatter to have these within thier own class and update method, but this works just fine.
            if self.rect.centery < self.launch_point:
                self.rect.centery += self.y_delta
            elif self.rect.centery == self.launch_point:
                self.rect.centerx = spaceship.rect.centerx    

            if self.rect.y <= self.byl:
                self.kill()

            if pygame.sprite.spritecollide(self,enemy_sprites_lists,True, pygame.sprite.collide_mask):
                spaceship.score += 1
                self.kill()
                
#ENEMY SPRITE:
class Enemy(pygame.sprite.Sprite):
    delta = 5
    screen = pygame.display.get_surface()
    area = screen.get_rect()
    
    def __init__(self,pic_path,pos_x,pos_y):
        super().__init__()
        self.image = pygame.image.load(pic_path)
        self.rect = self.image.get_rect()   #fetch the rectangle around image
        self.rect.center = [pos_x, pos_y]   #position rect relative to center
        self.individual_enemy = enemy_sprites_lists.sprites()    #call so that it's updated.
        self.overlap_tolerance = 30
        
    def _clump_prevention(self):
        #Preventing enemy clumping and overlapping
        for counter1, i in enumerate(self.individual_enemy):
            for counter2, j in enumerate(self.individual_enemy):
                if counter1 != counter2:
                    if i.rect.colliderect(j.rect):
                        if abs(i.rect.right - j.rect.left) > self.overlap_tolerance and i.delta < 0 and j.delta > 0:
                            i.delta = -i.delta
                            j.delta = -j.delta
                            if (i.rect.right - j.rect.left) < -64:
                                i.rect.y += 2

                        if abs(i.rect.left - j.rect.right) > self.overlap_tolerance and i.delta > 0 and j.delta < 0:
                            i.delta = -i.delta
                            j.delta = -j.delta
                            if (i.rect.left - j.rect.right) < -64:
                                i.rect.y += 2
            
        
    def _movement(self):
        en_pos = self.rect.move((self.delta, 0))
        if not self.area.contains(en_pos):
            if (self.rect.left <= (self.area.left) and self.delta < 0) or (self.rect.right >= (self.area.right) and self.delta > 0):      #+/- 1 is overlap tolerance
                self.delta = -self.delta
                en_pos = self.rect.move((self.delta, 20))
        self.rect = en_pos

    def update(self):
        self._movement()
        self._clump_prevention() 
        
        if len(enemy_sprites_lists) < 2:   #ensuring that respawn works properly :) --> replace with a subscription way with sprite() method
            enemy_ammo_lists.empty()
            respawn()
        
        #mask image from rect:    
        self.mask = pygame.mask.from_surface(self.image)
        

#How do I get diagonal motion?
#Experiment with enumerate!

#Player image:
spaceship = Player("BusterGame\dog2.PNG",health = 7)
spaceship_speed = 11

#Primary weapon settings:    
bullet_1_launch_p = spaceship.rect.centery

#Bullet Immage:
rocket_speed = -10



#This contains all the games sprites for easy access and updating/manipulation:
player_sprites_lists = pygame.sprite.Group()
player_ammo_lists = pygame.sprite.Group()
enemy_sprites_lists = pygame.sprite.Group()
enemy_ammo_lists = pygame.sprite.Group()
ammo_sprites = pygame.sprite.Group()
med_packs = pygame.sprite.Group()
dust = pygame.sprite.Group()
simple_blaster_bullet = pygame.sprite.Group()

#Adding sprites to Group:
player_sprites_lists.add(spaceship)

#Displaying score:
font = pygame.font.Font('freesansbold.ttf', 32)
weapon_font = pygame.font.Font('freesansbold.ttf', 22)
def display_score(score_value, x=10,y=10):
    score = font.render("Score : " + str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

def display_ammo(mag_value, x = 500, y = 650):                      #The simple blaster does not need to update our use the ammo_limit attribute b/c it's a limitless blaster
    if spaceship.ammo_limit <= 1 and len(simple_blaster_bullet) <= 1 and spaceship.rapid_fire == False:     #One has to explicitly state the rapid_fire attribute in both conditions b/c of the linear order of checking!
        ammo = weapon_font.render("Simple Blaster", True, light_blue_white)
        screen.blit(ammo, (600,y))
    elif spaceship.rapid_fire == True:
        ammo = weapon_font.render("Rapid Fire: " + str(mag_value), True, light_blue_white)
        screen.blit(ammo, (x,y))
        
#Enemy Spawning:
def respawn():
    enemy = Enemy("BusterGame\dog2.PNG",random.randrange(0, screen_width),random.randrange(0, 150))
    while len(enemy_sprites_lists) < 14:     #great mechanic for spawning new levels
        for hostile in enemy_sprites_lists:
            if abs(hostile.rect.x - enemy.rect.x) > 32:   #If it were less than 30, then it would clump more.
                enemy_sprites_lists.add(enemy)
                break
        enemy = Enemy("BusterGame\dog2.PNG",random.randrange(0, screen_width),random.randrange(-150,150))

for enemy in range(7):
    enemy = Enemy("BusterGame\dog2.PNG",random.randrange(0, screen_width),random.randrange(0,150))
    enemy_sprites_lists.add(enemy)
    
def resupply(size):
    ammo_supply = Supplies("BusterGame\Bullet.PNG", pos_x = random.randrange(0, screen_width), pos_y = random.randrange(-50, 0), drop_rate = 3, scale=size)
    ammo_sprites.add(ammo_supply)
    
def health(size):
    med_pack = Supplies("BusterGame\dog2.PNG", pos_x = random.randrange(0, screen_width), pos_y = random.randrange(-50, 0), drop_rate = 3,scale=size)
    med_packs.add(med_pack)
    
def doggy_space():
    particles = Supplies("BusterGame\pawprint.PNG", pos_x = random.randrange(0, screen_width), pos_y = random.randrange(-50, 0), drop_rate = 4)
    dust.add(particles)
    
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

    #Getting current time in mil seconds:
    current_time = pygame.time.get_ticks()

    #eneny shooting:        #Is there a way to implement this into the class's update method?!...turn this into a function like respawn()?
    if current_time - last_enemy_shot > one_sec and len(enemy_ammo_lists) < 10 and len(enemy_sprites_lists) > 0:
        shooting_enemy = random.choice(enemy_sprites_lists.sprites())
        enemy_missile = Bullet("BusterGame\Bullet.PNG",15, shooting_enemy.rect.y,shooting_enemy.area.bottom,shooting_enemy.rect.centerx,shooting_enemy.rect.centery)
        enemy_ammo_lists.add(enemy_missile)
        last_enemy_shot = current_time
            
    #Keyboard controlling AKA event handling:
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pressed[pygame.K_RIGHT]:
        spaceship.moveRight(spaceship_speed)
    if pressed[pygame.K_LEFT]:
        spaceship.moveLeft(spaceship_speed)
        
    #Player machine gun shooting
    if pressed[pygame.K_UP]:            #Is there a way to implement this into the class's update method also?!
        if spaceship.score <= 25 and current_time - last_player_shot > one_sec or spaceship.add_ammo == 0 and current_time - last_player_shot > one_sec:
            rocket = Bullet("BusterGame\Bullet.PNG",launch_point = bullet_1_launch_p,rocket_speed = rocket_speed, pos_x = spaceship.rect.centerx, pos_y = spaceship.rect.centery)
            simple_blaster_bullet.add(rocket)
            rocket.launch()
            spaceship.simple_blaster_recharge = 0
            last_player_shot = current_time
        elif spaceship.score >= 25 and current_time - last_player_shot > cool_down and spaceship.ammo_limit >= 1:
            mac_bullets = Bullet("BusterGame\Bullet.PNG",launch_point = bullet_1_launch_p, rocket_speed = rocket_speed, pos_x = spaceship.rect.centerx, pos_y = spaceship.rect.centery)
            player_ammo_lists.add(mac_bullets)
            mac_bullets.launch()
            last_player_shot = current_time
            
    if spaceship.simple_blaster_recharge < 10:
        if current_time - last_player_shot > milli_sec:
            spaceship.simple_blaster_recharge += 1
    elif spaceship.simple_blaster_recharge == 10:
        #Make ready and loaded sound!
        pass
    
    if spaceship.score > 40:        #Leveling up gun speed
        cool_down = milli_sec
    
    #Display Game Over: 
    if pygame.sprite.spritecollide(spaceship,enemy_sprites_lists, True, pygame.sprite.collide_mask):
        enemy_sprites_lists.empty()
    if len(enemy_sprites_lists) == 0 or spaceship.remaining_health == 0:
        enemy_sprites_lists.empty()
        player_sprites_lists.empty()
        player_ammo_lists.empty()
        game_over_text()
    
    player_ammo_lists.update()
    simple_blaster_bullet.update()
    enemy_ammo_lists.update()
    enemy_sprites_lists.update()   #ditto^
    ammo_sprites.update()
    med_packs.update()
    dust.update()
    player_ammo_lists.draw(screen)
    simple_blaster_bullet.draw(screen)
    ammo_sprites.draw(screen)
    dust.draw(screen)
    player_sprites_lists.update()  #placed here to avoid being drawn over.
    med_packs.draw(screen)
    enemy_ammo_lists.draw(screen)
    player_sprites_lists.draw(screen)  #drawing all sprites on screen surface
    enemy_sprites_lists.draw(screen)
    display_score(spaceship.score)
    pygame.display.flip()   #another way to refresh screen sort of like pygame.display.update()
    clock.tick(60)  #frame rate

#TO-DOs:
#Make each class inherit form sprite class directly!...it optimizes performance apparently
#Properly implemtn Python's OS module
#Clean up unnecessary variables
#Add Player and enemy respawning (depending on advancing mechanic)
#Add more dynamic, randomized collision animation for enemy other than bouncing off each other (e.g. in "3D" space, i.e. shrinking in size, more pronounced diagonal motion)
#Replace artwork
#Add sound effects
#Add differnt types of enemies with different characteritics and weapons
#Add leveling up or levels to game
#Add different player weapons
#Maybe add some animations to the sprites including explosions and spaceship 3D/dynamic movement
#Have fun from there...maybe a dynamic bachground!
#Add ammo limit and pickup mechanism
#Add stats class!
#Reimpliment this schema to make Kennel Gate Keeper
