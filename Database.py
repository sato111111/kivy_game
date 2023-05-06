import sqlite3

class Database:
    def __init__(self):
        self.dbname = 'db/characters.db'

    def characters_dict_list_generate(self, ):
        # """key: [スキル名,スキルテキスト,ターゲット類(0=未分類、1=自分,2=味方単体,3=味方全体,4=敵単体,5=敵全体)
        #   ,コスト(1~5),攻撃属性,攻撃倍率(1.0 ~ 3.0),スキルレベル(1),ATKの影響(0.00 ~ 1.00),SPDの影響(0.00 ~ 1.00),テキスト]
        #          ATKの影響とSPDの影響は合計して1.00になるようにする。"""
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute('SELECT * FROM character')
        __list__ = []
        for row in cur:
            dic = {
                "id": row[0],
                "name": row[1],
                "hp": row[2],
                "atk": row[3],
                "pro": row[4],
                "spd": row[5],
                "text": row[6],
            }
            __list__.append(dic)
        conn.close()
        return __list__

    def arts_dict_list_generate(self, ):
        # {"id": 0, "name": "------", "target_type": "-------", "cost": 0, "attribute": "none", "damage_rate": 0,
        # "level": 0, "atk_impact": 0, "spd_impact": 0, "text": "------"},

        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute('SELECT * FROM martial_art')
        __list__ = []
        for row in cur:
            dic = {
                "id": row[0],
                "name": row[1],
                "target_type": row[2],
                "cost": row[3],
                "attribute": row[4],
                "damage_rate": row[5],
                "level": row[6],
                "atk_impact": row[7],
                "spd_impact": row[8],
                "text": row[9],
            }

            __list__.append(dic)

        conn.close()
        return __list__

    def weapons_dict_list_generate(self, ):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute('SELECT * FROM weapon')
        __list__ = []
        for row in cur:
            dic = {
                "id": row[0],
                "name": row[1],
                "atk": row[2],
                "text": row[3],
            }
            __list__.append(dic)
        conn.close()
        return __list__
        # key: [アイテム名,攻撃力,テキスト]

    def armors_dict_list_generate(self, ):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute('SELECT * FROM armor')
        __list__ = []
        for row in cur:
            dic = {
                "id": row[0],
                "name": row[1],
                "pro": row[2],
                "text": row[3],
            }
            __list__.append(dic)
        conn.close()
        return __list__
