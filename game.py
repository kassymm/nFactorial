import pygame
import time
import random
import inputbox
import json
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
highscore_background = pygame.image.load("images/logo.png")

font = pygame.font.SysFont('comicsans', 32)

# class of eggs. loc stands for the initial spawning nest of the egg. 
# We update the cooridinates of each egg at every display iteration.
class EGG():
    def __init__ (self, rotten, loc):
        self.timer = 0
        self.loc = loc
        self.rotten = rotten
        if self.loc == 0:
            self.x = 86
            self.y = 110
            self.timer = 0
        if self.loc == 1:
            self.x = 1170
            self.y = 110
            self.timer = 0.
        if self.loc == 2:
            self.x = 86
            self.y = 280
            self.timer = 0
        if self.loc == 3:
            self.x = 1170
            self.y = 280
            self.timer = 0

def draw(eggs, key, score, lives, level, elapsed_time):
    # pygame.display.update()
    win.fill((255,255,255))
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
        # if you can afford computationally you can uncommment the next line to draw eggs instead of ellipses
        # win.blit(egg_image, (egg.x, egg.y))
        if egg.rotten:
            pygame.draw.ellipse(win, "black", pygame.Rect(egg.x, egg.y, 20, 30))
        else:
            pygame.draw.ellipse(win, "black", pygame.Rect(egg.x, egg.y, 20, 30), width=3)


    score_text = font.render (f"{score}", 1, 'black')
    level_text = font.render (f"LVL: {level}", 1, 'black')
    instructions_text = font.render("Use d,f,j,k buttons to play!", 1, "black")

    win.blit(score_text, (800, 30))
    win.blit(level_text, (900, 30))
    if elapsed_time<5:
        win.blit(instructions_text, (450, 130))
    

    win.blit(pseudo_chicks, (200, 50), (0, 0, 312, 94))
    win.blit(chicks, (200, 50), (0, 0, 104*(3 - lives), 94))

    pygame.display.update()

def draw_start_menu():
    pygame.display.update()
    win.fill((255, 255, 255))
    win.blit(highscore_background, (450,131))
    font = pygame.font.SysFont('comicsans', 64)

    start_button = font.render('Press SPACE to start', True, (0,0,0))

    win.blit(start_button, (550, 400))
    FILE_NAME = "highscore.json"
    highscore_file = open(FILE_NAME, "r+")
    scores = json.load(highscore_file)
    padding_y = 0
    max_scores = 8 # We *could* paint every score, but it's not any good if you can't see them (because we run out of the screen).
    nbr_scores = 1
    for score in scores:
        if nbr_scores <= max_scores:
            win.blit(font.render(str(nbr_scores)+". " +str(score["name"]) +": " + str(score["score"]), 1, (0,0,0)), (50,50 + padding_y))
            padding_y += 60
            nbr_scores += 1


    

def main():
    game_state = 0 # 0, 1, 2 stand for start menu, game, game over
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if game_state == 0: #start menu

            draw_start_menu()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                start_time = time.time()
                game_state = 1
                fps_cap = 30
                key = 0
                score = 0
                lives = 3
                egg_add_increment = 1000 #time between the egg spawns
                egg_count = 0 #variable to track the time between spawns
                level = 1
                eggs = [] # I want to have a list of eggs that are present on the win at each moment.



        if game_state == 1: # game interface
            elapsed_time = time.time()-start_time
            clock = pygame.time.Clock()
            dt = clock.tick(fps_cap)
            keys = pygame.key.get_pressed()
            egg_count += level * dt
            increment = dt/30

            draw(eggs, key, score, lives, level, elapsed_time)

            if keys[pygame.K_d]:
                key = 0
            if keys[pygame.K_k]:
                key = 1
            if keys[pygame.K_f]:
                key = 2
            if keys[pygame.K_j]:
                key = 3

            if egg_count > egg_add_increment:
                nest = random.randint(0, 3)
                rotten = bool(random.uniform(0, 1) < level/10)
                eggs.append(EGG(rotten, nest))
                egg_add_increment = max (1000, egg_add_increment - 20)
                egg_count = 0

            level = sum(1 for x in [0, 10, 30] if score>=x)

            for egg in eggs:
        
                if egg.timer == -1:
                    egg.y +=10*increment
                    if egg.y >=500 and not egg.rotten:
                        lives -= 1
                        eggs.remove(egg)
                    if egg.y >=500 and egg.rotten:
                        eggs.remove(egg)

                if 0<=egg.timer < 75:
                    if egg.loc % 2 == 0:
                        egg.timer += 1*level*increment
                        egg.x += 2*level*increment
                        egg.y += 1*level*increment
                    else:
                        egg.timer += 1*level*increment
                        egg.x -= 2*level*increment
                        egg.y += 1*level*increment
                        
                if 75<= egg.timer:
                    if key == egg.loc and not egg.rotten:
                        eggs.remove(egg)
                        score += 1
                    if key == egg.loc and egg.rotten:
                        eggs.remove(egg)
                        lives = 0
                    
                    else:
                        egg.timer = -1
                        
        
            if lives == 0:
                game_state = 2
                pygame.time.delay(1000)
        
        if game_state == 2:
            name = inputbox.gameover(win)
            leaderboard = Leaderboard(name, score)
            leaderboard.load_previous_scores()
            leaderboard.save_score()
            game_state = 0
    

        

            

if __name__ == "__main__":
    main()


