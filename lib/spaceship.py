import pyxel
from .explosion import Explosion

class Energy:
    gravity = 0.03
    maxDy = 4

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dy = dy
        self.dx = dx
        self.collision_box = None

    def update(self, myList):
        self.dy += self.gravity
        self.y += min(self.dy, self.maxDy)
        self.x += self.dx
        self.collision_box = [self.x + 2, self.y + 2, self.x + 14, self.y + 14]

        if self.y > 200:
            myList.remove(self)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 48, 80, 16, 16, 0)

HORIZON = 100

class SpaceShip:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.explosion = []
        self.magma = []
        # self.ship = Rotation(0, 0, 64, 48, 80, 24, 40, 3)
        self.angle = pyxel.rndf(0, -10)
        self.x = pyxel.width
        self.y = HORIZON
        self.delete = False
        pyxel.play(3, 5, resume=True)
        self.energies = []
        self.energy_stock = 3

    def update(self, myList):
        flowup = (-2.75, -2.5, -2.5)
        if self.x < 180 and self.x > 150 and self.energy_stock > 0:
            # energy = Energy(self.x + 30, 170, -1 + len(self.energies) * .5, -2.5)
            energy = Energy(self.x + 30, 170, -1 + len(self.energies) * .5, flowup[len(self.energies) - 1])
            self.energies.append(energy)
            self.energy_stock -= 1

        for energy in self.energies:
            energy.update(self.energies)

        self.x -= self.scene_manager.acceleration  / 2
        self.y += 0.2
        self.angle -= 0.2
        
        if self.x > 40 or self.y < 160:

            if len(self.explosion) < 5:
                self.explosion.append(
                    Explosion(
                        pyxel.rndi(20, 60),
                        pyxel.rndi(10, 30),
                        [13, 12, 7],
                        1,
                        12
                    )
                )
            if len(self.magma) < 30:
                self.magma.append(
                    Explosion(
                        pyxel.rndi(0, 60),
                        pyxel.rndi(45, 50),
                        [9, 10, 10],
                        0.5,
                        8
                    )
                )
        if self.x < 0 and len(self.energies)<=0:
            self.delete = True

        for exp in self.explosion:
            exp.update(self.explosion)
                
        for magma in self.magma:
            magma.update(self.magma)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 64, 48, 80, 3, self.angle)
        for exp in self.explosion:
            exp.draw(self.x, self.y)
        
        for magma in self.magma:
            magma.draw(self.x, self.y)
            
        for energy in self.energies:
            energy.draw()

    def get_status(self):
        return self.delete
    
    def get_energies(self):
        energies = []
        for energy in self.energies:
            energies.append(energy)
        return energies
    
    def delete_energy(self, energy):
        self.energies.remove(energy)
