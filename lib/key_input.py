import pyxel

class KeyInput:

    UP = [
        pyxel.KEY_UP,
        pyxel.GAMEPAD1_BUTTON_DPAD_UP,
        pyxel.KEY_W,
    ]

    DOWN = [
        pyxel.KEY_DOWN,
        pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,
        pyxel.KEY_S,
    ]

    LEFT = [
        pyxel.KEY_LEFT,
        pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,
        pyxel.KEY_A,
    ]

    RIGHT = [
        pyxel.KEY_RIGHT,
        pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,
        pyxel.KEY_D,
    ]

    ZBUTTON = [
        pyxel.KEY_Z,
        pyxel.KEY_SPACE,
        pyxel.GAMEPAD1_BUTTON_A,
    ]

    XBUTTON = [
        pyxel.KEY_X,
        pyxel.KEY_ALT,
        pyxel.GAMEPAD1_BUTTON_B,
    ]

    def is_pressed(keys: list[int]) -> bool:
        for k in keys:
            if pyxel.btn(k):
                return True
        return False

    def is_released(keys: list[int]) -> bool:
        for k in keys:
            if pyxel.btnr(k):
                return True
        return False
