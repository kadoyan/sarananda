import pyxel

class Sparks:
    def __init__(self, scene_manager, num:int):
        self.scene_manager = scene_manager
        self.sparks = [[
            pyxel.rndf(0, pyxel.width), # X
            pyxel.rndf(20, 160), # Y
            pyxel.rndf(0.5, 3) # Speed
            ] for i in range(num)]
        
    def update(self):
        for spark in self.sparks:
            spark[0] -= spark[2] + (self.scene_manager.acceleration * .5) ** 2
            if spark[0] < 0:
                spark[0] = pyxel.width
    
    def draw(self):
        for spark in self.sparks:
            pyxel.pset(spark[0], pyxel.sin(spark[0]) + spark[1], 9)
