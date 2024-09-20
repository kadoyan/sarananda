class Collision:
    
    @staticmethod
    def is_collision(object_a:list, object_b:list):
        """
        長方形 object_a と object_b が重なっているかどうかと、衝突の方向を判定します。
        各オブジェクトは (x1, y1, x2, y2) の形式で指定します。

        :param object_a: (x1, y1, x2, y2) の形式の長方形
        :param object_b: (x1, y1, x2, y2) の形式の長方形
        :return: 衝突しているかどうか (bool)、衝突方向 (上, 下, 左, 右のうち該当する方向をリストで返します)
        """
        x1_1, y1_1, x2_1, y2_1 = object_a
        x1_2, y1_2, x2_2, y2_2 = object_b

        # 衝突しているかどうかを判定
        collision = not (x2_1 < x1_2 or x1_1 > x2_2 or y2_1 < y1_2 or y1_1 > y2_2)
        
        directions = []

        if collision:
            # 衝突している場合、方向を判定する
            # 上からの衝突
            if y2_1 > y1_2 and y1_1 < y1_2:
                directions.append("Top")
            # 下からの衝突
            if y1_1 < y2_2 and y2_1 > y2_2:
                directions.append("Bottom")
            # 左からの衝突
            if x2_1 > x1_2 and x1_1 < x1_2:
                directions.append("Left")
            # 右からの衝突
            if x1_1 < x2_2 and x2_1 > x2_2:
                directions.append("Right")

        return collision, directions
