import pyxel

class SceneManager:
    def __init__(self):
        self.jafont = pyxel.Font("./assets/misaki_gothic_2nd.bdf")
        self._scene: int = 4  # シーン番号を管理
        self.status_height = 24 # ステータス表示の高さ
        self.distance = 60 * 200 # マップの長さ
        self.max_shield: int = 12 # シールドの最大値
        self.reset()
        self.observers = [] # オブザーバーを保持するリスト
        
    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, value):
        self._scene = value
        # print(f"Sceneが {value} に変更されました")
        self.notify_observers() # シーンが変更されたらオブザーバーに通知

    def add_observer(self, observer):
        """オブザーバーを追加"""
        self.observers.append(observer)

    def notify_observers(self):
        """すべてのオブザーバーに通知"""
        for observer in self.observers:
            observer.on_scene_change(self._scene)

    def reset(self):
        # 全体に関わる変数
        self.play_time: int = 0  # プレイ時間
        self.damages: int = 0  # ダメージ回数
        self.energies: int = 0  # 取得したエナジー数
        self.shield:int = self.max_shield # 現在のシールド
        self.acceleration: float = 0  # 現在の加速度
        self.position = 0 # プレイヤーの経過位置
        self.wall_position = 0 # 後ろ壁の位置
        
        pyxel.pal()
