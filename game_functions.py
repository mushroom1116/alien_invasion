import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


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
    if event.key == pygame.K_q:
        sys.exit()


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


def check_events(ai_settings, screen, state, sb, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, state, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            # 检查按下键
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            # 检查送开建
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, state, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """玩家单击play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not state.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        state.reset_state()
        state.game_active = True
        # 重置记分牌
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人列表和子弹
        aliens.empty()
        bullets.empty()

        # 创建一群新外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没到限制就发射一颗子弹"""
    # 创建一颗新子弹加入编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_alien_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens = int(available_space_x / (2 * alien_width))
    return number_aliens


def get_numbet_rows(ai_settings, ship_height, alient_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - 3 * alient_height - 2 * ship_height
    number_rows = int(available_space_y / (2 * alient_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    # 如果这里不使用x而直接更新alien.rect.x，
    # 则alien.update中也不要使用x,因为alien.x没有得到更新一直是初值，这样屏幕上就会只出现一列alien
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    # alien.rect.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.rect.y = 50 + alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_numbet_rows(ai_settings, ship.rect.height, alien.rect.width)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边界时采取措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, state, screen, sb, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边界，并更新整群外星人位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检查外星人与飞船的碰撞
    # finds any sprites in a group that collide with the given sprite
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, state, screen, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, state, screen, sb, ship, aliens, bullets)


def update_bullets(ai_settings, screen, state, sb, ship, aliens, bullets):
    """更新子弹位置，并删除消失子弹"""
    # 更新子弹位置
    bullets.update()
    # 删除消失子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, state, sb, ship, aliens, bullets)


def ship_hit(ai_settings, state, screen, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if state.ships_left > 0:
        # 将ship_left减1
        state.ship_left -= 1
        # 更新
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        state.game_active = False
        pygame.mouse.set_visible(True)





def check_bullet_alien_collisions(ai_settings, screen, state, sb, ship, aliens, bullets):
    """响应子弹与外星人的碰撞"""
    # 检查是否有子弹击中外星人，若是，删除相应的子弹和外星人
    # detect collision between a group and another group, (dokilla, dokillb)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            state.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(state, sb)
    if len(aliens) == 0:
        # 删除现有的子弹并创建一群新的外星人，提高等级
        bullets.empty()
        ai_settings.increase_speed()
        state.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def update_screen(ai_settings, screen, state, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitem()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()
    # 如果游戏处于非活跃态就绘制play按钮
    if not state.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def check_aliens_bottom(ai_settings, state, screen, sb, ship, aliens, bullets):
    """检查是否有外星人到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 飞船被撞一样处理
            ship_hit(ai_settings, state, screen, sb, ship, aliens, bullets)
            break


def check_high_score(state, sb):
    """检查是否诞生了新最高分"""
    if state.score > state.high_score:
        state.high_score = state.score
        sb.prep_high_score()

