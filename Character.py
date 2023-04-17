import math
import dictionaries as di
from MartialArts import MartialArts


class Character:
    """キャラクター"""

    def __init__(self, chara_no,is_hero = 0):
        arts = di.arts_dict_list
        weapon = di.weapon_dict_access
        armor = di.armor_dict_access
        chara_status = di.character_dict_access(str(chara_no))

        self.name = chara_status[0]
        self.maxhp = chara_status[1]
        self.hp = self.maxhp
        self.atk = chara_status[2]
        self.spd = chara_status[3]
        self.arts = [arts[1], arts[2],arts[3]]
        # 「下記要検証」何がしたかったのか、失念
        self.artsA = map(lambda i: MartialArts(i), self.arts)
        self.equ = weapon(1), armor(2)
        # self.image = chara_status[10]
        self.is_hero = is_hero #0=Enemy,1 =Hero
        self.status = lambda: "『" + str(self.name) + "』　hp:" + str(math.floor(self.hp)) + "/" + str(
            math.floor(self.maxhp)) + "　ATK:" + str(self.atk) + "　SPD:" + str(self.spd)
        self.status_hp = lambda: "『" + str(self.name) + "』　hp:" + str(math.floor(self.hp)) + "/" + str(
            math.floor(self.maxhp))
        # 　↓　markup対応
        self.name_txt = lambda: "[b][u]" + self.name + "[/u][/b]"
        self.status_txt = lambda : "H P:　" + str(self.hp) + "\nATK:　" + str(self.atk) + "\nSPD:　" + str(self.spd) + "\n"
        self.status_full_txt = lambda: "H P:　" + str(self.hp) + "　/　" + str(self.maxhp) + "\nATK:　" + str(
            self.atk) + "\nSPD:　" + str(self.spd) + "\n"

    def status_up(self):
        if self.maxhp < 999:
            self.maxhp = self.maxhp + 1000

            if self.maxhp >= 999:
                self.maxhp = 999

        self.hp = self.maxhp
