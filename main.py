import pygame
import sys
from pygame.locals import *
import traceback
from myplane import MyPlane
import enemy
import bullet
import supply
from random import *
import os

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")

background = pygame.image.load("images/background.png").convert()

# 定义血槽颜色
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

# 载入音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

def add_small_enemies(group1, group2, num):
    '''
    添加小飞机
    '''
    for i in range(num):
        temp_enemy = enemy.SmallEnemy(bg_size)
        group1.add(temp_enemy)
        group2.add(temp_enemy)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        temp_enemy = enemy.MidEnemy(bg_size)
        group1.add(temp_enemy)
        group2.add(temp_enemy)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        temp_enemy = enemy.BigEnemy(bg_size)
        group1.add(temp_enemy)
        group2.add(temp_enemy)

# 提升敌机的速度
def inc_speed(target, inc):
    for each in target:
        each.speed += inc

def main():
    
    #加载背景音乐
    pygame.mixer.music.play(-1)

    running = True #定义用于控制程序循环变量

    # 用于定义游戏的帧率
    clock = pygame.time.Clock()

    #创建我的飞机
    me = MyPlane(bg_size)
    switch_plane = False  #用于切换飞机图片
    delay = 100

    #生成敌方飞机
    enemies = pygame.sprite.Group()
    #生成小型敌方飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)
    #生成中型敌方飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 5)
    #生成大型敌方飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 3)
    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    #生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    
    #生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-33,me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx+30,me.rect.centery)))

    # 统计用户得分
    score = 0
    score_font = pygame.font.Font("font/font.ttf",36) #字体类型
    WHITE = (255,255,255)   # 字体颜色

    # 标志是否暂停游戏,四个状态，四个图片
    paused = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    pause_rect = pause_nor_image.get_rect()
    pause_rect.left, pause_rect.top=width - pause_rect.width - 10, 10
    pause_image = pause_nor_image

    #设置难度级别
    level = 1

    #全屏炸弹
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    #定义补给发放,每30秒发一次
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    #设置一个定时器
    SUPPLY_TIMER = USEREVENT
    pygame.time.set_timer(SUPPLY_TIMER,30000)

    #超级子弹的定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1
    #标志是否使用超级子弹
    is_double_bullet = False

    # 剩余数量
    life_image = pygame.image.load("images/life.png")
    life_rect = life_image.get_rect()
    life_num = 3

    #计时器，当我的飞机重生后的安全期
    INVINCIBLE_TIME = USEREVENT + 2

    #用于记录重复记录文件
    recorded = False

    #游戏结束界面
    gameover_font = pygame.font.Font("font/font.ttf", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIMER, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIMER, 30000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if paused:
                        pause_image = resume_pressed_image
                    else:
                        pause_image = pause_pressed_image
                else:
                    if paused:
                        pause_image = resume_nor_image
                    else:
                        pause_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            # 判断补给
            elif event.type == SUPPLY_TIMER:
                supply_sound.play()
                if choice([True, False]):
                    bullet_supply.reset()
                else:
                    bomb_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                print("INVINCIBLE_TIME")
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME,0)
                
        # 根据用户的得分增加难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            #增加3架小型敌机，2架中型敌机和一架大型敌机
            add_small_enemies(small_enemies, enemies,3)
            add_mid_enemies(mid_enemies, enemies,2)
            add_big_enemies(big_enemies, enemies,1)
            #提升小型敌机的速度
            inc_speed(small_enemies,1)
        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            #增加5架小型敌机，3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies,5)
            add_mid_enemies(mid_enemies, enemies,3)
            add_big_enemies(big_enemies, enemies,2)
            #提升小型敌机的速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        elif level == 3 and score > 600000:
            level = 4
            upgrade_sound.play()
            #增加5架小型敌机，3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies,5)
            add_mid_enemies(mid_enemies, enemies,3)
            add_big_enemies(big_enemies, enemies,2)
            #提升小型敌机的速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        elif level == 4 and score > 1000000:
            level = 5
            upgrade_sound.play()
            #增加5架小型敌机，3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies,5)
            add_mid_enemies(mid_enemies, enemies,3)
            add_big_enemies(big_enemies, enemies,2)
            #提升小型敌机的速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)

        
        # 画出屏幕的背景
        screen.blit(background,(0,0))
        
        # 判断游戏是否继续
        if  life_num and not paused:
            # 调用key模块的get_pree获得当前被按下的键盘
            # 频繁读取键盘状态时最好使用这种方式
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
            
            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            #绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    #发射超级子弹
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,18000)
                    bullet_supply.active = False
            
            # 发射子弹
            if not(delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullet2[bullet2_index].reset((me.rect.centerx-33,me.rect.centery))
                    bullet2[bullet2_index + 1].reset((me.rect.centerx+30,me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullet1[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy ==0:
                                    e.active = False
                            else:
                                e.active = False

            # 绘制敌方大型飞机飞机
            for each in big_enemies:
                if each.active:
                    # 移动飞机
                    each.move()
                    if each.hit:
                        #绘制击中的特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_plane:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                    
                    #绘制敌机的血槽
                    pygame.draw.line(screen, BLACK, \
                        (each.rect.left, each.rect.top-5),\
                        (each.rect.right, each.rect.top-5), 2)
                    #当生命大于20%，显色绿色，否则显示黑色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,\
                        (each.rect.left, each.rect.top - 5),
                        (each.rect.left + each.rect.width * energy_remain,\
                            each.rect.top - 5),2)

                    #飞机即将出现在画面中，播放音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:
                    #毁灭
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play() #第一次播放音效
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            score += 10000
                            enemy3_fly_sound.stop()
                            each.reset()

            # 绘制敌方中型飞机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        #绘制被击中的特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    #绘制敌机的血槽
                    pygame.draw.line(screen, BLACK, \
                        (each.rect.left, each.rect.top-5),\
                        (each.rect.right, each.rect.top-5), 2)
                    #当生命大于20%，显色绿色，否则显示黑色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,\
                        (each.rect.left, each.rect.top - 5),
                        (each.rect.left + each.rect.width * energy_remain,\
                            each.rect.top - 5),2)
                else:
                    #毁灭
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play() #第一次播放音效
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            enemy2_down_sound.stop()
                            each.reset()
            
            # 绘制敌方小型飞机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    #毁灭
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play() #第一次播放音效
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            enemy1_down_sound.stop()
                            each.reset()

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies,False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False

            # 绘制我方飞机
            if me.active:
                if switch_plane:
                    screen.blit(me.image_me1, me.rect)
                else:
                    screen.blit(me.image_me2, me.rect)
            else:
                #我方飞机毁灭
                if not (delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME,3000)
            # 绘制剩余炸弹的数量
            bomb_text = bomb_font.render("x %d " % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height-bomb_rect.height-10))   #显示炸弹图
            screen.blit(bomb_text, (20 + bomb_rect.width, height-text_rect.height-5))   #显示字

            #绘制剩余生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,(width - 10 -(i+1)*life_rect.width,\
                        height - 10 - life_rect.height))
            
            #绘制最终的得分
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10,5))


        elif life_num == 0:
            #停止背景音乐
            pygame.mixer.music.stop()

            #停止全部音效
            pygame.mixer.stop

            #停止一些计时器
            pygame.time.set_timer(SUPPLY_TIMER,0)  #补给计时器

            if not recorded:
                if os.path.exists("record.txt"):
                    #读取历史最高分
                    with open("record.txt","r") as f:
                        record_score = int(f.read())
                else:
                    record_score = 0
                #如果玩家分数大于历史最高分，则存档
                if score > record_score:
                    with open("record.txt","w") as f:
                        f.write(str(score))
                        recorded = True
            #绘制结束界面
            record_score_text = score_font.render("Best : %d" % record_score, True, WHITE)
            screen.blit(record_score_text, (50,50))

            gameover_text1 = gameover_font.render("Your Score", True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (width - gameover_text1_rect.width)//2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                 (width - gameover_text2_rect.width) // 2, \
                                 gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            #检测用户的鼠标操作
            #如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击“结束游戏”            
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()   
        #绘制暂停图片
        screen.blit(pause_image, pause_rect)
        
        
        
        #用于切换图片,每五帧切换一次
        if delay % 5 == 0:
            switch_plane = not switch_plane
        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    # try:
    main()
    # except SystemExit:
    #     pass
    # except:
    #     traceback.print_exc()
    #     pygame.quit()
    #     input()



