import random

from Character import Character as c
class Gatya:
    CHARA_ID_COUNT = 10
    RARE1_LIST = []
    RARE2_LIST = []
    RARE3_LIST = []
    RARE4_LIST = []
    RARE5_LIST = []
    for i in range(CHARA_ID_COUNT):
        chara = c.Character(i+1)
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

    GATYA_LIST = [
        {'list':RARE5_LIST,'rate':0.05},
        {'list':RARE4_LIST,'rate':0.18},
        {'list':RARE3_LIST,'rate':0.3},
        {'list':RARE2_LIST,'rate':0.6},
        {'list':RARE1_LIST,'rate':1.0},
    ]
    def gatya_generate(self):

        rand = random.random()
        for chara in self.GATYA_LIST:
            if rand < chara["rate"]:
                random.shuffle(chara["list"])

        return chara["list"][0]

    def run_gatya_10(self):
        MAX_GATYA = 10
        result = []
        for _ in range(MAX_GATYA):
            result.append(self.gatya_generate())
        return result
