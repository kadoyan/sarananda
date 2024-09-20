import pyxel

class SoundFade:
    def __init__(self):
        self.fade = False
        
        # gain初期値を記録
        self.default_gain = [1.0, 0.3, 0.3, 0.6]
        for tone in pyxel.tones:
            self.default_gain.append(tone.gain)

    def update(self):
        self.fade = not self.fade

        if self.fade:
            for tone in pyxel.tones:
                if tone.gain > 0.001 and pyxel.frame_count % 5 == 0:
                    tone.gain *= 0.75
                    
    def reset(self):
        pyxel.stop()
        for idx, tone in enumerate(pyxel.tones):
            tone.gain = self.default_gain[idx]
