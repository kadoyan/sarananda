import pyxel
from .observer import Observer

from lib.score_calc import ScoreCalc
from lib.convert_timeformat import ConvertTimeFormat
from lib.fade import Fade

class GameOver(Observer):
    def on_scene_change(self, scene):
        if scene == 3:
            self.reset()
            
    def reset(self):
        self.timer = 0
        self.fade = Fade()
        self.goto_title = False
        self.result_value = []
            
    def __init__(self, scene_manager) -> None:
        self.scene_manager = scene_manager
        self.result_color = (
            7, 7, 7, 7, 12, 12, 12, 12, 12, 9
        )
            
        self.result_key = (
            "TIME",
            "SHIELD",
            "ENERGY",
            "DAMAGE",
            "DISTANCE SCORE",
            "SHIELD BONUS",
            "MAX SHIELD BONUS",
            "ENERGY BONUS",
            "NO DAMAGE BONUS",
            "TOTAL SCORE"
        )
        self.reset()

    def update(self):
        self.timer += 1
        self.result = ScoreCalc.score(self.scene_manager)
        self.result_value = [
            ConvertTimeFormat.convert_to_minutes_seconds_milliseconds(self.scene_manager.play_time),
            self.scene_manager.shield,
            self.scene_manager.energies,
            self.scene_manager.damages,
            self.result["distance_score"],
            self.result["shield_score"],
            self.result["fullshield_score"],
            self.result["energy_score"],
            self.result["nodamage_score"]
        ]
        if len(self.result_key) > len(self.result_value):
            total = sum(self.result_value[4:])
            self.result_value.append(total)

        if self.timer >= 420:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_Z):
                self.goto_title = True

        if self.goto_title:
            if self.fade.fade_out():
                self.scene_manager.scene = 0
    
    def draw(self):
        if self.timer <= 1:
            pyxel.pal()
            
        if self.timer > 60:
            
            x_base = 50
            y_base = 20
            time_base = 120
            
            for idx, key in enumerate(self.result_key):
                if self.timer > 120 + idx * 20:
                    pyxel.text(x_base, y_base + 12 * idx, f"{key}: {self.result_value[idx]}" , self.result_color[idx])

        if self.timer >= 460:
            pyxel.text(160, 80, "GAME OVER", 8, self.scene_manager.jafont)
            if self.timer % 80 > 20:
                pyxel.text(62, 160, "PRESS Z / SPACE KEY / TRIGGER A", 9, self.scene_manager.jafont)
