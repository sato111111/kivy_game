from operator import attrgetter
# 以下テスト用
import random
from Character import Character as Ch

from MartialArts import MartialArts as MA

turn = 0


class Battle:
    def __init__(self, player_party, enemy_party):
        self.h_p = player_party
        self.e_p = enemy_party
        self.win = "戦闘に勝利した"
        self.lose = "戦闘に敗北した"

    def battle_turn(self):
        """ターン数"""
        global turn
        turn += 1
        turn_str = str(turn) + "ターン目  :　"

    def battle_move_select(self):
        """行動選択"""
        h_target = 0
        for i in self.h_p:
            self.move_select(i)

        # 実行動

        e_target = 0

        self.dam = self.h_p[h_target].artsA.power_attack(self.e_p[e_target])

        dam_str = str(self.dam) + "ダメージ与えた"

        self.dam = self.e_p[e_target].artsA.power_attack(self.h_p[h_target])

        # 体力チェック
        hpc_txt = self.delete_check()
        # 勝敗チェック

        if hpc_txt is not None:
            dam_str = dam_str + hpc_txt
            # 例 10ダメージ与えた enemyを倒した

        battle_result = self.party_check()

        if battle_result is not None:
            dam_str = dam_str + battle_result
            turn = 0

        # under_txt = turn_str + dam_str
        under_txt = dam_str

        return under_txt, self.h_p, self.e_p

        # 戦闘可能なものがいれば戦闘続行
        # 敵全滅の場合　勝利

    def party_check(self):
        if 0 >= len(self.e_p):
            return self.win

        # 味方全滅の場合　敗北
        elif 0 >= len(self.h_p):
            return self.lose

        else:
            pass

    def delete_check(self):
        # 検証につき0固定
        h_target = 0
        e_target = 0
        message = None
        h = self.h_p[h_target]
        e = self.e_p[e_target]

        if e.hp <= 0:
            message = e.name + "を倒した"
            self.e_p.pop(e_target)



        elif h.hp <= 0:
            message = h.name + "はやられた"
            self.h_p.pop(h_target)

        else:
            pass

        return message

    def move_select(self, chara):
        chara.arts


class BattleTest:
    def __init__(self, characters=None):
        self.next_turn_list = []
        self.down_list = []
        self.characters = []

    def spd_sort(self, party_list):
        sorted_list = sorted(party_list, reverse=True, key=attrgetter("spd"))

        return sorted_list

    def battle_test(self):
        for chara in self.characters:
            chara.hp -= 200
        down_list = []
        next_turn_list = []

        [next_turn_list.append(f.name) if f.hp > 0 else down_list.append(f) for f in self.characters]
        print(next_turn_list)

        print([f.name +"//"+ str(f.hp) +"//"+str(f.spd) for f in self.spd_sort(down_list)])

    def test_attack(self):
        turn = "a"


btst = BattleTest()

[btst.characters.append(Ch(random.randrange(1, 10))) for _ in range(6)]

btst.battle_test()
