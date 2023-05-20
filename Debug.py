import random

class Debug:
    def enemies_generate(self,En):
        en = []
        for _ in range(random.randrange(2, 4)):
            en.append(En(random.randrange(1, 10)))
        return en


    def test_info(self,):
        name = "プレイヤーネーム"
        return name
    def test_enemy(self,enemy_card):
        enemy_card.select_art = enemy_card.arts_list[1]
        pass

    def gacha_test(self,gacha_list):

        return [c.name for c in gacha_list]
