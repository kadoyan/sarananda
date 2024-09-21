import pyxel
from lib.scene_manager import SceneManager

from lib.title import Title
from lib.game_core import GameCore
from lib.ending import Ending
from lib.game_over import GameOver
from lib.demo import Demo

import json

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 192

SCENE_TITLE = 0
SCENE_GAME = 1
SCENE_ENDING = 2
SCENE_GAMEOVER = 3
SCENE_DEMO = 4

class App:
    def __init__(self):
        # pyxel初期化
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=60, display_scale=3, title="Sarananda")
        with open(f"./assets/sarananda.json", "rt") as f:
            self.music = json.loads(f.read())
        
        pyxel.load("./assets/sarananda.pyxres")

        self.scene_manager = SceneManager()
        self.title = Title(self.scene_manager)
        self.game_core = GameCore(self.scene_manager)
        self.ending = Ending(self.scene_manager)
        self.gameover = GameOver(self.scene_manager)
        self.demo = Demo(self.scene_manager)
        
        # オブザーバー
        self.scene_manager.add_observer(self.title)
        self.scene_manager.add_observer(self.game_core)
        self.scene_manager.add_observer(self.ending)
        self.scene_manager.add_observer(self.gameover)
        self.scene_manager.add_observer(self.demo)
        
        for ch, sound in enumerate(self.music):
            set_channel = ch + 16
            pyxel.sounds[set_channel].set(*sound)

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.scene_manager.scene == SCENE_TITLE:
            self.title.update()

        elif self.scene_manager.scene == SCENE_GAME:
            # BGM
            if pyxel.play_pos(0) is None:
                for ch, sound in enumerate(self.music):
                    set_channel = ch + 16
                    pyxel.sound(set_channel).set(*sound)
                    pyxel.play(ch, set_channel, loop=True)

            self.game_core.update()
                
        elif self.scene_manager.scene == SCENE_ENDING:
            self.ending.update()
            
        elif self.scene_manager.scene == SCENE_GAMEOVER:
            self.gameover.update()
                
        elif self.scene_manager.scene == SCENE_DEMO:
            # BGM
            if pyxel.play_pos(0) is None:
                for ch in range(2):
                    pyxel.play(ch, ch + 18, loop=True)
            self.demo.update()

    def draw(self):
        pyxel.cls(0)

        if self.scene_manager.scene == SCENE_TITLE:
            self.title.draw()

        elif self.scene_manager.scene == SCENE_GAME:
            self.game_core.draw()
                
        elif self.scene_manager.scene == SCENE_ENDING:
            self.ending.draw()
                
        elif self.scene_manager.scene == SCENE_GAMEOVER:
            self.gameover.draw()
                
        elif self.scene_manager.scene == SCENE_DEMO:
            self.demo.draw()

if __name__ == "__main__":
    App()
