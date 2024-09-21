import pyxel
from .observer import Observer

from .fade import Fade
from .sound_fade import SoundFade
from .show_results import ShowResults

class GameOver(Observer):
    def on_scene_change(self, scene):
        if scene == 3:
            self.reset()
            
    def reset(self):
        self.goto_title = False
        self.fade_out = Fade()
        self.sound_fade = SoundFade()
        self.show_results = ShowResults(self.scene_manager)
            
    def __init__(self, scene_manager) -> None:
        self.scene_manager = scene_manager
        self.reset()

    def update(self):
        self.show_results.update()
        if self.goto_title:
            if self.fade_out.fade_out():
                self.scene_manager.scene = 0

        if self.show_results.timer >= 360:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_Z):
                self.goto_title = True
    
    def draw(self):
        self.show_results.draw()

        if self.show_results.timer >= 360:
            pyxel.text(160, 80, "GAME OVER", 8, self.scene_manager.jafont)
            if self.show_results.timer % 80 > 20:
                pyxel.text(62, 160, "PRESS Z / SPACE KEY / TRIGGER A", 10, self.scene_manager.jafont)
