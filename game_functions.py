import sys
import pygame
from bullet import Bullet


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    """响应送开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # 检查按下键
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            # 检查送开建
            check_keyup_events(event, ship)


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没到限制就发射一颗子弹"""
    # 创建一颗新子弹加入编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(bullets):
    """更新子弹位置，并删除消失子弹"""
    # 更新子弹位置
    bullets.update()
    # 删除消失子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def update_screen(ai_settings, screen, ship, bullets):
    """更新屏幕上的图像"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitem()