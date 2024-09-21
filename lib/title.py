import pyxel
from .observer import Observer

from .fade import Fade
from .key_input import KeyInput
from lib.sound_fade import SoundFade

LOGO_BASE_U = 48
LOGO_BASE_V = 0
LOGO_BASE_W = 178
LOGO_BASE_H = 8
LOGO_MARGIN_X = 40

STAR_MAX = 80


class Star:
    def __init__(self):
        self.x = pyxel.width / 2
        self.y = pyxel.height / 2
        self.radius = pyxel.rndf(0, 360)
        self.speed = pyxel.rndf(1, 10)
        self.color = 1

    def update(self, myList):
        self.speed += self.speed * 0.05
        self.x = pyxel.cos(self.radius) * self.speed + pyxel.width / 2
        self.y = pyxel.sin(self.radius) * self.speed + pyxel.height / 2

        if self.x < 0 or self.x > pyxel.width or self.y < 0 or self.y > pyxel.height:
            myList.remove(self)

    def draw(self):
        if self.speed < 90:
            pyxel.pset(self.x, self.y, self.color + int(self.speed // 20))
        else:
            pyxel.circ(self.x, self.y, 1, self.color + int(self.speed // 20))


class Title(Observer):
    def on_scene_change(self, scene):
        if scene == 0:
            self.reset()

    def reset(self):
        # print("タイトルリセット")
        pyxel.pal()
        pyxel.load("./assets/sarananda.pyxres")

        self.timer = 0  # タイトル画面演出用カウンター
        self.first_wait = 0  # 初期ウエイト
        self.step = 0  # ロゴ表示用カウンター
        self.direction = 1  # ロゴパーツ移動方向
        self.x = [  # ロゴ位置調整
            -LOGO_BASE_W,
            LOGO_BASE_W + LOGO_MARGIN_X * 2,
            -LOGO_BASE_W,
            LOGO_BASE_W + LOGO_MARGIN_X * 2,
            -LOGO_BASE_W,
            LOGO_BASE_W + LOGO_MARGIN_X * 2,
            -LOGO_BASE_W,
            LOGO_BASE_W + LOGO_MARGIN_X * 2,
        ]
        self.goto_game = False  # シーン移行フラグ

        self.stars = []  # 背景の星

        self.fade = Fade()  # フェード
        self.sound_fade = SoundFade() # 音楽フェード

    def __init__(self, scene_manager) -> None:
        self.scene_manager = scene_manager
        self.reset()

    def update(self):
        self.first_wait += 1

        if self.timer > 60 and len(self.stars) < STAR_MAX:
            self.stars.append(Star())

        for star in self.stars:
            star.update(self.stars)

        if self.step >= 6:
            self.timer += 1

        if KeyInput.is_pressed(KeyInput.ZBUTTON):
            self.goto_game = True

        if self.goto_game:
            self.sound_fade.update()
            if self.fade.fade_out():
                self.scene_manager.scene = 1
                self.sound_fade.reset()

    def draw(self):
        if self.timer > 60:
            for star in self.stars:
                star.draw()
        if self.first_wait > 60:
            for n in range(6):
                if self.step < 6:
                    self.x[self.step] += 2 * self.direction
                    if self.x[self.step] == 40:
                        pyxel.play(0, 0, loop=False)
                        self.step += 1
                        self.direction *= -1

                pyxel.blt(
                    self.x[n],
                    40 + LOGO_BASE_H + LOGO_BASE_H * n,
                    0,
                    LOGO_BASE_U,
                    LOGO_BASE_V + LOGO_BASE_H * n,
                    LOGO_BASE_W,
                    LOGO_BASE_H,
                    0,
                )

        if self.step >= 6:
            if self.timer == 20:
                pyxel.play(0, [1, 2, 2, 2, 2], loop=False)
            if self.timer == 24:
                pyxel.play(2, [1, 2, 2, 2, 2], loop=False)
            # 左下
            if self.timer > 20:
                pyxel.blt(LOGO_MARGIN_X + 27, 80, 0, 48, 48, 16, 24, 0)
            # 上
            if self.timer > 25:
                pyxel.blt(LOGO_MARGIN_X + 75, 40, 0, 64, 48, 56, 16, 0)
            # 下
            if self.timer > 30:
                pyxel.blt(LOGO_MARGIN_X + 71, 80, 0, 64, 64, 48, 32, 0)
            # 中
            if self.timer > 32:
                pyxel.blt(LOGO_MARGIN_X + 72, 48, 0, 112, 80, 32, 32, 0)
            # 上
            if self.timer > 33:
                pyxel.blt(LOGO_MARGIN_X + 90, 32, 0, 112, 64, 32, 16, 0)
            # 先端
            if self.timer > 34:
                pyxel.blt(LOGO_MARGIN_X + 112, 16, 0, 128, 48, 48, 16, 0)
            if self.timer > 60:
                pyxel.text(
                    LOGO_MARGIN_X + 2,
                    120,
                    'BASED ON THE MSX-FAN READER\'S SUBMISSION\nBASIC PROGRAM "SARANANDA."',
                    12,
                )
                pyxel.text(
                    LOGO_MARGIN_X + 5,
                    170,
                    "2024 KADOYAN / SPECIAL THANKS:frenchbread",
                    6
                )
                if self.timer % 24 > 0:
                    pyxel.pal(15, 10)
                if self.timer % 24 > 8:
                    pyxel.pal(15, 12)
                if self.timer % 24 > 16:
                    pyxel.pal(15, 9)
            else:
                pyxel.pal(15, 10)
            if self.timer & 120 > 60:
                pyxel.text(
                    LOGO_MARGIN_X + 2,
                    140,
                    "PRESS Z or SPACE KEY or TRIGGER A to START",
                    7,
                    self.scene_manager.jafont,
                )
