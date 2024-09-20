import pyxel
from .convert_timeformat import ConvertTimeFormat

LIFE_W = 16
LIFE_H = 8


class Status:
    @classmethod
    def draw(cls, scene_manager):
        """
        ステータス表示
        """
        pyxel.rect(0, pyxel.height - scene_manager.status_height, pyxel.width, pyxel.height, 0)
        life_y = pyxel.height - scene_manager.status_height + 4
        colors = [12, 9, 8]

        # Shield
        pyxel.text(4, life_y + 1, "SHIELD", 12)
        for m in range(scene_manager.max_shield):
            pyxel.blt(28 + m * (LIFE_W - 3), life_y, 0, 32, 56, LIFE_W, LIFE_H, 0)
        for l in range(scene_manager.shield):
            pyxel.blt(28 + l * (LIFE_W - 3), life_y, 0, 32, 48, LIFE_W, LIFE_H, 0)
        
        # Timer
        # time_difference = pyxel.frame_count - start_frame
        pyxel.text(pyxel.width - 60, life_y, f"TIME {str(ConvertTimeFormat.convert_to_minutes_seconds_milliseconds(scene_manager.play_time))}", 7)

        # Distance
        distance_length = pyxel.width - 70
        pyxel.text(4, life_y + 10, "DISTANCE", 12)
        pyxel.line(38, life_y + 14, distance_length, life_y + 14, 12)
        scale = distance_length - 38
        # wallPosition = (scene_manager.wall_position / scene_manager.distance) * scale
        # pyxel.rect(38, life_y + 11, wallPosition, 3, 9)
        myPosition = scene_manager.position / scene_manager.distance * scale
        pyxel.circ(myPosition + 38, life_y + 12, 1, 7)
        
        # Speed
        max_speed = 4 * ((pyxel.width - 16) / pyxel.width)
        max_speed_width = 34
        speed_width = (scene_manager.acceleration/ max_speed) * max_speed_width
        pyxel.text(pyxel.width - 60, life_y + 10, "SPEED", 7)
        pyxel.rect(pyxel.width - 40, life_y + 10, max_speed_width + 2, 5, 5)
        pyxel.rect(pyxel.width - 39, life_y + 11, max_speed_width, 3, 1)
        pyxel.rect(pyxel.width - 39, life_y + 11, speed_width, 3, colors[int(scene_manager.acceleration) - 1])
