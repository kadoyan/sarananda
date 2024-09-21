import pyxel

from .score_calc import ScoreCalc
from .convert_timeformat import ConvertTimeFormat

class ShowResults:
            
    def __init__(self, scene_manager) -> None:
        self.timer = 0
        self.goto_title = False
        self.result_value = None
        self.scene_manager = scene_manager
        self.result_color = (
            7, 7, 7, 7, 12, 12, 8, 12, 12, 12, 12, 10
        )
            
        self.result_key = (
            "TIME",
            "SHIELD",
            "ENERGY CUBE",
            "DAMAGE",
            "BASE SCORE",
            "COMPLETE BONUS",
            "DAMAGE PENALTY",
            "SHIELD BONUS",
            "MAX SHIELD BONUS",
            "ENERGY CUBE BONUS",
            "NO DAMAGE BONUS",
            "TOTAL SCORE"
        )

    def update(self):
        self.timer += 1
        self.result = ScoreCalc.score(self.scene_manager)
        self.result_value = [
            ConvertTimeFormat.convert_to_minutes_seconds_milliseconds(self.scene_manager.play_time),
            self.scene_manager.shield,
            self.scene_manager.energies,
            self.scene_manager.damages,
            self.result["distance_score"],
            self.result["comp_bonus"],
            self.result["damege_penalty"],
            self.result["shield_score"],
            self.result["fullshield_score"],
            self.result["energy_score"],
            self.result["nodamage_score"]
        ]
        if len(self.result_key) > len(self.result_value):
            total = sum(self.result_value[4:])
            conv_total = self.to_full_width(total)
            self.result_value.append(conv_total)
    
    def draw(self):
        if self.timer <= 1:
            pyxel.pal()
            
        if self.timer > 60:
            
            x_base = 40
            y_base = 20
            
            for idx, key in enumerate(self.result_key):
                jafont = None
                if len(self.result_key) - 1 == idx:
                    jafont = self.scene_manager.jafont
                if self.timer > 120 + idx * 20:
                    pyxel.text(x_base, y_base + 10 * idx, f"{key}: {self.result_value[idx]}" , self.result_color[idx], jafont)
    
    def to_full_width(self, text):
        # 半角数字と全角数字の対応表を作成
        trans_table = str.maketrans("0123456789", "０１２３４５６７８９")
        # 変換
        return str(text).translate(trans_table)
