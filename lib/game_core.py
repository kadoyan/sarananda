import pyxel
from .observer import Observer

from .tile_shift import TileShift
from .prominence import Prominences
from .magma_perlin_noice import Magma
from .player import Player
from .status import Status
from .sparks import Sparks
from .spaceship import SpaceShip
from .sound_fade import SoundFade

from .fade import Fade

class GameCore(Observer):
    def on_scene_change(self, scene):
        if scene == 1:
            self.reset()
            
    def reset(self):
        # print("ゲームコアリセット")
        # ゲーム画面高さ
        self.game_height = pyxel.height - self.scene_manager.status_height

        # プロミネンス
        self.prominences = Prominences(self.scene_manager)

        # プレイヤー
        self.player = Player(self.prominences, self.scene_manager)

        # 背景
        magma_height = 16
        self.magma = Magma(
            -2,
            self.game_height - magma_height + 2,
            magma_height,
            self.scene_manager,
        )
        self.sparks = Sparks(self.scene_manager, 30)
        self.spaceship = []

        # フェード
        self.fadein = Fade()
        self.fadeout = Fade()
        self.sound_fade = SoundFade()
        
        # 時間
        self.start_frame = pyxel.frame_count
        
        # ゲーム変数リセット
        self.scene_manager.reset()
    
    def __init__(self, scene_manager):
        # seed(114)
        self.scene_manager = scene_manager
        
        self.reset()

    def update(self):
        self.scene_manager.position += self.scene_manager.acceleration
        self.scene_manager.play_time = pyxel.frame_count - self.start_frame

        if int(self.scene_manager.position) % 1500 >= 1480 and len(self.spaceship) <= 0:
            self.spaceship.append(SpaceShip(self.scene_manager))
        for ship in self.spaceship:
            ship.update(self.spaceship)
            if ship.get_status():
                self.spaceship.remove(ship)

        # 遠景シフト
        for n in range(6):
            timing = (4 + n) - int(self.scene_manager.acceleration)
            TileShift.update(0, -1, 8, 8, n * 8, 16, timing)
            TileShift.update(0, -1, 8, 8, n * 8, 24, timing)

        self.player.update(self.spaceship)
        self.magma.update()
        self.sparks.update()
        if self.scene_manager.position > 500:
            self.prominences.update()
            
        self.is_gameover()
        self.is_goal()

    def draw(self):
        self.fadein.fade_in()

        if self.player.effect < 10:
            pyxel.camera()
        else:
            pyxel.camera(pyxel.rndi(-2, 2), pyxel.rndi(-2, 2))

        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, self.game_height, 0)
        self.prominences.draw()

        for ship in self.spaceship:
            ship.draw()

        self.magma.draw()
        self.sparks.draw()
        self.player.draw()
        # self.firewall.draw()

        pyxel.camera()
        Status.draw(self.scene_manager)

    def is_goal(self):
        if self.scene_manager.position >= self.scene_manager.distance:
            self.sound_fade.update()
            if self.fadeout.fade_out():
                self.scene_manager.scene = 2
                self.sound_fade.reset()
        return False

    def is_gameover(self):
        if self.scene_manager.shield <= 0:
            self.sound_fade.update()
            if self.fadeout.fade_out():
                self.scene_manager.scene = 3
                self.sound_fade.reset()
        return False
