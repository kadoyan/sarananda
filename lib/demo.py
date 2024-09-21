import pyxel
from .observer import Observer
from .type_writer import TypeWriter
from .scene_manager import SceneManager
from .fade import Fade
from .pseudo_3d import Pseudo3D
from .sound_fade import SoundFade
from collections import deque

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 192

class PowerBar:
    def __init__(self, x:int, y:int, w:float, h:float, border:int, fill:int, target):
        self.x, self.y, self.w, self.h, self.border, self.fill, self.target = [x, y, w, h, border, fill, target]
        self.val = 0
        
    def draw(self, val:float):
        val_width = min(self.w * val - 2, 100)
        self.target.rectb(self.x, self.y, self.w, self.h, self.border)
        self.target.rect(self.x + 1, self.y + 1, self.w - 2, self.h -2 , 0)
        self.target.rect(self.x + 1, self.y + 1, val_width, self.h -2 , self.fill)

class Demo(Observer):
    def __init__(self, scene_manager) -> None:
        self.scene_manager = scene_manager
        self.start_frame = pyxel.frame_count
        
        self.fade_in = Fade()
        self.fade_out = Fade()
        self.sound_fade = SoundFade()
        
        self.messages = [
            ["ミッションログ Ｎｏ．１４６７３８２０９", 7],
            ["消息を絶った宇宙艦隊の調査のため、わたしは、超高性能宇宙戦闘機「ＤＯＴ　ＶＩＰＥＲ」で問題の宙域に急行した。", 7],
            ["調査を開始してまもなく、機体に搭載されたハイパーＡＩ「ミケランジェロ」がわずかな次元のゆらぎをとらえた。そしてその時、異変が起きたのだ。", 7],
            ["ミケランジェロ「強力な次元フィールドにとらえられました。次元のはざまに吸い込まれます！」", 12],
            ["ミケランジェロ「…………………………………………", 12],
            ["ミケランジェロ「……………………", 12],
            ["ミケランジェロ「通常空間にもどりました………座標の取得に失敗しました。現在地は不明です。", 12],
            ["ミケランジェロ「周囲に異常な高温と核融合反応、強力な重力を確認。恒星の内部と推測されます。", 12],
            ["ミケランジェロ「機体保護のため、火器管制システムをシャットダウン、シールドに動力を集中させます。", 12],
            ["「もしや、艦隊もここに？", 7],
            ["ミケランジェロ「残念ながら、強力な重力に囚われてしまったようです。救出は絶望的です。", 12],
            ["ミケランジェロ「未確認のエナジーフィールドで空間がたもたれていますが、崩壊が始まっています。このままではわたしたちも炎に飲まれます。", 12],
            ["「……我々には、この状況を報告する義務がある。", 7],
            ["ミケランジェロ「ラジャー。脱出ルートを算出しました。強力な重力と、高温のプラズマに注意してください。", 12],
            ["ミケランジェロ「艦隊の船体からシールドエナジーがもれ出しているようです。回収を推奨します。", 12],
            ["「よし、発進だ！", 7]
        ]
        self.message_index = 0
        self.visual_height = 88
        self.visual_width = 184
        self.offscreen = pyxel.Image(self.visual_width, self.visual_height)
        self.multi_timer = 0
        
        self.weapon_bar = PowerBar(30, 73, 50, 4, 9, 10, self.offscreen)
        self.shield_bar = PowerBar(30, 81, 50, 4, 13, 12, self.offscreen)
        self.bar_shift = 0
        
        self.pip_size = [0] * 4

        self.type_writer = TypeWriter(
            24, 130, self.scene_manager, self.messages, 8, 3
        )


    def update(self):
        if self.start_frame + 60 < pyxel.frame_count:
            self.fade_in.fade_in()
            # BGM
            if pyxel.play_pos(0) is None:
                pyxel.play(2, 18, loop=True)
                pyxel.play(3, 19, loop=True)

            self.offscreen.cls(0)
            for x in range(-4000, 4000, 500):
                left = Pseudo3D.convert(x, 800, 1, self.visual_width, self.visual_height)
                right = Pseudo3D.convert(x, 800, 80, self.visual_width, self.visual_height)
                self.offscreen.line(
                    left[0],
                    left[1] - 40,
                    right[0],
                    right[1] - 40,
                    11,
                )
            for z in range(1, 80, 10):
                y = Pseudo3D.convert(0, 800, z - pyxel.frame_count / 4 % 10, self.visual_width, self.visual_height)
                self.offscreen.line(
                    0,
                    y[1] - 44,
                    self.visual_width,
                    y[1] - 44,
                    11,
                )
            
            # なんか線のついたやつ
            if pyxel.frame_count % 60 > 30:
                self.offscreen.blt(100, 0, 0, 176, 48, 32, 16, 0)
            if pyxel.frame_count % 100 > 50:
                self.offscreen.blt(94, 40, 0, 176, 48, 32, -16, 0)
            if pyxel.frame_count % 40 > 20:
                self.offscreen.blt(84, 20, 0, 208, 48, 16, 16, 0)
            # 謎の円
            center_x = 165
            center_y = 65
            self.offscreen.circ(center_x, center_y, 12, 0)
            colors = [1, 11, 13, 12]
            for n in range(4):
                x1 = pyxel.cos((pyxel.frame_count + n * 4) * 4 + 8) * 12 + center_x
                y1 = pyxel.sin((pyxel.frame_count + n * 4) * 4 + 8) * 12 + center_y
                x2 = pyxel.cos((pyxel.frame_count + n * 4) * 4 - 8) * 12 + center_x
                y2 = pyxel.sin((pyxel.frame_count + n * 4) * 4 - 8) * 12 + center_y
                self.offscreen.tri(x1, y1, x2, y2, center_x, center_y, colors[n])
                
            # cos1 = pyxel.cos(pyxel.frame_count * 4 + 16)
            # sin1 = pyxel.sin(pyxel.frame_count * 4 + 16)
            # cos2 = pyxel.cos(pyxel.frame_count * 4 - 16)
            # sin2 = pyxel.sin(pyxel.frame_count * 4 - 16)
            # x1, y1, x2, y2 = [cos1 * 12 + center_x, sin1 * 12 + center_y, cos2 * 12 + center_x, sin2 * 12 + center_y]
            # self.offscreen.tri(x1, y1, x2, y2, center_x, center_y, 11)
            self.offscreen.circ(center_x, center_y, 4, 11)
            self.offscreen.circb(center_x, center_y, 12, 11)
            if pyxel.frame_count % 60 > 10:
                self.offscreen.blt(124, 72, 0, 176, 48, -32, -16, 0)
                    
            # 棒グラフみたいなの
            self.offscreen.text(4, 72, "WEAPON", 9)
            self.offscreen.text(4, 80, "SHIRLD", 12)
            
            if self.type_writer.message_index <= 7:
                self.bar_shift = pyxel.rndf(0, 0.05)
            
            if self.type_writer.message_index > 7:
                self.bar_shift = min(self.bar_shift + 0.005, 0.8)
                
            self.weapon_bar.draw(.8 - self.bar_shift)
            self.shield_bar.draw(.2 + self.bar_shift)
            
            # PiP
            if self.type_writer.message_index in (1, 2):
                self.pip_size[0] = min(self.pip_size[0] + 0.05, 1)
                self.offscreen.blt(4, 4, 0, 160, 112, 64, 48, None, 0, self.pip_size[0])
                
            if self.type_writer.message_index >= 7:
                self.pip_size[1] = min(self.pip_size[1] + 0.05, 1)
                self.offscreen.blt(4, 4, 0, 144, 64, 64, 48, None, 0, self.pip_size[1])
                
            if self.type_writer.message_index >= 10:
                self.pip_size[2] = min(self.pip_size[2] + 0.05, 1)
                self.offscreen.blt(132, 8, 0, 208, 64, 48, 48, None, 0, self.pip_size[2])
                
            if self.type_writer.message_index >= 14:
                self.offscreen.blt(124, 48, 0, 48, 80, 16, 16)
                color = 5 + pyxel.frame_count % 3
                self.offscreen.rectb(124, 48, 16, 16, color)
            
            # メッセージ
            if self.type_writer.update(self.messages[self.message_index]):
                self.sound_fade.update()
                if self.fade_out.fade_out():
                    self.scene_manager.scene = 0
                    self.sound_fade.reset()
            else:
                # ノイズエフェクト    
                if self.type_writer.message_index in (3, 4):
                    if self.multi_timer < 30:
                        self.multi_timer += .5
                    self.make_noise(self.multi_timer)
                    
                if self.type_writer.message_index == 5:
                    if self.multi_timer > 0:
                        self.multi_timer -= .5
                        self.make_noise(self.multi_timer)
                
                if self.type_writer.message_index >= 5:
                    if pyxel.frame_count % 80 > 70:
                        self.make_noise(pyxel.frame_count % 5)

    def draw(self):
        pyxel.cls(0)
        if self.start_frame + 60 < pyxel.frame_count:
            self.type_writer.draw()

            self.visual_x = 38
            self.visual_y = 24
            shake_x = 0
            shake_y = 0
            if self.type_writer.message_index in (3, 4):
                shake_x = pyxel.rndi(-2, 2)
                shake_y = pyxel.rndi(-2, 2)
            pyxel.blt(
                self.visual_x + shake_x,
                self.visual_y + shake_y,
                self.offscreen,
                0,
                0,
                self.visual_width,
                self.visual_height,
                0,
            )
            pyxel.rectb(
                self.visual_x - 1 + shake_x,
                self.visual_y - 1 + shake_y,
                self.visual_width + 2,
                self.visual_height + 2,
                6,
            )
            pyxel.rectb(
                self.visual_x - 3 + shake_x,
                self.visual_y - 3 + shake_y,
                self.visual_width + 6,
                self.visual_height + 6,
                5,
            )

    def pseudo_3d(self, x: float, y: float, z: float, w:int, h:int):
        if z == 0:
            z = -1
        s = 1 / z
        x = x * s + w / 2
        y = y * s + h / 2
        return [x, y, s]
    
    def make_noise(self, timer:float):
        offscreen = self.offscreen.data_ptr()
        for idx in range(0, len(offscreen), 3):
            data = offscreen[idx]
            data = data + pyxel.rndi(0, data + int(timer))
            offscreen[idx] = data
        # dequeに変換
        newdata = deque(offscreen)
        # ローテーション
        newdata.rotate(pyxel.rndi(-4, 4))
        offscreen[:] = list(newdata)[:]
        
if __name__ == "__main__":
    App()
