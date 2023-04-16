# Разработай свою игру в этом файле!
from pygame import *

window = display.set_mode((1800, 800))

clock = time.Clock()

hp = 3
collect_coins = 0
shoot_timer = 0

class Hero(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def show(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

    def control(self):
        global hp, game, collect_coins
        keyboard = key.get_pressed()
        if keyboard[K_w] and self.rect.y > 0:
            self.rect.y -= 8
            #if self.rect.colliderect(stena.rect):
            if sprite.spritecollide(self, stenaall, False):
                self.rect.y += 8
        if keyboard[K_s] and self.rect.bottom < 800:
            self.rect.y += 8
            if sprite.spritecollide(self, stenaall, False):
                self.rect.y -= 8
        if keyboard[K_d] and self.rect.right < 1800:
            self.rect.x += 8
            if sprite.spritecollide(self, stenaall, False):
                self.rect.x -= 8
        if keyboard[K_a] and self.rect.x > 0:
            self.rect.x -= 8
            if sprite.spritecollide(self, stenaall, False):
                self.rect.x += 8
        if self.rect.colliderect(e1.rect):
            hp -= 1 
            if hp == 0:
                game = 0
            self.rect.x = 200
            self.rect.y = 200
        if self.rect.colliderect(heal.rect):
            hp += 1 
            heal.rect.x = -1000
        for i in coins.sprites():
            if self.rect.colliderect(i.rect):
                i.rect.x = -1000
                collect_coins += 1
                if collect_coins == 3:
                    finish.rect.x = 1650
        
    
    def resize(self, w, h):
        self.image = transform.scale(self.image, (w, h))
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = x, y

class Enemy(Hero):
    def __init__(self, img, x, y, steps, speed):
        super().__init__(img, x, y)
        self.steps = steps
        self.distans = 0
        self.side = 1
        self.speed = speed
# 1 - направо
# -1 - налево
    def move(self):
        self.rect.x += self.side * 5
        if self.side == 1:
            self.rect.x += 5
        else:
            self.rect.x -= 5

        self.distans += 1

        if self.distans == self.steps:
            self.distans = 0
            self.side = -self.side
class Bullet(Hero):
    def __init__(self, img, x, y, x_direction, y_direction):
        super().__init__(img, x, y)
        self.x_direction = x_direction
        self.y_direction = y_direction
    def move(self):
        self.rect.x += self.x_direction
        self.rect.y += self.y_direction

e1 = Enemy('e.png', 400, 200, 100, 1)
e1.resize(100, 100)


player = Hero('knife.png', 200, 200)
player.resize(100, 100)

foon = image.load('foon.png')
foon = transform.scale(foon, (1800, 800))

heart = image.load('heart.png')
heart = transform.scale(heart, (50, 50))

turret = Hero('enemy.png', 100, 600)
turret.resize(200, 200)


stena1 = Hero('stena.png', 0, 0)
stena2 = Hero('stena.png', 300, 0)
stena3 = Hero('stena.png', 600, 0)
stena4 = Hero('stena.png', 1100, 0)
stena5 = Hero('stena.png', 1400, 0)
stena6 = Hero('stena.png', 0, 380)
stena7 = Hero('stena.png', 500, 380)
stena8 = Hero('stena.png', 800, 380)
stena9 = Hero('stena.png', 1100, 380)
stena10 = Hero('stena.png', 1400, 380)
stenaall = sprite.Group()
stenaall.add(stena2, stena3, stena4, stena5, stena7, stena6, stena8, stena9)

heal = Hero('heal.png', 1000, 0)
heal.resize(100, 100)

finish = Hero('finish.png', -600, 600)
finish.resize(200, 200)

bullets = sprite.Group()

c1 = Hero('coin.png', 0, 0)
c2 = Hero('coin.png', 1700, 700)
c3 = Hero('coin.png', 1650, 200)
coins = sprite.Group()
coins.add(c1, c2, c3)

for i in coins.sprites():
    i.resize(70, 70)

game = 1
while game == 1:
    window.blit(foon, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = 2

    if player.rect.colliderect(finish.rect):
        game = 3 
    player.control()
    player.show()

    heal.show()

    finish.show()
    stena1.show()
    stenaall.draw(window)
    coins.draw(window)
    bullets.draw(window)
    for b in bullets.sprites():
        b.move()
    for b in bullets.sprites():
        if b.rect.x > 1800 or b.rect.x < -100:
            bullets.remove(b)
        if b.rect.y > 800 or b.rect.y < -100:
            bullets.remove(b)
        if b.rect.colliderect(player.rect):
            bullets.remove(b)
            hp -= 1
            if hp == 0:
                game = 0
            player.rect.x = 200
            player.rect.y = 200


    e1.move()
    e1.show()

    turret.show()
    shoot_timer += 1
    if shoot_timer == 60:
        shoot_timer = 0
        b = Bullet('gfnhjy.png', turret.rect.x, turret.rect.y, 8, 0)
        b.resize(150, 150)
        bullets.add(b)
    stena10.show()
    stena1.show()

    for i in range(hp):
        window.blit(heart, (20 + 50*i, 20))
    
    display.update()

    clock.tick(60)

if game == 0:
    window.blit(foon, (0, 0))
    font.init()
    Shrift = font.Font(None, 80)
    lose_text = Shrift.render('Ты проиграл', True, (0, 0, 0))
    window.blit(lose_text, (700, 300))
    display.update()
    while True:
        for e in event.get():
            if e.type == QUIT:
                exit()
        clock.tick(60)
if game == 3:
    window.blit(foon, (0, 0))
    font.init()
    Shrift = font.Font(None, 80)
    lose_text = Shrift.render('Ты победил', True, (0, 0, 0))
    window.blit(lose_text, (700, 300))
    display.update()
    while True:
        for e in event.get():
            if e.type == QUIT:
                exit()
        clock.tick(60)