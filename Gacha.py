import random

from Character import Character as c
class Gacha:
    CHARA_ID_COUNT = 10
    RARE1_LIST = []
    RARE2_LIST = []
    RARE3_LIST = []
    RARE4_LIST = []
    RARE5_LIST = []
    for i in range(CHARA_ID_COUNT):
        chara = c(i+1)
        if chara.RARE is 1:
            RARE1_LIST.append(chara)
        elif chara.RARE is 2:
            RARE2_LIST.append(chara)
        elif chara.RARE is 3:
            RARE3_LIST.append(chara)
        elif chara.RARE is 4:
            RARE4_LIST.append(chara)
        elif chara.RARE is 5:
            RARE5_LIST.append(chara)
    #レア度毎に排出レートを設定

    GATYA_LIST = [
       # {'list':RARE5_LIST,'rate':0.1},    #0.1  ~         1
        {'list':RARE4_LIST,'rate':0.25},    #0.25 ~         1.5
        {'list':RARE3_LIST,'rate':0.45},    #0.45 ~ 0.25+   2
        {'list':RARE2_LIST,'rate':0.7},     #0.7  ~ 0.4 +   2.5
        {'list':RARE1_LIST,'rate':1.0},     #1.0  ~ 0.7 +   3
    ]
    def __init__(self):
        pass
    def generate(self):
        """排出の実行"""
        rand = random.random()  #レア度レートを定義
        #print(f'{rand}')
        for gacha_c in self.GATYA_LIST:   #レートを元に排出するレアリティを決定
            if rand < gacha_c["rate"]:
                random.shuffle(gacha_c["list"])   #取得したリストの順番をシャッフル
                #print(f'{gacha_c["list"][0].name},{gacha_c["list"][0].RARE}')
                return gacha_c["list"][0] #シャッフルしたリストから1番目をreturn

    def run_continue_10(self):
        MAX_GATYA = 10
        result = []

        for _ in range(MAX_GATYA):
            result.append(self.generate())    #メソッドからreturnされたキャラをresultに挿入
        return result
    def double_checker(self):
        global PLAYER_INFO