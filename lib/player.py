import pyxel
from dataclasses import dataclass
from statistics import median

from .key_input import KeyInput
from .collision import Collision
from .manga_line import Triangles
from .explosion import Explosion

GRAVITY = 0.04
MAX_Y = 1.5
MAX_X = 1.2
PADDING = [2, 4] # 衝突判定余白x,y

class Player:
    def __init__(self, collision_target, scene_manager) -> None:
        self.scene_manager = scene_manager
        self.collision_target = collision_target
        self.x = 50 #50, 80, 0, 0, 32, 16, 8, 0, 
        self.y = 80
        self.bank = 0
        self.u = 0
        self.v = 32
        self.w = 16
        self.h = 16
        self.alpha = 3
        self.dy = 0
        self.dx = 0
        self.sprite_shift = 0
        self.burner = 0
        self.body = [0, 0]
        self.hit = False
        self.effect = 0
        self.is_gameover = False
        self.explosion = []
        self.playable_height = pyxel.height - self.scene_manager.status_height

    def update(self, spaceship):
        self.burner = 2
        self.hit = False
        if self.effect > 0:
            self.effect -= 1
        
        if not self.is_gameover:
            # X座標
            if KeyInput.is_pressed(KeyInput.LEFT):
                self.dx -= 0.2
                self.burner = 0
            if KeyInput.is_pressed(KeyInput.RIGHT):
                self.dx += 0.2
                self.burner = 1
            self.dx = median([-MAX_X, self.dx, MAX_X])
            self.x += self.dx
            self.x = median([0, self.x, pyxel.width - self.w])
            if self.x > pyxel.width / 3:
                self.scene_manager.acceleration = 4 * (self.x / pyxel.width)
            else:
                self.scene_manager.acceleration = 1

            # Y座標
            self.dy = min(self.dy + GRAVITY, MAX_Y)
            if KeyInput.is_pressed(KeyInput.ZBUTTON):
                self.dy -= GRAVITY * 3
                self.burner = 1
            self.dy = median([-MAX_Y, self.dy, MAX_Y])
            self.y += self.dy
            self.y = median([0, self.y, self.playable_height])

            # スプライト
            if self.dy > 1:
                self.sprite_shift = self.w
            elif self.dy < -1:
                self.sprite_shift = self.w * 2
            else:
                self.sprite_shift = 0

            # コリジョンボックス
            self.body = [
                self.x + PADDING[0],
                self.y + PADDING[1],
                self.x - PADDING[0] + self.w,
                self.y - PADDING[1] + self.h,
            ]

            self.check_life(spaceship)
        else:
            if len(self.explosion) < 6:
                self.explosion.append(
                    Explosion(
                        pyxel.rndi(0, 10),
                        pyxel.rndi(0, 10),
                        [13, 12, 7],
                        1,
                        8)
                    )
            for exp in self.explosion:
                exp.update(self.explosion)

    def draw(self):
        if not self.is_gameover:
            #Booster
            burner_frame = 4 * pyxel.rndi(0, 1)
            if self.burner > 0:
                pyxel.blt(
                    self.x - 8,
                    self.y + 6,
                    self.bank,
                    self.u + (self.burner + 1) * 8,
                    self.v + self.h + burner_frame,
                    8,
                    4,
                    0,
                )
                # pyxel.text(self.x, self.y+8, str(self.burner), 7)
            
            #Player
            if self.effect <= 0:
                pyxel.blt(
                    self.x,
                    self.y,
                    self.bank,
                    self.u + self.sprite_shift,
                    self.v,
                    self.w,
                    self.h,
                    self.alpha,
                )
            else:
                if pyxel.frame_count % 4 <= 2:
                    pyxel.blt(
                        self.x,
                        self.y,
                        self.bank,
                        self.u + self.sprite_shift,
                        self.v,
                        self.w,
                        self.h,
                        self.alpha,
                    )
            
            # shield
            if self.effect > 0 and pyxel.frame_count % 4 <= 2:
                pyxel.blt(
                    self.x,
                    self.y,
                    self.bank,
                    0, 56,
                    16, 8,
                    self.alpha,
                )
                pyxel.blt(
                    self.x,
                    self.y + 8,
                    self.bank,
                    0, 56,
                    16, -8,
                    self.alpha,
                )
            #Manga lines
            if self.effect > 25:
                Triangles.draw(3, 300, 3, self.x + self.w / 2, self.y + self.h / 2, 7)

        else:
            for exp in self.explosion:
                exp.draw(self.x, self.y)
            

    def check_life(self, spaceship):
        targets = self.collision_target.get_collision_boxes()
        damage = False
    
        # エネルギー
        for ship in spaceship:
            items = ship.get_energies()
            for item in items:
                collision, directions = Collision.is_collision(self.body, item.collision_box)
                if collision:
                    self.scene_manager.energies += 1
                    pyxel.play(3, 7, resume=True)
                    ship.delete_energy(item)
                    if self.scene_manager.max_shield >= self.scene_manager.shield + 1:
                        self.scene_manager.shield += 1
        
        # 床と天井
        MARGIN_TOP = 4
        MARGIN_BOTTOM = 16
        if self.y < MARGIN_TOP:
            self.dy = 1.2
        if self.y > self.playable_height - MARGIN_BOTTOM:
            self.dy = -1.5
        
        # 炎
        if self.effect < 1:
            if self.y < MARGIN_TOP or self.y > self.playable_height - MARGIN_BOTTOM:
                damage = True
            else:
                for target in targets:
                    collision, directions = Collision.is_collision(self.body, target)
                    if collision:
                        damage = True
                        
            if damage:
                self.hit = True
                self.effect = 40
                self.scene_manager.shield -= 1
                self.scene_manager.damages += 1
                pyxel.play(3, 4, resume=True)
                if self.scene_manager.shield <= 0:
                    self.is_gameover = True
        return False
