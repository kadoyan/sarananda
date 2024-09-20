import pyxel
from dataclasses import dataclass

@dataclass
class Explosion:
    x: int
    y: int
    colors: list
    increase: float
    max_step: int
    step = 0
    
    def update(self, list):
        self.step += self.increase
        if self.step > self.max_step:
            list.remove(self)
    
    def draw(self, parent_x, parent_y):
        for c in range(len(self.colors)):
            pyxel.circ(self.x + parent_x, self.y + parent_y, max(3, self.step), self.colors[0])
            pyxel.circ(self.x + parent_x, self.y + parent_y, max(2, self.step - 2), self.colors[1])
            pyxel.circ(self.x + parent_x, self.y + parent_y, max(1, self.step - 3), self.colors[2])
