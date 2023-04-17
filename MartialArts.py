class MartialArts:

    def __init__(self,arts):
        # 技名

        self.arts_name = arts[0]
        # 技コスト
        self.cost = arts[1]
        # 攻撃倍率（計算時に使用）
        self.dam_math = arts[2]
        # スキルレベル（計算時に使用）
        self.arts_sklv = arts[3]
        # ダメージ計算用(ATK参照)
        self.dam_atk = arts[4]
        # ダメージ計算用(SPD参照)
        self.dam_spd = arts[5]
        # テキスト
        self.arts_txt = arts[6]

    def normal_attack(self, target):
        dam = self.dam_atk
        target.hp -= dam
        return dam,self.arts_name

    def power_attack(self,  target):
        dam = self.dam_atk
        dam *= 20
        target.hp -= dam
        return dam

    def speed_attack(self,target):
        dam = self.dam_atk + self.dam_spd
        target.hp -= dam
        return dam
