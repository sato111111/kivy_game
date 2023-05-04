import random


def enemies_generate(En):
    en = []
    for _ in range(random.randrange(2, 4)):
        en.append(En(random.randrange(1, 10)))
    return en


def test_info():
    name = "プレイヤーネーム"
    return name
def test_enemy(enemy_card):
    enemy_card.select_art = enemy_card.arts_list[1]
    pass