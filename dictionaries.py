# """key: [スキル名,スキルテキスト,ターゲット類(0=未分類、1=自分,2=味方単体,3=味方全体,4=敵単体,5=敵全体)
#   ,コスト(1~5),攻撃倍率(1.0 ~ 3.0),スキルレベル(1),ATKの影響(0.00 ~ 1.00),SPDの影響(0.00 ~ 1.00),テキスト]
#          ATKの影響とSPDの影響は合計して1.00になるようにする。"""

arts_dict_list = [
    {"no": 0, "name": "------", "target_type": "-------", "cost": 0, "atk_type": "none", "damage_rate": 0,
     "skill_level": 0, "atk_impact": 0, "spd_impact": 0, "arts_text": "------"},
    {"no": 1, "name": "殴る", "target_type": "enemy", "cost": 1, "atk_type": "none", "damage_rate": 1, "skill_level": 1,
     "atk_impact": 0.5, "spd_impact": 0.5, "arts_text": "自分も痛いが、反動ダメージはない。","test":100},
    {"no": 2, "name": "蹴る", "target_type": "enemy", "cost": 1, "atk_type": "none", "damage_rate": 1, "skill_level": 1,
     "atk_impact": 0.5, "spd_impact": 0.5, "arts_text": "(未実装)","test":50},
    {"no": 3, "name": "ずつく", "target_type": "enemy", "cost": 1, "atk_type": "none", "damage_rate": 1, "skill_level": 1,
     "atk_impact": 0.5, "spd_impact": 0.5, "arts_text": "(未実装)","test":75},
]


# "4": ["もやす", 5, 2, 225, 13, 6, "", ],"5": ["思念波", 4, 2, 225, 13, 6, "", ],


def weapon_dict_access(weapon_no: int):
    """key: [アイテム名,攻撃力,テキスト]
           """
    weapon_dict = {

        "1": ["木製サック", 2, "自家製。"],
        "2": ["量産サック", 4, "店頭に並んでいたサック。"],
        "3": ["100均のナイフ", 5, "切れ味は悪い。"],

    }
    return weapon_dict[str(weapon_no)]


def armor_dict_access(armor_no: int):
    """key: [アイテム名,防御力,テキスト]
               """

    armor_dict = {

        "1": ["少年誌", 2, "もう読むことはない。"],
        "2": ["辞典", 4, "読まない。"],

    }

    return armor_dict[str(armor_no)]


def character_dict_access(chara_no: int):
    """ key: [名前,HP(50~250),ATK(0~20),SPD(0~20)]"""

    chara_dict = {
        "1": ["アリ", 150, 15, 3, ],
        "2": ["イカ", 100, 5, 18],
        "3": ["ウマ", 225, 13, 6],
        "4": ["エビ", 85, 17, 4],
        "6": ["カイ", 225, 13, 6]
    }

    return chara_dict[str(chara_no)]
