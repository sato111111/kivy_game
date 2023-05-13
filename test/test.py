import random

# ガチャのアイテムリスト
items = [
    {'name': 'アイテムA', 'rate': 0.1},
    {'name': 'アイテムB', 'rate': 0.3},
    {'name': 'アイテムC', 'rate': 0.6},
]

# ガチャを実行する関数
def run_gacha():
    rand = random.random()  # 0から1のランダムな値を生成
    print(f"rand:{rand}")
    # 確率に基づいてアイテムを選ぶ
    for item in items:
        if rand < item['rate']:
            return item['name']

    return 'なし'  # 全ての確率に合致しなかった場合

# ガチャを10回実行して結果を表示
for _ in range(10):
    result = run_gacha()
    print(result)