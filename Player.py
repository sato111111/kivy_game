from Database import Database


class Player:
    """プレイヤーデータ"""
    sqlite = Database()
    gpi = sqlite.get_player_info()

    def __init__(
            self,
            # player_name="テストプレイヤー",
            player_party=[],
            max_cost=5
    ):
        self.name = self.gpi["name"]
        self.party = player_party
        self.max_cost = max_cost

    def get_player_name(self):
        return "私の名前は " + self.name + "です。"
