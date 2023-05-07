import math
from Database import Database


class Character:
    """キャラクター"""
    sqlite = Database()
    characters = sqlite.characters_dict_list_generate()

    def __init__(self, characters_no: int):
        self.IS_TYPE = None
        character = self.characters[characters_no]
        self.no = character["id"]
        self.name = character["name"]
        self.maxhp = character["hp"]
        self.hp = self.maxhp
        self.atk = character["atk"]
        self.pro = character["pro"]
        self.spd = character["spd"]

        self.art1 = MartialArt(-1)
        self.art2 = MartialArt(2)
        self.art3 = MartialArt(3)

        self.arts_list = [self.art1, self.art2, self.art3]

        self.weapon = Weapon(1)
        self.armor = Armor(2)

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
    sqlite = Database()
    arts = sqlite.arts_dict_list_generate()

    def __init__(self, arts_no: int):
        # 技名
        art = self.arts[arts_no]

        self.no = art["id"]
        self.name = art["name"]
        self.target_type = art["target_type"]
        # 技コスト
        self.cost = art["cost"]
        self.attribute = art["attribute"]
        # 攻撃倍率（計算時に使用）
        self.damage_rate = art["damage_rate"]
        # スキルレベル（計算時に使用）
        self.skill_level = art["level"]
        # ダメージ計算用(ATK参照)
        self.atk_impact = art["atk_impact"]
        # ダメージ計算用(SPD参照)
        self.spd_impact = art["spd_impact"]
        # テキスト
        self.text = art["text"]

    def normal_attack(self):
        damage = (self.damage_rate * (self.atk_impact + self.spd_impact)) * 10
        return damage

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
    sqlite = Database()
    weapons = sqlite.weapons_dict_list_generate()

    def __init__(self, weapons_no: int):
        weapon = self.weapons[weapons_no]

        self.no = weapon["id"]
        self.name = weapon["name"]
        self.atk = weapon["atk"]
        self.text = weapon["text"]


class Armor:
    sqlite = Database()
    armors = sqlite.armors_dict_list_generate()

    def __init__(self, armors_no: int):
        armor = self.armors[armors_no]

        self.no = armor["id"]
        self.name = armor["name"]
        self.pro = armor["pro"]
        self.text = armor["text"]


class Hero(Character):

    def __init__(self, characters_no: int):
        super().__init__(characters_no)
        self.IS_TYPE = "HERO"
    def save_current_state(self):
        self.current_atk = self.atk
        self.current_pro = self.pro
        self.current_spd = self.spd

    def load_current_state(self):
        self.hp = self.maxhp
        self.atk = self.current_atk
        self.pro = self.current_pro
        self.spd = self.current_spd

class Enemy(Character):

    def __init__(self, characters_no: int):
        super().__init__(characters_no)
        self.IS_TYPE = "ENEMY"

class Empty:
    def __init__(self):
        self.IS_TYPE = "EMPTY"
