import pygame
from random import *


class SmallEnemy(pygame.sprite.Sprite):
    '''
    定义小型的敌机
    '''
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("images/enemy1_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy1_down2.png").convert_alpha(),\
            pygame.image.load("images/enemy1_down3.png").convert_alpha(),\
            pygame.image.load("images/enemy1_down4.png").convert_alpha()
        ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0],bg_size[1]
        self.speed = 2
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)  #用于检测非透明部分是否发生碰撞
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-5 * self.height, 0)
        

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        # 重新初始化敌机位置
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-5 * self.height, 0)
        self.active = True

class MidEnemy(pygame.sprite.Sprite):
    '''
    定义中型的敌机
    '''
    energy = 8
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy2.png").convert_alpha()
        self.image_hit = pygame.image.load("images/enemy2_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("images/enemy2_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down2.png").convert_alpha(),\
            pygame.image.load("images/enemy2_down3.png").convert_alpha(),\
            pygame.image.load("images/enemy2_down4.png").convert_alpha()
        ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0],bg_size[1]
        self.speed = 2
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)  #用于检测非透明部分是否发生碰撞
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -self.height)
        self.energy = MidEnemy.energy
        self.hit = False    #用于检测飞机是否被击中
       

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.energy = MidEnemy.energy
        # 重新初始化敌机位置
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -self.height)
        self.active = True

class BigEnemy(pygame.sprite.Sprite):
    '''
    定义中型的敌机
    '''
    energy = 20  #定义类的变量，因为函数中都需要用到这个
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load("images/enemy3_n2.png").convert_alpha()
        self.image_hit = pygame.image.load("images/enemy3_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("images/enemy3_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down2.png").convert_alpha(),\
            pygame.image.load("images/enemy3_down3.png").convert_alpha(),\
            pygame.image.load("images/enemy3_down4.png").convert_alpha(),\
            pygame.image.load("images/enemy3_down5.png").convert_alpha(),\
            pygame.image.load("images/enemy3_down6.png").convert_alpha()\
        ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0],bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-15 * self.height, -5 * self.height)
        self.active = True
        self.mask = pygame.mask.from_surface(self.image1)  #用于检测非透明部分是否发生碰撞
        self.energy = BigEnemy.energy
        self.hit = False    #用于检测飞机是否被击中

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        # 初始化能量
        self.energy = BigEnemy.energy
        # 重新初始化敌机位置
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-15 * self.height, -5 * self.height)
        self.active = True