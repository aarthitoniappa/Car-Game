import pygame
from pygame.locals import *
import random
from pygame import mixer
import time

#set game window variable 
size = width, height = (800, 800)
road_width = int(width/1.6)
roadmark_w = int(width/80)
right_lane = width/2 + road_width/4
left_lane = width/2 - road_width/4

speed = 1

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(size)  # make game window 
pygame.display.set_caption("Aarthi's Car Game")  # title
# pygame.draw.rect(screen,(50,50,50),(width/2-road_width/2,0,road_width,height)) #dispaly road
# screen.fill((60,220,0)) #background color: red,green,blue
# pygame.display.update()
mixer.music.load('background (1).wav') #add a background music
mixer.music.play(-1) #create loop for background music 

running = True

#load cars intital postions and set value of their location to a box surrounding the image
car = pygame.image.load("redcar2.png") 
car_location = car.get_rect()
car_location.center = right_lane, height*0.8

car2 = pygame.image.load("car3.png")
car2_location = car2.get_rect()
car2_location.center = left_lane, height*0.2

player_car_mask = pygame.mask.from_surface(car) #create a mask to use to signal when collisions happen
enemy_car1_mask = pygame.mask.from_surface(car2) #create a mask to use to signal when collisions happen

start_icon = pygame.image.load("start.png") #have a start icon appear at begining of game
game_over_icon = pygame.image.load("gameover.png") #have icon appear at end of game 

#game states
game_started = False 
car2_onscreen = False 
game_over = False
start_time = None
collision_enabled = False
level_up_enabled = False
level = 1  
prev_speed = speed
counter = 0

font = pygame.font.Font(None, 100)

#display start icon untill game starts 
pygame.display.flip()

#game loop
while running:
    if not game_started:
        screen.blit(start_icon, (width // 2 - start_icon.get_width() // 2, height // 2 - start_icon.get_height() // 2))
        pygame.display.flip() 
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_SPACE:  # Start the game when the Space key is pressed
                game_started = True
                level_up_enabled = True  
                collision_enabled = True
        #have start icon appear untill user hits space to start game and game states are intialized
        
    if game_started and level_up_enabled:
        counter += 1
        if counter == 1024:
            speed += 1
            counter = 0
            if speed > prev_speed:
                level += 1  
                print("Level Up", level)
            prev_speed = speed
    #increase level and speed every 1024 frames 
    car2_location[1] += speed
    if car2_location[1] > height:
        if random.randint(0, 1) == 0:
            car2_location.center = right_lane, -200
        else:
            car2_location.center = left_lane, -200
    #if car goes off screen then it will randomly be assigned to the top edge of the right or left lane 
    #if car_location[0] == car2_location[0] and car2_location[1] > car_location[1]-150: was my orginal code for collisions with this line of code the colllision would have been based off a box around the cars
    if game_started and collision_enabled:
        if player_car_mask.overlap(enemy_car1_mask, (car2_location.x - car_location.x, car2_location.y - car_location.y)):
            explosionSound = pygame.mixer.Sound("explosion.wav")
            explosionSound.set_volume(0.5) 
            explosionSound.play()
            #play explosion sound when car masks overlap signalling a collision 
            pygame.time.delay(1000)
            screen.blit(game_over_icon, (width // 2 - game_over_icon.get_width() // 2, height // 2 - game_over_icon.get_height() // 2))
            font = pygame.font.Font(None, 50)  # Choose a font and size for the level display
            level_display = font.render("Level: " + str(level), True, (255, 255, 255))
            screen.blit(level_display, (width // 2 - level_display.get_width() // 2, height // 2 + 100))
            pygame.display.update()
            pygame.time.delay(1500)
            print("GAME OVER! YOU LOST!")
            game_over = True
            #delays so the user can hear the sound and see the display of game over and the level they got to before the application closes 
    for event in pygame.event.get():
        if event.type == QUIT:
            # collapse the app if users closes window 
            running = False
        if event.type == KEYDOWN:
            # move user car to the left
            if event.key in [K_a, K_LEFT]:
                car_location = car_location.move([-int(road_width/2), 0])
            # move user car to the right
            if event.key in [K_d, K_RIGHT]:
                car_location = car_location.move([int(road_width/2), 0])

# design game elements on the screen 
    screen.fill((60, 220, 0))
    pygame.draw.rect(screen, (50, 50, 50), (width/2-road_width /
                     2, 0, road_width, height))  # dispaly road
    pygame.draw.rect(screen, (255, 240, 60), (width/2-roadmark_w/2,
                     0, roadmark_w, height))  # center yellow mark
    pygame.draw.rect(screen, (255, 255, 255), (width/2-roadmark_w /
                     2 + roadmark_w*23, 0, roadmark_w, height))  # center yellow mark
    pygame.draw.rect(screen, (255, 255, 255), (width/2+roadmark_w /
                     2 - roadmark_w*24, 0, roadmark_w, height))  # center yellow mark
    screen.blit(car, car_location)
    screen.blit(car2, car2_location)
    pygame.display.update()
    if game_over: 
        running = False
pygame.quit()
