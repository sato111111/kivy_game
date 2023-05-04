# """key: [スキル名,スキルテキスト,ターゲット類(0=未分類、1=自分,2=味方単体,3=味方全体,4=敵単体,5=敵全体)
#   ,コスト(1~5),攻撃属性,攻撃倍率(1.0 ~ 3.0),スキルレベル(1),ATKの影響(0.00 ~ 1.00),SPDの影響(0.00 ~ 1.00),テキスト]
#          ATKの影響とSPDの影響は合計して1.00になるようにする。"""

arts_dict_list = [
    {"no": 0, "name": "------", "target_type": "-------", "cost": 0, "attribute": "none", "damage_rate": 0,
     "skill_level": 0, "atk_impact": 0, "spd_impact": 0, "text": "------"},

    {"no": 1, "name": "殴る", "target_type": "VISITOR", "cost": 1, "attribute": "none", "damage_rate": 1, "skill_level": 1,
     "atk_impact": 0.5, "spd_impact": 0.5, "text": "自分も痛い。", },
    {"no": 2, "name": "蹴る", "target_type": "VISITOR", "cost": 1, "attribute": "none", "damage_rate": 1, "skill_level": 1,
     "atk_impact": 0.5, "spd_impact": 0.5, "text": "(未実装)", },
    {"no": 3, "name": "ずつく", "target_type": "VISITOR", "cost": 1, "attribute": "none", "damage_rate": 1, "skill_level": 1,
     "atk_impact": 0.5, "spd_impact": 0.5, "text": "(未実装)",},
    {"no": 99, "name": "テストアーツ", "target_type": "VISITOR", "cost": 0, "attribute": "none", "damage_rate": 1, "skill_level": 1,
     "atk_impact": 10, "spd_impact": 10, "text": "テスト用arts",},

]

# key: [アイテム名,攻撃力,テキスト]

weapons_dict_list = [
    {"no": 0, "name": "------", "atk": 0, "text": "------"},

    {"no": 1, "name": "サック", "atk": 2, "text": "(未実装)"},
    {"no": 2, "name": "木刀", "atk": 4, "text": "(未実装)", },
    {"no": 3, "name": "ナイフ", "atk": 5, "text": "(未実装)", },

    {"no": 99, "name": "テストウェポン", "atk": 5, "text": "テスト用武器", },

]
# key: [アイテム名,防御力,テキスト]
armors_dict_list = [
    {"no": 0, "name": "------", "pro": 0, "text": "------"},

    {"no": 1, "name": "Tシャツ", "pro": 2, "text": "(未実装)"},
    {"no": 2, "name": "Yシャツ", "pro": 4, "text": "(未実装)", },
    {"no": 99, "name": "テストアーマー", "pro": 4, "text": "テスト用防具", },
    # {"no": 3, "name": "ナイフ", "pro": 5, "text": "(未実装)", },

]
characters_dict_list = [
            #key: [名前,HP(50~250),ATK(0~20),SPD(0~20)]
    {"no": 0, "name": "------", "hp": 0, "atk": 0,"pro":0, "spd": 0, "text": "------"},

    {"no": 1, "name": "アリ", "hp": 55, "atk": 15, "pro":1,"spd": 3, "text": "蟻"},
    {"no": 2, "name": "イカ", "hp": 80, "atk": 5,"pro":1, "spd": 8, "text": "烏賊"},
    {"no": 3, "name": "ウマ", "hp": 105, "atk": 11, "pro":2,"spd": 10, "text": "馬"},
    {"no": 4, "name": "エビ", "hp": 85, "atk": 9, "pro":3,"spd": 9, "text": "海老"},
    {"no": 5, "name": "オニ", "hp": 45, "atk": 15, "pro":4,"spd": 1, "text": "鬼"},
    {"no": 6, "name": "カイ", "hp": 80, "atk": 8, "pro":7,"spd": 9, "text": "貝"},
    {"no": 7, "name": "キジ", "hp": 70, "atk": 10,"pro":1, "spd": 14, "text": "雉"},
    {"no": 8, "name": "クジラ", "hp": 140, "atk": 8,"pro":10, "spd": 2, "text": "鯨"},
    {"no": 9, "name": "ケムシ", "hp": 50, "atk": 12, "pro":1,"spd": 2, "text": "毛虫"},
    {"no": 10, "name": "コオロギ", "hp": 70, "atk": 4,"pro":0, "spd":7, "text": "蟋蟀"},

    {"no": 99, "name": "テストキャラ", "hp": 250, "atk": 20, "pro":20,"spd": 20, "text": "テスト用キャラ"},

]


