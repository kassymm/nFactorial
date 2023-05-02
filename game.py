import pygame
from pygame.locals import *
import time
import random

pygame.init()


width, height = 1276, 627
key = 0

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ну, погоди!")


bg = pygame.image.load("images/Static.png") #background
wolf= pygame.image.load('images/sprites-wolf.png') #wolf
egg_image = pygame.image.load('images/sprites-egg.png') 

# class of eggs. loc stands for the initial spawning nest of the egg. 
# We update the cooridinates of each egg at every display iteration.
class EGG:
    def __init__ (self, loc):
        self.timer = 0
        self.loc = loc
        if self.loc == 0:
            self.x = 86
            self.y = 96
            self.timer = 0
        if self.loc == 1:
            self.x = 1130
            self.y = 96
            self.timer = 0
        if self.loc == 2:
            self.x = 86
            self.y = 260
            self.timer = 0
        if self.loc == 3:
            self.x = 1130
            self.y = 260
            self.timer = 0




def draw(eggs, key, left, right):
    win.fill((210,210,210))
    win.blit(bg, (0, 0))
    if key == 0:
        win.blit(wolf, (200, 160), (0,0, 396, 381)) #(horizontal, vertical)
    if key == 1:
        win.blit(wolf, (700, 160), (0,381*1, 396, 381)) 
    if key == 2:
        win.blit(wolf, (200, 160), (0,381*2, 396, 381)) 
    if key == 3:
        win.blit(wolf, (700, 160), (0,381*3, 396, 381))
    for egg in eggs:
        win.blit(egg_image, (egg.x, egg.y))
    if left:
        pass #insert temporary image of the broken egg on the left
    if right:
        pass #insert temporary image of the broken egg on the right
    pygame.display.update()
    

def main():
    run = True
    clock = pygame.time.Clock()
    key = 0
    rollingtime = 30
    score = 0
    lives = 3
    left = False
    right = False

    egg1 = EGG(1)

    # I want to have a list of eggs that are present on the screen at each moment.
    eggs = [egg1]

    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # closing the game window
                run = False
                break
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            key = 0
        if keys[pygame.K_k]:
            key = 1
        if keys[pygame.K_f]:
            key = 2
        if keys[pygame.K_j]:
            key = 3
        
        for egg in eggs:
            if egg.timer < 75 and egg.loc in {0, 2}:
                egg.timer += 1
                egg.x += 2
                egg.y += 1
            if egg.timer < 75 and egg.loc in {1, 3}:
                egg.timer += 1
                egg.x -= 2
                egg.y += 1
            if egg.timer == 75:
                if key == egg.loc:
                    eggs.remove(egg)
                    score += 1
                    lives -= 1
                else:
                    if egg.y >=500 and egg.loc in {0,2}:
                        left = True
                        eggs.remove(egg)
                        # insert timed broken egg image on the left
                    if egg.y >=500 and egg.loc in {1,3}:
                        right = True
                        eggs.remove(egg)
                        # insert timed broken egg image on the left
                    
                    
                    egg.y+=10
                    lives -= 1



        draw(eggs, key, left, right)

    
    pygame.quit()

if __name__ == "__main__":
    main()

