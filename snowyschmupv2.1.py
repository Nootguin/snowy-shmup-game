# Schmup
# Frozen Jam by Copyright 2008 Elle Trudgett | https://github.com/elle-trudgett - Licensed under CC BY 3.0 https://creativecommons.org/licenses/by/3.0/ | edited by qubodup
# Art from Kenney.nl

import pygame
import random
from os import path

# Images directory
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Window
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE =("#12011A")
ORANGE =("#E6924D")
LAWN =("#A7D475")
BEIGE =("#928575")

# Initialise pygame and create the window
pygame.init() # runs pygame
pygame.mixer.init() # initalises sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snowy shmup") # Sets Window Name
clock = pygame.time.Clock() # clock is a part of time and time is part of pygame


# Drawing Text
font_name = pygame.font.match_font('arial') # pygame will search through the list of fonts on your computer and will find the closest match to that name
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK) # true means if you want the text to be anti-aliassed or not
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y) # middle top of the rectangle
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 200) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.radius = 20 # collison circle size
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # draws the collison boxes
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 # speedx property that will keep track of how fast the player is moving in the x direction (side-to-side).
        self.shield = 200 # every time you get hit by a meteor you lose some shield
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.powertimer = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()


    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 300)




class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_img)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()        
        self.radius = int(self.rect.width * 0.85 /2) # another cleaner way
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # draws the collison boxes
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0   # rotation of sprite
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks() # will get how many ticks there has been since the clock started and this variable keeps track of that

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50: # if now is equal to 1000ms and last update was 900ms means that the last update was 100ms ago
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360 # divides by 360 and makes sure it doesnt go above 360
            # Creating new center and optimising meteor spins
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate() # to prevent update function being too crowded we can define rotate seperatly and you can comment it out and it wont ever do the rotate
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Load Sprites
background = pygame.image.load(path.join(img_dir, "snow.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "Ship.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserRed.png")).convert()
meteor_img = [] # list of images
meteor_list = ["meteor.png","meteor1.png","meteor2.png","meteor3.png","meteor4.png","meteor5.png","meteor6.png","meteor7.png"]

for img in meteor_list:
    meteor_img.append(pygame.image.load(path.join(img_dir,img)).convert())
explosion_anim = {}
explosion_anim['lrg'] = []
explosion_anim['sml'] = []
explosion_anim['player'] = []
for i in range (9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lrg = pygame.transform.scale(img, (75,75))
    explosion_anim['lrg'].append(img_lrg)
    img_sml = pygame.transform.scale(img, (32,32))
    explosion_anim['sml'].append(img_sml)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, "shield_gold.png")).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, "bolt_gold.png")).convert()

# Load Sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Shoot1.wav'))
expl_sounds = []
for snd in ['Boom1.wav', 'Boom2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = (pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg')))
pygame.mixer.music.load(path.join(snd_dir, 'frozenjam.ogg'))
pygame.mixer.music.set_volume(0.4)

# Start Game
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    newmob()

score = 0
pygame.mixer.music.play(loops=-1) # could for example add a playlist or loops, =-1 means it loops back to the start again 
#Game Loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    # check for closing window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius # more points depending on image size
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lrg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # Update to see if hit player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) # specifying what kind of collision you want to use
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sml')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 200
    
    # if the player hit a powerup
    hits = pygame.sprite.spritecollide(player,powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 200:
                player.shield = 200
        if hit.type == 'gun':
            player.powerup()
        
            
    # if the player died and the explosion finished playing
    if player.lives == 0 and not death_explosion.alive():
        player.kill()
        running = False



    # Draw / render assets
    screen.fill(LAWN)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10) # where?, what?, size?, x positon?, y position?
    draw_shield_bar(screen, 5, 5, player.shield) # x, y and number value of which number value to fill
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()
pygame.quit()