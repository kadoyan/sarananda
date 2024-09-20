import pyxel

class Fade:
    def __init__(self):
        self.step = 0
        self.palette_step = [0, 0, 1, 1, 2, 1, 13, 6, 4, 4, 9, 3, 13, 1, 13, 14]
        
    def fade_out(self):
        return self.fade_core(False)
            
    def fade_in(self):
        if self.step < 10:
            return self.fade_core(True)
        else:
            return True
            
    def reset(self):
        pyxel.pal()
        self.step = 0
        
    def fade_core(self, fadein:bool):
        self.step += 0.1
        for color in range(0,16):
            target_palette = color
            if fadein: # Fade in
                for loop in range(5, int(self.step), -1):
                    target_palette = self.palette_step[target_palette]
            else: # Fade out
                for loop in range(int(self.step)):
                    target_palette = self.palette_step[target_palette]
            pyxel.pal(color, target_palette)
        if self.step >= 10:
            return True
        return False
