import pyxel
from dataclasses import dataclass

@dataclass
class Triangle:
    x1: float
    y1: float
    x2: float
    y2: float
    x3: float
    y3: float

class Triangles:
    @classmethod
    def draw(cls, inner_r:int, outer_r:int, num:int, center_x:float, center_y:float, color:int):
        """
		集中線を描きます。
		inner_r: 内側の半径px
		outer_r: 外側の半径px
		num: 線の数
		center_x,center_y: 中心の座標px
		color: 色
		"""
        items = []
        
        base_radian = pyxel.rndi(0, 360)
        sub_radian = 360 / num 
        for i in range(num):
            base_radian += sub_radian
            triangle = Triangle(
                pyxel.cos(base_radian) * inner_r + center_x,
                pyxel.sin(base_radian) * inner_r + center_y,
                pyxel.cos(base_radian - 0.5) * outer_r + center_x,
                pyxel.sin(base_radian - 0.5) * outer_r + center_y,
                pyxel.cos(base_radian + 0.5) * outer_r + center_x,
                pyxel.sin(base_radian + 0.5) * outer_r + center_y,
            )
            items.append((triangle))
            
        for item in items:
            pyxel.tri(item.x1, item.y1, item.x2, item.y2, item.x3, item.y3, color)
