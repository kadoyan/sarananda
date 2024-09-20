class ScoreCalc:
    @staticmethod
    def score(scene_manager):
        distance = scene_manager.distance # ステージ距離
        position = scene_manager.position # プレイヤー位置
        time = scene_manager.play_time # プレイ時間
        shield = scene_manager.shield # シールド残量
        max_shield = scene_manager.max_shield # シールド最大値
        damage = scene_manager.damages # ダメージ回数
        energy = scene_manager.energies # 取得アイテム
        
        base_time = distance * 1.5 #標準クリアタイム

        # タイムスコア
        distance_score = int((position / distance) * (base_time / time)) * 1000 - damage * 10
        print((position / distance) * (base_time / time), damage)
        # シールド残量スコア
        shield_score = shield * 10
        # シールド最大ボーナス
        fullshield_score = 0
        if shield >= max_shield:
            fullshield_score = 5000
        # 取得エナジーボーナス
        energy_score = energy * 100
        # ノーダメージボーナス
        nodamage_score = 0
        if damage <= 0:
            nodamage_score = 50000
        
        return {
            "distance_score": distance_score,
            "shield_score": shield_score,
            "fullshield_score": fullshield_score,
            "energy_score": energy_score,
            "nodamage_score": nodamage_score,
        }
