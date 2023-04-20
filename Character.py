import math
import dictionaries as di
from MartialArts import MartialArts


class Character:
    """キャラクター"""
    arts = di.arts_dict_list
    weapons = di.weapon_dict_list
    armors = di.armor_dict_list
    characters = di.character_dict_list

    def __init__(self, chara_no: int, is_hero=0):
        chara = self.characters[chara_no]

        self.name = chara["name"]
        self.maxhp = chara["hp"]
        self.hp = self.maxhp
        self.atk = chara["atk"]
        self.spd = chara["spd"]

        self.arts = [self.arts[-1], self.arts[2], self.arts[3]]
        self.weapon = self.weapons[1]
        self.armor = self.armors[2]
        self.is_hero = is_hero  # 0=Enemy,1 =Hero

    def status(self):
        return "『" + str(self.name) + "』　hp:" + str(math.floor(self.hp)) + "/" + str(
            math.floor(self.maxhp)) + "　ATK:" + str(self.atk) + "　SPD:" + str(self.spd)

    def status_hp(self):
        return "『" + str(self.name) + "』　hp:" + str(math.floor(self.hp)) + "/" + str(
            math.floor(self.maxhp))

    # markup対応↓
    def name_txt(self):
        return "[b][u]" + self.name + "[/u][/b]"

    def status_txt(self):
        return "H P:　" + str(self.hp) + "\nATK:　" + str(self.atk) + "\nSPD:　" + str(self.spd) + "\n"

    def status_full_txt(self):
        return "H P:　" + str(self.hp) + "　/　" + str(self.maxhp) + "\nATK:　" + str(
            self.atk) + "\nSPD:　" + str(self.spd) + "\n"

    def status_up(self):
        self.maxhp = 999 if self.maxhp != 999 else None
        self.hp = self.maxhp
