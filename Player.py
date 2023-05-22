from Database import Database
from Character import Hero


class Player:
    """プレイヤーデータ"""
    db = Database()
    player_info = db.get_player_info()
    player_party = db.get_player_party()
    def __init__(self,):
        self.id = self.player_info["id"]
        self.name = self.player_info["name"]
        self.max_cost = self.player_info["cost"]
        self.character_list_limit = self.player_info["list_limit"]
        self.play_limit = self.player_info["play_time"],
        self.year = self.player_info["year"],
        self.month = self.player_info["month"],
        self.day = self.player_info["day"],
        self.party = self.set_player_party()
    def set_player_party(self):
        return [Hero(chara["character_number"]) for chara in self.player_party]
    def set_have_player_character(self,result):
        self.db.set_have_player_character(result)


    def get_player_name(self):
        return "私の名前は " + self.name + "です。"
    def get_have_hero(self):
        return self.db.get_have_player_character()
