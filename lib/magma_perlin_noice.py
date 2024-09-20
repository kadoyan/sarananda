import pyxel

class Magma:
    def __init__(self, y_top:int, y_bottom:int, height:int, scene_manager):
        self.scene_manager = scene_manager
        self.y_top = y_top
        self.y_bottom = y_bottom
        self.height = height
        self.local_acceleration = 0
        self.offscreen = []
        for i in range(3):
            self.offscreen.append(pyxel.Image(pyxel.width, self.height))
        
    def update(self):
        self.local_acceleration += (1 + self.scene_manager.acceleration) * 0.5
    
    def draw(self):
        for index, screen in enumerate(self.offscreen):
            self.__waving(screen, (index + 1) * 2, self.local_acceleration, index + 8)
            pyxel.blt(0, self.y_top, screen, 0, 0, screen.width, self.height * -1, 0)
            pyxel.blt(0, self.y_bottom, screen, 0, 0, screen.width, self.height, 0)
   
    def __shift_list(self, lst, shift, fill_value=0):
        if shift > 0:
            # Right
            return [fill_value] * shift + lst[:-shift]
        elif shift < 0:
            # Left
            return lst[-shift:] + [fill_value] * (-shift)
        else:
            # none
            return lst
    
    def __waving(self, image, shift, acceleration, c):
        image.cls(0)
        image.rect(0, shift, image.width, image.height - shift, c)
        ptr = image.data_ptr()
        for x in range(image.width):
            collection = []
            for y in range(image.height):
                point = y * image.width + x
                color = ptr[point]
                collection.append(color)
            shift_volume = int(pyxel.sin(pyxel.noise((x + acceleration * c * 0.1) / 30, pyxel.frame_count / 30)) * 250)
            shifted_list = self.__shift_list(collection, shift_volume, 0)
            for y in range(image.height):
                point = y * image.width + x
                ptr[point] = shifted_list[y]
