import pygame
import math
from random import randint, choice
from sys import exit

pygame.init()

# Game Variables
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1000
FPS = 60
GREY = (220,220,200)


# Screens
loading_screen = True
game_screen = False
end_screen = False

window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) 
clock = pygame.time.Clock()
pygame.display.set_caption("Dinosaur Game")

# Font 
game_font = pygame.font.Font('font/Pixeltype.ttf',75)
load_font = pygame.font.Font('font/Pixeltype.ttf',100)

# Graphics
pygame_icon = pygame.image.load("graphics/logo.jpg").convert_alpha()
pygame.display.set_icon(pygame_icon)
ground = pygame.image.load("graphics/ground.png").convert_alpha()

# Background
sky = pygame.image.load("graphics/bg/sky.png").convert_alpha()
menu = pygame.image.load("graphics/bg/start.jpg").convert_alpha()
end = pygame.image.load("graphics/bg/end.png").convert_alpha()
sky_width = sky.get_width()
tiles = math.ceil(SCREEN_WIDTH/sky_width)+1
scroll = 0
# Music 
load_music = pygame.mixer.Sound("audio/loadingMusic.mp3")
load_music.set_volume(0.15)
game_music = pygame.mixer.Sound("audio/gameMusic.mp3")
game_music.set_volume(0.15)
end_music = pygame.mixer.Sound("audio/gameover.mp3")
end_music.set_volume(0.15)
g_music = False
l_music  = True
e_music = False
# Player 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hitbox = pygame.image.load("graphics/zombie/zombieFirst.png").convert_alpha()
        player = pygame.image.load("graphics/player/playerStand.png").convert_alpha()
        player_run1 = pygame.image.load("graphics/player/playerRun1.png").convert_alpha()
        player_run2 = pygame.image.load("graphics/player/playerRun2.png").convert_alpha()
        self.player_run = [player,player_run1,player_run2]
        self.player_jump = pygame.image.load("graphics/player/playerJump.png").convert_alpha()    
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.35)
        self.gravity = 0
        self.player_speed = 5
        self.player_index = 0
        self.image = self.player_run[self.player_index]
        self.rect = self.hitbox.get_rect(midbottom = (100,420))
    def player_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom == 420:
            self.gravity = -20
            self.jump_sound.play()

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.player_speed
        
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH-50:
            self.rect.x += self.player_speed

    def apply_grav(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 420:
            self.rect.bottom = 420
    
    def play_animation(self):
        if self.rect.bottom < 420:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_run):
                self.player_index = 0
            self.image = self.player_run[int(self.player_index)]
        
    def update(self):
        self.player_move()
        self.apply_grav()
        self.play_animation()
 
player1 = pygame.sprite.GroupSingle()
player1.add(Player())

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "zombie":
            zombie1 = pygame.image.load("graphics/zombie/zombieFirst.png").convert_alpha()
            zombie2 = pygame.image.load("graphics/zombie/zombieMid.png").convert_alpha()
            zombie3 = pygame.image.load("graphics/zombie/zombieLast.png").convert_alpha()
            self.enemy_move = [zombie1,zombie2,zombie3]
            y_ = 425
        else:
            bat2 = pygame.image.load("graphics/bat/bat2.png").convert_alpha()
            bat1 = pygame.image.load("graphics/bat/bat1.png").convert_alpha()
            self.enemy_move = [bat1,bat2]
            y_ = randint(280,350)
        self.enemy_index = 0
        self.image = self.enemy_move[self.enemy_index]
        self.rect = self.image.get_rect(midbottom = (randint(1100,1300),y_))
        
    def enemy_animation(self):
                self.enemy_index += 0.12
                if self.enemy_index >= len(self.enemy_move):
                        self.enemy_index = 0
                self.image = self.enemy_move[int(self.enemy_index)]
    
    def destroy(self):
        if self.rect.x < -100:
            self.kill()

    def update(self):
        self.enemy_animation()
        self.rect.x -= 9
        self.destroy()


enemy1 = pygame.sprite.Group()
enemy_timer = pygame.USEREVENT + 1
enemy_timer2 = pygame.USEREVENT + 2
enemy_timer3 = pygame.USEREVENT + 3
spawnrate = 650
spawnrate2 = 575
spawnrate3 = 520
pygame.time.set_timer(enemy_timer,spawnrate)
pygame.time.set_timer(enemy_timer2,spawnrate2)
pygame.time.set_timer(enemy_timer3,spawnrate3)

def collision():
        if pygame.sprite.spritecollide(player1.sprite,enemy1,False):
            enemy1.empty()
            return False
        else:
            return True

# Load Screen
name = load_font.render("Dino Jumper",False,(174,252,0))
name_rect = name.get_rect(center = (500,170))
start_text = game_font.render("Press to Start!",False, GREY)
start_texth = game_font.render("Press to Start!",False,"White")
start_rect = start_text.get_rect(center = (500,250))

# End Screen 
play_again = game_font.render("Play Again?",False,GREY)
play_againh = game_font.render("Play Again?",False,"White")
play_rect = play_again.get_rect(center = (500,200))
quit_ = game_font.render("Quit",False,GREY)
quit_h = game_font.render("Quit",False,"White")
quit_rect = quit_.get_rect(center = (500,300))

# Game Screen
start_time = 0
def show_score():
    time = int(pygame.time.get_ticks()/1000) - start_time
    if(time%25 == 0 and time != 0 and time <= 50):
        score = game_font.render(f"Score: {time}",False,"Red")
    elif(time%10 == 0 and time != 0):
        score = game_font.render(f"Score: {time}",False,"Yellow")
    else:
        score = game_font.render(f"Score: {time}",False,"Black")
    score_rect = score.get_rect(center = (500,50))
    window.blit(score,score_rect)
    return time

# Start Game
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_screen:
            # Enemy Spawns
            if score < 25:
                if event.type == enemy_timer:
                    enemy1.add(Enemy(choice(["zombie","zombie","zombie","bat","bat"])))
            elif score < 50:
                if event.type == enemy_timer2:
                    enemy1.add(Enemy(choice(["zombie","zombie","zombie","bat","bat"])))
            else:
                if event.type == enemy_timer3:
                    enemy1.add(Enemy(choice(["zombie","zombie","zombie","bat","bat"])))

    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()
    # Loading Screen
    if loading_screen:
        if l_music:
            g_music = True
            l_music = False
            load_music.play(loops = -1)
        pygame.display.update()
        window.blit(menu,(0,0))
        window.blit(name,name_rect)
        if start_rect.collidepoint(mouse):
            window.blit(start_texth,start_rect)
        else:
            window.blit(start_text,start_rect)
        if start_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
            loading_screen = False
            game_screen = True
            start_time = int(pygame.time.get_ticks()/1000) 
   
    # End Screen
    if end_screen:
        pygame.display.update()
        if e_music:
            game_music.stop()
            e_music = False
            g_music = True
            end_music.play(loops=-1)

        window.blit(end,(0,0))
        score_msg = load_font.render(f"Final Score: {score}",False,"White")
        scoreRect = score_msg.get_rect(center = (500,100))
        window.blit(score_msg,scoreRect)
        if play_rect.collidepoint(mouse):
            window.blit(play_againh,play_rect)
        else:
            window.blit(play_again,play_rect)
        # Restart Game
        if play_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
            end_screen = False
            game_screen = True
            start_time = int(pygame.time.get_ticks()/1000) 

        if quit_rect.collidepoint(mouse):
            window.blit(quit_h,quit_rect)
        else:
            window.blit(quit_,quit_rect)
        # Quit
        if quit_rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
            end_screen = False
            load_screen = True
            pygame.quit()
            exit()

    # Game Screen
    if game_screen:
        pygame.display.update()
        if g_music:
            load_music.stop()
            end_music.stop()
            e_music = True
            g_music = False
            game_music.play(loops = -1)
        # Draw Scrolling Background
        for i in range(0,tiles):
            window.blit(sky,(i*sky_width + scroll,-60))

        scroll -= 1
        if abs(scroll) > sky_width:
            scroll = 0
        
        window.blit(ground,(0,425))
        score = show_score()

        # Enemy
        enemy1.draw(window)
        enemy1.update()

        game_screen = collision()
        if game_screen == False:
            end_screen = True

        # Player 
        player1.draw(window)
        player1.update()
            
    