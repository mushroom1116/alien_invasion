import pygame
from pygame.sprite import Group

import game_functions as gf
from button import Button
from game_state import GameState
from scoreboard import Scoreboard
from setting import Settings
from ship import Ship


def run_game():
    """初始化游戏并创建一个屏幕对象"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # 创建按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建统计信息实例
    state = GameState(ai_settings)
    sb = Scoreboard(ai_settings, screen, state)
    # 创建一个飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个外星人编组
    # alien = Alien(ai_settings, screen)
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏主循环
    while True:
        # 监控键盘和鼠标
        gf.check_events(ai_settings, screen, state, sb, play_button, ship, aliens, bullets)
        if state.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, state, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, state, screen, sb, ship, aliens, bullets)
        # 每次循环重新绘制屏幕
        gf.update_screen(ai_settings, screen, state, sb, ship, aliens, bullets, play_button)


run_game()
