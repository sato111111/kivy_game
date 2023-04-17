class Player:
    """プレイヤーデータ"""
    def __init__(
            self,
            player_name="テストプレイヤー",
            player_party=[],
            max_cost=5
    ):

        self.name = player_name
        self.party = player_party
        self.max_cost = max_cost

    def get_player_name(self):
        return "私の名前は " + self.name + "です。"