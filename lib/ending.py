import pyxel
from .observer import Observer

from .fade import Fade
from .sound_fade import SoundFade
from .show_results import ShowResults


class Ending(Observer):
    def on_scene_change(self, scene):
        if scene == 2:
            self.reset()
            
    def reset(self):
        
        self.timer = 0  # エンディング用カウンター
        self.dx = pyxel.width + 120  # X移動計算用
        self.dy = pyxel.height - 20  # Y移動計算用
        self.start = 100  # 演出タイミング

        self.sun_rotation = 0  # 太陽自転用カウンター
        self.goto_title = False  # タイトル移行フラグ

        # フェード処理
        self.fade_in = Fade()
        self.fade_out = Fade()
        
        self.show_results = ShowResults(self.scene_manager)

        # 太陽
        self.sun_x = 140  # 太陽移動用
        self.sun_r = 30  # 太陽半径
        self.sun_plate = pyxel.Image(self.sun_r * 2, self.sun_r * 2)

    def __init__(self, scene_manager):
        self.scene_manager = scene_manager

        self.reset()

        self.star = []
        for n in range(200):
            self.star.append(
                [
                    pyxel.rndi(10, pyxel.width - 10),
                    pyxel.rndi(10, pyxel.height - 10),
                    [1, 5],
                ]
            )

    def update(self):
        self.timer += 1
        if self.timer >= self.start + 140:
            self.dx *= 0.9
            self.dy *= 0.9

        if self.timer >= self.start + 460:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_Z):
                self.goto_title = True

        if self.goto_title:
            if self.fade_out.fade_out():
                self.scene_manager.scene = 0

        self.sun_plate.cls(0)
        self.sun_rotation += 0.2
        r = self.sun_r

        # 太陽ノイズ
        x, y = [0, 0]
        for ny in range(r * 2):
            for nx in range(r * 2):
                n = pyxel.noise(
                    nx / 3,
                    ny / 3,
                    pyxel.frame_count / 120,
                )
                if n > 0.2:
                    col = 0
                elif n > 0:
                    col = 8
                elif n > -0.6:
                    col = 9
                else:
                    col = 10
                self.sun_plate.pset(nx + x, ny + y, col)
                
        if self.timer >= self.start + 100:
            self.show_results.update()

    def draw(self):
        pyxel.cls(0)
        self.fade_in.fade_in()

        for star in self.star:
            pyxel.pset(star[0], star[1], star[2][pyxel.rndi(0, len(star[2]) - 1)])
        # self.repeat_scroll(0, 0, 0, 0, self.sun_r * 2, self.sun_r * 2, self.sun_plate)

        # 太陽コピー
        x, y, v, w, h = [140 - self.sun_x, 30, 0, self.sun_r * 2, 2]
        self.sun_x *= 0.99
        for line in range(0, self.sun_r, 2):
            shift = self.sun_r * 2 * (self.sun_r - line)
            # 上半分
            self.repeat_scroll(
                x,
                y + line,
                self.sun_rotation % shift / (self.sun_r - line),
                line,
                w,
                h,
                self.sun_plate,
            )
            # 下半分
            self.repeat_scroll(
                x,
                y + self.sun_r * 2 - line - 2,
                self.sun_rotation % shift / (self.sun_r - line),
                self.sun_r * 2 - line - 2,
                w,
                h,
                self.sun_plate,
            )

        # アイリスエフェクト
        r = self.sun_r
        cx, cy = [x + r, y + r]
        for my in range(y, 91, 1):
            mx = pyxel.sqrt(r * r - (my - cy) * (my - cy)) + cx
            pyxel.line(x + r * 2, my, mx, my, 0)
            pyxel.line(x, my, cx - mx + x + r, my, 0)

        pyxel.circb(x + self.sun_r, y + self.sun_r, self.sun_r + 2, 8)
        pyxel.circb(x + self.sun_r, y + self.sun_r, self.sun_r + 1, 10)
        pyxel.circb(x + self.sun_r, y + self.sun_r, self.sun_r, 9)

        if self.timer >= self.start:
            sx, sy = [
                x + self.sun_r + self.timer - 80,
                y + self.sun_r * 1.5 + (self.timer / 10),
            ]
            length = pyxel.rndi(1, 3)
            pyxel.line(
                sx + pyxel.cos(self.timer * 5) * length,
                sy + pyxel.sin(self.timer * 5) * length,
                sx - pyxel.cos(self.timer * 5) * length,
                sy - pyxel.sin(self.timer * 5) * length,
                7,
            )
            length = pyxel.rndi(1, 3)
            pyxel.line(
                sx + pyxel.cos(self.timer * 5 + 90) * length,
                sy + pyxel.sin(self.timer * 5 + 90) * length,
                sx - pyxel.cos(self.timer * 5 + 90) * length,
                sy - pyxel.sin(self.timer * 5 + 90) * length,
                7,
            )
            pyxel.pset(sx, sy, 12)
        if self.timer == self.start + 140:
            pyxel.play(0, 9)
        
        if self.timer >= self.start + 140:
            # ブースター
            # x, y = [self.dx + 40, self.dy + 70 + pyxel.sin(self.timer * 2) * 2]
            x, y = [self.dx - 140, self.dy - 30 + pyxel.sin(self.timer * 2) * 6]
            pyxel.circ(x + 76, y + 56, pyxel.rndi(10, 12), 9)
            pyxel.circ(x + 76, y + 56, pyxel.rndi(8, 10), 10)
            pyxel.circ(x + 76, y + 56, pyxel.rndi(7, 8), 7)
            pyxel.circ(x + 54, y + 60, pyxel.rndi(10, 12), 9)
            pyxel.circ(x + 54, y + 60, pyxel.rndi(8, 10), 10)
            pyxel.circ(x + 54, y + 60, pyxel.rndi(7, 8), 7)
            # 自機
            pyxel.blt(x, y, 0, 48, 112, 112, 64, 3, 0, 1)

        if self.timer >= self.start + 100:
            self.show_results.draw()

        if self.timer >= self.start + 460:
            x = 60
            pyxel.text(
                x,
                pyxel.height - 40,
                "THANK YOU for PLAYING!",
                [2, 12, 6, 7, 8, 10][pyxel.rndi(0, 5)],
            )
            pyxel.text(x, pyxel.height - 30, "PRESS Z or SPACE KEY or TRIGGER A", 7, self.scene_manager.jafont)

    def repeat_scroll(self, x, y, u, v, w, h, target):
        # 無限スクロール
        pyxel.blt(x + u, y, self.sun_plate, 0, v, w - u, h)
        pyxel.blt(x, y, self.sun_plate, w - u, v, u, h)


if __name__ == "__main__":
    App()
