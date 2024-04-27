from pygame import *
from random import *

# set window and backround
window = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

# class for elements (draw)
class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x =  player_x
        self.rect.y = player_y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group() # group of bullets

class Rocket(Gamesprite): # class for rocket (movement and attack)
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < 700-50:
            self.rect.x +=self.speed
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x, 445, 5)
        bullets.add(bullet)

class UFO(Gamesprite): # class for ufos (movement) 
    def update (self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >= 400:            
            self.rect.y = 0
            self.rect.x = randint(0, 650)
            self.speed = randint(1, 5)
            missed += 1

class Bullet(Gamesprite): # class for bullets (movement) 
    def update(self):
        self.rect.y -= self.speed

# set elements(rocket, ufos)
rocket = Rocket('rocket.png', 20, 445, 10)
ufos = sprite.Group() # group of ufos
for i in range(5):
    ufo = UFO('ufo.png', randint(0, 650), 0, randint(1, 5))
    ufos.add(ufo)

font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 30)

# set lose and win
lose = font1.render('YOU LOSE! (If you want to play again press a.)', True, (255, 0, 0))
win = font1.render('YOU WIN! (If you want to play again press a.)', True, (0, 255, 0))

score = 0
missed = 0

finish = False

# play music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

clock = time.Clock()
FPS = 60
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    # handle collision and score updates
    collide = sprite.groupcollide(ufos, bullets, True, True)
    for i in collide:
        score += 1
        ufo = UFO('ufo.png', randint(0, 650), 0, randint(1, 5))
        ufos.add(ufo)

    # check for game over conditions
    if sprite.spritecollide(rocket, ufos, False) or missed >= 5:
        window.blit(lose, (50, 200))
        finish = True
    if score >= 10:
        window.blit(win, (50, 200))
        finish = True

    if finish == False:
        window.blit(background, (0, 0))
        # draw elements
        rocket.draw()
        ufos.draw(window)
        bullets.draw(window)
        # elements' movement
        bullets.update()
        ufos.update()
        rocket.update()

    # set score and missed
    text_score = font2.render('Score:' + str(score), True, (255, 255, 255))
    window.blit(text_score, (10, 20))
    text_missed = font2.render('Missed:' + str(missed), True, (255, 255, 255))
    window.blit(text_missed, (10, 50))

    keys_pressed = key.get_pressed()

    #reset button
    if keys_pressed[K_a]:
        finish = False
        score = 0
        missed = 0
        for ufo in ufos:
            ufo.rect.y = 0

    # set pause and resume
    pause = font1.render('Pause', 1, (255, 255, 255))
    resume = font1.render('Resume', 1, (255, 255, 255))

    # pause button
    if keys_pressed[K_p]:
        finish = True
        window.blit(pause, (200, 200))
    
    # resume button
    if keys_pressed[K_r]:
        finish = False
        window.blit(resume, (200, 200))
    
    clock.tick(FPS)
    display.update()