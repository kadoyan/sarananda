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

        # 基本スコア(進んだ距離 ÷ ステージ全体の距離) × (進んだ距離 ÷ クリア時間)
        progress = min(position / distance, 1)
        distance_score = int(progress * (position / time) * distance)
        # クリアボーナス
        comp_bonus = 30000 if progress >= 1 else 0
        # シールド残量スコア
        shield_score = shield * 300
        # シールド最大ボーナス
        fullshield_score = 0
        if shield >= max_shield:
            fullshield_score = 10000
        # 取得エナジーボーナス
        energy_score = energy * 500
        # ノーダメージボーナス
        nodamage_score = 0
        if damage <= 0:
            nodamage_score = 50000
        # ダメージペナルティ
        damage_penalty = damage * -100
        
        return {
            "distance_score": distance_score,
            "comp_bonus": comp_bonus,
            "damege_penalty": damage_penalty,
            "shield_score": shield_score,
            "fullshield_score": fullshield_score,
            "energy_score": energy_score,
            "nodamage_score": nodamage_score
        }
