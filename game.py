import pygame
import time
import random
import inputbox
from leaderboard import *
pygame.init()

width, height = 1276, 627
key = 0
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ну, погоди!")
bg = pygame.image.load("images/BG.png") #background
wolf= pygame.image.load('images/wolf.png') #wolf
egg_image = pygame.image.load('images/egg.png')
chicks = pygame.image.load("images/HP-black.png")
pseudo_chicks = pygame.image.load("images/HP-gray.png")

font = pygame.font.SysFont('comicsans', 60)

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

def draw(eggs, key, left, right, score, lives, level):
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

    score_text = font.render (f"{score}", 1, 'black')
    level_text = font.render (f"LVL: {level}", 1, 'black')

    win.blit(score_text, (800, 30))
    win.blit(level_text, (900, 30))
    

    win.blit(pseudo_chicks, (200, 50), (0, 0, 312, 94))
    win.blit(chicks, (200, 50), (0, 0, 104*(3 - lives), 94))



    pygame.display.update()


def show_highscore():
    global SCORE
    global screen
    global leaderboard
    win.fill((210, 210, 210))
    leaderboard.draw(screen)
    pygame.display.update()
    

def main():
    run = True
    clock = pygame.time.Clock()
    key = 0
    score = 0
    lives = 3
    left = False
    right = False
    # start_time = time.time()
    # elapsed_time = 0
    egg_add_increment = 2000 #time between the egg spawns
    egg_count = 0 #variable to track the time between spawns
    level = 1
    egg1 = EGG(1)

    # I want to have a list of eggs that are present on the screen at each moment.
    eggs = [egg1]

    while run:
        egg_count += clock.tick(10)

        # elapsed_time = time.time - start_time 
        if egg_count > egg_add_increment:
            nest = random.randint(0, 3)
            eggs.append(EGG(nest))
            egg_add_increment = max (200, egg_add_increment - 20)
            egg_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # closing the game window
                run = False
                break
        

        keys = pygame.key.get_pressed()
    
        # important_keys = [pygame.K_d, pygame.K_k, pygame.K_f, pygame.K_j]
        # if True in important_keys:
        #     key = important_keys.index(True)
        if keys[pygame.K_d]:
            key = 0
        if keys[pygame.K_k]:
            key = 1
        if keys[pygame.K_f]:
            key = 2
        if keys[pygame.K_j]:
            key = 3
        level = sum(1 for x in [0, 10, 30] if score>=x)

        for egg in eggs:

            if egg.timer == 100:
                egg.y +=10
                if egg.y >=500:
                    lives -= 1
                    if egg.loc % 2 == 0:
                        left = True# insert temporary broken egg image on the left
                    else:
                        right = True
                    eggs.remove(egg)

            if egg.timer < 75:
                if egg.loc % 2 == 0:
                    egg.timer += 1*level
                    egg.x += 2*level
                    egg.y += 1*level
                else:
                    egg.timer += 1*level
                    egg.x -= 2*level
                    egg.y += 1*level
                    
            if 75<= egg.timer <=78:
                if key == egg.loc:
                    eggs.remove(egg)
                    score += 1

                else:
                    egg.timer = 100

 
            
                    # insert timed broken egg image on the left
        
        draw(eggs, key, left, right, score, lives, level)        
        
        if lives == 0:
            name = inputbox.gameover(win)
            leaderboard = Leaderboard(name, score)
            leaderboard.load_previous_scores()
            leaderboard.save_score()
            leaderboard.draw(win)
            
            

if __name__ == "__main__":
    main()

