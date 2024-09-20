import pyxel

class Pseudo3D:
    @staticmethod
    def convert( x: float, y: float, z: float, w:int, h:int):
        if z == 0:
            z = -1
        s = 1 / z
        x = x * s + w / 2
        y = y * s + h / 2
        
        return [x, y, s]
