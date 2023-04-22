import math
from dictionaries import *


class Character:
    """キャラクター"""

    def __init__(self, characters_no: int):
        chara = characters_dict_list[characters_no]
        self.no = chara["no"]
        self.name = chara["name"]
        self.maxhp = chara["hp"]
        self.hp = self.maxhp
        self.atk = chara["atk"]
        self.pro = chara["pro"]
        self.spd = chara["spd"]

        self.art1 = MartialArt(-1)
        self.art2 = MartialArt(2)
        self.art3 = MartialArt(3)

        self.arts_list = [self.art1, self.art2, self.art3]

        self.weapon = Weapon(1)
        self.armor = Armor(2)

        self.is_hero = False

    def status(self):
        return f"『{self.name} 』　hp:{(math.floor(self.hp))} /  {math.floor(self.maxhp)}ATK:{self.atk}SPD: {self.spd}"

    def status_hp(self):
        return f"『{self.name}』　hp:{math.floor(self.hp)}/{math.floor(self.maxhp)}"

    # markup対応↓
    def name_txt(self):
        return f"[b][u]{self.name}[/u][/b]"

    def status_txt(self):
        return f"H P:　{self.hp}\nATK:　{self.atk}\nSPD:　{self.spd}\n"

    def status_full_txt(self):
        return f"H P:　{self.hp}　/　{self.maxhp}\nATK:　{self.atk}\nSPD:　{self.spd}\n"

    def status_up(self):
        self.maxhp = 999 if self.maxhp != 999 else None
        self.hp = self.maxhp


class MartialArt:
    arts = arts_dict_list

    def __init__(self, arts_no: int):
        # 技名
        art = self.arts[arts_no]

        self.no = art["no"]
        self.name = art["name"]
        self.target_type = art["target_type"]
        # 技コスト
        self.cost = art["cost"]
        self.attribute = art["attribute"]
        # 攻撃倍率（計算時に使用）
        self.damage_rate = art["damage_rate"]
        # スキルレベル（計算時に使用）
        self.skill_level = art["skill_level"]
        # ダメージ計算用(ATK参照)
        self.atk_impact = art["atk_impact"]
        # ダメージ計算用(SPD参照)
        self.spd_impact = art["spd_impact"]
        # テキスト
        self.text = art["text"]

    def normal_attack(self, target):
        dam = self.dam_atk
        target.hp -= dam
        return dam, self.arts_name

    def power_attack(self, target):
        dam = self.dam_atk
        dam *= 20
        target.hp -= dam
        return dam

    def speed_attack(self, target):
        dam = self.dam_atk + self.dam_spd
        target.hp -= dam
        return dam


class Weapon:
    weapons = weapons_dict_list

    def __init__(self, weapons_no: int):
        weapon = self.weapons[weapons_no]

        self.no = weapon["no"]
        self.name = weapon["name"]
        self.atk = weapon["atk"]
        self.text = weapon["text"]


class Armor:
    armors = armors_dict_list

    def __init__(self, armors_no: int):
        armor = self.armors[armors_no]

        self.no = armor["no"]
        self.name = armor["name"]
        self.pro = armor["pro"]
        self.text = armor["text"]


class Hero(Character):
    def __init__(self, characters_no: int):
        super().__init__(characters_no)
        self.is_hero = True
        self.select_art = None
        self.card_pos_x = ""
        self.card_pos_y = ""



class Enemy(Character):
    def __init__(self, characters_no: int):
        super().__init__(characters_no)
        self.is_pos = []
