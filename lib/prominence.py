import pyxel
from dataclasses import dataclass
# from random import choice

# プロミネンスの移動量候補
JUMP_WIDTH = [40, 50, 60, 70, 80]
JUMP_HEIGHT = [70, 90, 110, 120]


# プロミネンス
@dataclass
class Prominence:
    x: float
    y: float
    speed_x: float
    speed_y: float
    radian = 0
    remove = False
    collision_boxes = []


# 飛沫
@dataclass
class Particle:
    x: float
    y: float
    delay: int
    jump: float
    move_x: float
    direction: int


class Prominences:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.prominences = []  # プロミネンス
        self.particles = []  # 飛沫
        self.collision_boxes = []  # 衝突判定用座標リスト
        self.seed = 0

    def update(self):
        self.collision_boxes = []  # 衝突リスト初期化

        # プロミネンス生成
        if pyxel.frame_count % 80 == 0:
            pyxel.rseed(self.seed)
            self.seed += 1
            new_prominense = Prominence(
                pyxel.width // 2 + pyxel.rndi(pyxel.width // 8, pyxel.width // 4) * int(self.scene_manager.acceleration),
                pyxel.rndi(0, 1) * (pyxel.height - self.scene_manager.status_height),
                JUMP_WIDTH[pyxel.rndi(0, len(JUMP_WIDTH) - 1)],
                JUMP_HEIGHT[pyxel.rndi(0, len(JUMP_HEIGHT) - 1)],
            )
            self.prominences.append(new_prominense)
            pyxel.play(3, 3, resume=True)

        # プロミネンス動かす
        for prominence in self.prominences:
            prominence.x -= 0.5 * self.scene_manager.acceleration
            prominence.radian -= 1.5
            if prominence.remove:
                self.prominences.remove(prominence)

        # パーティクル動かす
        for particle in self.particles:
            particle.delay -= 1
            particle.x -= 0.5 * self.scene_manager.acceleration
            if particle.delay <= 0:
                particle.y -= particle.direction * particle.jump
                particle.jump -= 0.05
                if abs(particle.jump) > 1:
                    self.particles.remove(particle)

    def draw(self):
        for prominence in self.prominences:
            for c in range(0, 3):
                for i in range(0, 28):
                    direction = -1
                    if prominence.y != 0:
                        direction = 1
                    x = (
                        prominence.x
                        + pyxel.cos((prominence.radian + i * 4) * direction)
                        * prominence.speed_x
                    )
                    y = (
                        prominence.y
                        + pyxel.sin((prominence.radian + i * 4) * direction)
                        * prominence.speed_y
                    )
                    r = 10 + pyxel.rndi(-1, 2) - c - i * 0.2
                    color = 8 + c
                    radian = prominence.radian
                    pyxel.circ(x, y, r, color)

                    # 衝突範囲設定
                    if i % 3 == 0 and c == 0:
                        collision_box = [
                            x - r * 0.75,
                            y - r * 0.75,
                            x + r * 1.25,
                            y + r * 1.25,
                        ]
                        self.collision_boxes.append(collision_box)

                    # パーティクル設定
                    if (
                        (radian < 0 and radian > -20)
                        or (radian < -160 and radian > -180)
                    ) and i == 0:
                        for n in range(3):
                            particle = Particle(
                                x + pyxel.rndi(-10, 10),
                                y,
                                pyxel.rndi(0, 60),
                                pyxel.rndf(0.1, 0.3),
                                pyxel.rndf(-0.4, 0.4),
                                direction,
                            )
                            self.particles.append(particle)

            if prominence.radian < -300:
                prominence.remove = True

        for particle in self.particles:
            if particle.delay <= 0:
                particle.x += particle.move_x
                pyxel.circ(particle.x, particle.y, pyxel.rndf(0.5, 2), pyxel.rndi(9, 10))

        # 衝突範囲表示
        # for box in self.collision_boxes:
        #     x1, y1, x2, y2 = box
        #     pyxel.rectb(x1, y1, x2 - x1, y2 - y1, 0)

    def get_collision_boxes(self):
        return self.collision_boxes
