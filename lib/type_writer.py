import pyxel

class TypeWriter:
    def __init__(
        self,
        x: int,
        y: int,
        scene_manager,
        message,
        sfx,
        speed: int = 5,
    ) -> None:
        self.x = x  # 表示座標x
        self.y = y  # 表示座標y
        self.speed = speed  # 表示スピード
        self.current_text = [""]  # 表示中のテキスト
        self.char_index = 0  # 何文字目
        self.frame_count = 0  # カウンター
        self.done = False  # 表示完了フラグ
        self.line = 0  # 表示中の行
        self.max_letters = 26  # 一行の最大文字数
        self.scene_manager = scene_manager  # シーンマネージャー
        self.messages = message
        self.message_index = 0
        self.sfx = sfx  # 効果音
        self.max_index = len(self.messages) - 1
        self.finished = False
        self.color = None  # 表示色

    def update(self, text: str) -> bool:
        self.text = self.messages[self.message_index][0]  # テキスト
        self.color = self.messages[self.message_index][1]  # 色
        if not self.finished:
            if not self.done and self.char_index < len(self.text):
                if self.frame_count % self.speed == 0:
                    pyxel.play(3, self.sfx, resume=True)
                    self.current_text[self.line] += self.text[self.char_index]
                    self.char_index += 1
                    if self.char_index % self.max_letters == 0:
                        self.line += 1
                        self.current_text.append("")
                self.frame_count += 1
            elif self.char_index >= len(self.text):
                self.done = True

            if (
                pyxel.btnp(pyxel.KEY_Z)
                or pyxel.btnp(pyxel.KEY_SPACE)
                or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
            ):
                if not self.done:
                    all_text = [
                        self.text[i : i + self.max_letters]
                        for i in range(0, len(self.text), self.max_letters)
                    ]
                    self.current_text = all_text
                    self.line = len(all_text)
                    self.done = True
                else:
                    self.current_text.clear()  # 表示中のテキストクリア
                    self.current_text.append("")
                    self.char_index = 0  # 何文字目
                    self.frame_count = 0  # カウンター
                    self.done = False  # 表示完了フラグ
                    self.line = 0  # 表示中の行
                    if self.max_index > self.message_index:
                        self.message_index += 1  # 次のメッセージへ
                    else:
                        self.finished = True
                
        return self.finished

    def draw(self):
        for line, text in enumerate(self.current_text):
            pyxel.text(
                self.x, self.y + line * 12, text, self.color, self.scene_manager.jafont
            )

        if self.done and pyxel.frame_count % 60 > 20 and not self.finished:
            pyxel.text(
                self.x + (self.max_letters - 1) * 8,
                self.y + 36,
                "▼",
                self.color,
                self.scene_manager.jafont,
            )
