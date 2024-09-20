import pyxel
from collections import deque

class TileShift:

    def update(bank, speed_h, width, height, u, v, timing):
        """
        Shift an image cell on an image bank

        Args:
            bank (int): The number of the image bank
            speed_h (int): Scrolling direction
            width (int): tile width(px)
            height (int): tile height(px)
            u (int): X position of the target image on the image bank
            v (int): Y position of the target image on the image bank
            timing (int): Scroll timing (frame)
        """
        screen_ptr = pyxel.images[0].data_ptr()
        if timing == 0 :
            timing = 1
        if pyxel.frame_count % timing == 0:
            for y in range(0, height):
                cell = u + (v + y) * 256
                source = screen_ptr[cell:cell+width]
                shifted = deque(source)
                shifted.rotate(speed_h)
                screen_ptr[cell:cell+width] = shifted
