import pygame
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
size = [800, 600]

clock = pygame.time.Clock()


class CrossHair:  # Aim 표시
    def __init__(self, _gamepad):
        self.img_size = 30
        self.gamepad = _gamepad
        self.crosshair_img = pygame.image.load("assets/crosshair02.png")
        self.crosshair_img = pygame.transform.scale(self.crosshair_img, (self.img_size, self.img_size))

    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        self.gamepad.blit(self.crosshair_img, (mouse_x - self.img_size/2, mouse_y - self.img_size/2))


class Hud:  # 게임에 표시되는 contents (총알개수 , 장전여부)

    def __init__(self, _gamepad):
        self.godo_font = pygame.font.Font('font/GodoM.ttf', 32)
        self.c_bullet = 30
        self.all_bullet = 30
        self.gamepad = _gamepad
        self.reload_cnt = 0

    def reload(self):  # 재장전(2초동안 재장전)
        print('roloading')
        print('=================' + str(self.reload()) + '================')
        if self.reload_cnt > 2 * 60:  # 2초 카운팅이 됬을 때
            self.c_bullet = self.all_bullet

        else:  # 2초가 아직 안지났을 때
            self.reload_txt = self.godo_font.render('reloading ', True, BLACK)
            self.gamepad.blit(self.reload_txt, (550, 520))
            self.reload_cnt += 1

    def shoot(self):  # 총알을 발사할 때

        if self.c_bullet == 0:  # 총알이 없을 때
            self.reload()
            self.update_bullet(self.all_bullet, self.all_bullet)
        else:  # 총알이 있을 때
            self.c_bullet-=1

    def update_bullet(self, c_bullet, all_bullet):  # 현재총알 / 전체총알을 화면에 표시
        self.bullet = self.godo_font.render(str(c_bullet) + '/' + str(all_bullet), True, BLACK)
        self.gamepad.blit(self.bullet, (620, 520))

    def update(self):  # 요소 전체를 표시
        self.update_bullet(self.c_bullet, self.all_bullet)


class Target:  # 떨어지는 아이템들

    def __init__(self, name, _gamepad):  # 왼쪽/오른쪽 방향을 결정 & 아이템 결정
        self.x_speed = 3

        self.y_a = 0.2
        self.y_speed = 7

        self.x = -3
        self.y = 300

        self.img_size = 50
        self.gamepad = _gamepad
        self.target_img = pygame.image.load("assets/" + name + ".png")
        self.target_img = pygame.transform.scale(self.target_img, (self.img_size, self.img_size))

        self.pos = random.randrange(1, 3)  # 왼쪽 오른쪽 방향결정
        if self.pos == 1:  # 왼쪽에서 시작
            pass

        if self.pos == 2:  # 오른쪽에서 시작
            self.x = 800
            self.x_speed = -3

    def update(self):  # 속도 & 가속도로 떨어지는 거 구현
        self.y_speed -= self.y_a
        self.x += self.x_speed
        self.y -= self.y_speed
        self.gamepad.blit(self.target_img, (self.x, self.y))

    def isbroke(self, mouse_x, mouse_y):  # 총에 맞았는지 확인
        self.cen_x = self.x + (self.img_size / 2)
        self.cen_y = self.y + (self.img_size / 2)
        if (self.cen_x - mouse_x)**2 + (self.cen_y - mouse_y)**2 <= (self.img_size/2)**2:  # Aim이 원 부등식 안에 포함되어있는지 확인
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            del self


    def check(self):  # 바닥에 떨어져있는지를 확인
        if self.y > 670:
            return False

        elif self.y <= 670:
            return True


def run_game():
    global gamepad, background
    done = False
    cross = CrossHair(gamepad)
    hud = Hud(gamepad)
    cnt = 0
    term = 60
    godo_font = pygame.font.Font('font/GodoM.ttf', 32)
    targets = []
    # ========== main game loop ========== #
    while not done:
        cnt += 1
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                hud.shoot()
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]

                for target in targets:
                    if target.isbroke(mouse_x, mouse_y):
                        del target

            elif event.type == pygame.QUIT:
                done = True

        gamepad.fill(WHITE)
        gamepad.blit(background, (0, 0))
        pygame.mouse.set_visible(False)

        if cnt == 4 * term:
            cnt = 0
            num = random.randrange(1, 3)
            targets = []
            for _ in range(num):
                target = Target('poison', gamepad)
                targets.append(target)

        hud.update()  #Hud를 화면에 표시

        target_len = len(targets)
        for index in range(target_len):  # Target 아이템들 모두 화면에 표시
            targets[index].update()
            targets[0].check()

        # target_group = pygame.sprite.RenderPlain(*targets)
        # target_group.update()
        cross.update()  #Aim 표시
        pygame.display.flip()
        clock.tick(60)
    # ========== end ========== #

    pygame.quit()


def main():  #배경화면 설정, 게임 main루프 실행
    global gamepad, background
    background = pygame.image.load("./assets/bg.png")
    background = pygame.transform.scale(background, (800, 600))
    pygame.init()
    gamepad = pygame.display.set_mode(size)
    pygame.display.set_caption("Game Title")
    run_game()


if __name__ == '__main__':  #main 함수 실행
    main()