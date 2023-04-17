from operator import attrgetter

import japanize_kivy  # import するだけで機能する。
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.widget import Widget
import numpy as np

Config.set("graphics", "width", 700)
Config.set("graphics", "height", 700)

from Player import Player as Pl
from Character import Character as Ch
from time import sleep
from sounds.Sounds import Sounds as Se
from Battle import Battle
import dictionaries as di

# 指定したkvファイル読み込み
# Builder.load_file("my.kv")
"""ウィンドウ制御、レイアウト関連クラス"""

global g_player


class KiApp(App):
    def build(self):
        """ビルドされた時に1度だけ実行"""

        Window.size = (720, 1280)
        self.title = 'test game'
        self.icon = "image/icon.png"

        he = [Ch(1, 1), Ch(2, 1),
              Ch(3, 1)
              ]

        global g_player
        g_player = Pl("テストプレイヤー", he)

        # 起動時の実行環境の切り替え 「MainWidget()」,「TestWidget()」
        return self.env_execute(TestWidget())

    def env_execute(self, environment):  # 手続き型凝集、スタンプ結合
        """起動時の実行環境を選択"""
        sm = ScreenManager()
        rs = RootScreen(name="root_screen")
        mtw = MainTopWidget()
        ms = MenuScreen(name="menu_screen")
        bs = BattleScreen(name="battle_screen")

        environment_execute = sm  # スクリーンマネージャを起動
        environment_execute.add_widget(rs)  # SMにスクリーンを紐付け
        environment_execute.children[0].add_widget(mtw)  # スクリーンに画面上部のウィジェットを紐付け
        environment_execute.children[0].children[0].add_widget(environment)  # 上部のウィジェットに下部のウィジェットを紐付け
        environment_execute.add_widget(ms)

        return environment_execute

    def on_pause(self):
        """ ポーズ時のイベント """

        print('Pause')

        return True

    def on_resume(self):
        """ 復帰時のイベント """

        print('Return application')

        return False

    def on_start(self):
        return


class RootScreen(Screen):
    pass


class BattleScreen(Screen):
    pass


class MainTopWidget(GridLayout):

    def __init__(self, tplbl="", **kwargs):  # スタンプ結合
        super().__init__(**kwargs)
        self.top_label.text = tplbl if tplbl != "" else "ゲームスタート"

    def top_update_text_label(self, dt):
        self.text_label.text = self.txt_lbl

    def top_update_top_label(self, dt):
        self.top_label.text = self.top_lbl

    def menu_btn(self):  # 機能的凝集、スタンプ結合
        # メニュースライド呼び出し
        self.parent.manager.transition = WipeTransition()
        self.parent.manager.current = 'menu_screen'

    def top_menu_btn(self):  # メッセージ結合
        self.reset()

    def reset(self):  # 手続き型凝集、スタンプ結合
        self.clear_widgets()
        self.parent.add_widget(MainTopWidget("リセットしました"))
        self.parent.children[0].add_widget(MainWidget())


class SuperWidget(GridLayout):
    """MainWidget,BattleWidget専用の継承クラス"""
    art_dict = ObjectProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.se = Se()

    def widget_change(self, widget):  # 手続き型凝集、スタンプ結合
        pa = self.parent
        self.clear_widgets()
        pa.add_widget(widget)
        pa.remove_widget(pa.children[1])

    def update_top_label(self, dt):
        self.parent.top_label.text = self.top_lbl
        # Clock.schedule_once(self.update_top_label) で呼び出しで更新

    def update_text_label(self, dt):
        self.parent.text_label.text = self.txt_lbl
        # Clock.schedule_once(self.update_text_label) で呼び出しで更新

    def pushed_btn(self, btn_str: str):  # データ結合
        self.text_change(btn_str)

    def text_change(self, t):
        self.se.se_play("correct.mp3")


class MainWidget(SuperWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def text_change(self, t):
        super().text_change(t)
        ans = None

        if t == "A":
            ans = t + "ボタンを選択"
            self.widget_change(TestWidget())

        elif t == "B":
            ans = t + "ボタンを選択"

        elif t == "C":
            pass

        else:
            ans = t


class TestWidget(SuperWidget):
    """テスト環境用のレイアウトウィジェット
        モジュールの動作確認等に使う"""

    # target_type = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_ac_count = 0
        self.max_ac_count = 0
        self.current_turn = 0
        global g_player
        self.max_cost = g_player.max_cost
        player_party = g_player.party
        Clock.schedule_once(self.update_btn_welcome_test_env)
        self.en = [Ch(1), Ch(3), Ch(4)]
        self.order_of_action_list_insert = lambda: [self.parent.children[3].children[0].add_widget(chara_in_widget) for
                                                    chara_in_widget in
                                                    [OSHero(c) if c.is_hero == 1 else OSEnemy(c) for c in
                                                     sorted([c for c in player_party + self.en if c != "empty"],
                                                            reverse=True, key=attrgetter("spd"))]]

    def update_btn_welcome_test_env(self, dt):
        self.parent.top_label.text = "テスト環境" + str(self.current_turn) + "ターン目"
        self.parent.text_label.text = "テストテキスト"
        self.a_btn.text = "戦闘呼び出し(テスト)"
        self.b_btn.text = "(未実装)"
        self.c_btn.text = "(未実装)"

    def update_battle_text(self, dt):
        self.current_turn += 1
        self.parent.top_label.text = "戦闘：" + str(self.current_turn) + "ターン目"
        self.parent.text_label.text = "行動したいキャラクターを選択してください"
        self.a_btn.text = ""
        self.b_btn.text = ""
        self.c_btn.text = ""

    def text_change(self, t, _=None):

        super().text_change(t)
        if t == "戦闘呼び出し(テスト)":
            self.btn_ins()
            self.order_of_action_list_insert()
            self.turn_start()
        elif t == "戦闘実行(本番)":
            pass
        else:
            [self.target_select(arts) if arts["name"] == t else _ for arts in di.arts_dict_list]

    def turn_start(self):

        Clock.schedule_once(self.update_battle_text)
        hero_count = 0
        he_card = self.parent.children[2].children[0]

        # パーティの人数確認=============================
        for i in range(3):
            if he_card.children[i].hero_card.is_active != "empty":
                hero_count += 1
            else:
                pass

            print("hero_count:" + str(hero_count))
        self.max_ac_count = hero_count

    # == == == == == == == == == == == == == == =
    def turn_end(self):

        pa = self.parent.children[2].children[0]
        for i in range(3):
            if pa.children[i].hero_card.is_active != "down" and pa.children[i].hero_card.is_active != "empty":
                pa.children[i].hero_card.is_active = "standby"
                pa.children[i].hero_card.selected_arts.text = pa.children[i].sel_arts_bs
            else:
                pass
        self.turn_start()

    def target_select(self, arts):
        txt_lbl = ""
        if arts["target_type"] == "enemy":
            txt_lbl = "対象の敵を選択しよう"

            # self.parent.children[2].children[0].enemy_target_type = "enemy"
            target_type = "enemy"
            # canvasで選択対象を光らせるメソッド追加予定
        elif arts["target_type"] == "enemies":
            pass

        elif arts["target_type"] == "hero":
            txt_lbl = "対象を選択しよう"
            self.enemy_target_state = 1
            # canvasで選択対象を光らせるメソッド追加予定
        elif arts["target_type"] == "heroes":
            pass

        self.parent.text_label.text = txt_lbl

    def btn_ins(self, _=None):

        """画面左(HeroCard)にボタンを挿入"""
        left_pt_full = g_player.party + ["", ""]  # 先に空(empty)を挿入

        [self.parent.children[2].children[0].add_widget(chara_in_widget) for chara_in_widget in
         [HeroCard(c) if c != "" else EmptySpace() for c in left_pt_full[0:3]]]

        # 右画面にEnemyボタンを挿入

        bfr_pt_full = self.en + ["", ""]  # 後続に空を挿入

        [self.parent.children[2].children[2].add_widget(chara_in_widget) for chara_in_widget in
         [EnemyField(c) if c != "" else EmptySpace() for c in bfr_pt_full[0:3]]]


class HeroCard(ButtonBehavior, BoxLayout):
    """自陣カードの表示設定"""

    def __init__(self, character: Ch, **kwargs):
        super().__init__(**kwargs)
        chara = character

        self.name.text = chara.name_txt()
        self.hpbar.max = chara.maxhp
        self.hpbar.now = chara.hp
        self.hpbar.text = "HP:" + str(self.hpbar.now) + "/" + str(self.hpbar.max)

        self.hero_card.atk = chara.atk
        self.hero_card.spd = chara.spd
        self.arts_list = chara.arts

        self.sel_arts_bs = '(技名スペース)'
        self.selected_arts.text = self.sel_arts_bs
        # standby=行動前,active=行動中(原則一人),acted=行動済
        self.hero_card.is_active = "standby"
        self.hero_card.is_arts = "standby"

        Clock.schedule_interval(self.particle_animation, 2)

    def particle_animation(self, dt: object):
        prt = self.particle
        anime = Animation(part_x=40, part_y=40)
        anime.bind(on_complete=self.part_reset)
        anime.start(prt)

    def part_reset(self, *args):
        prt = args[1]

        if prt.part_c == 1:
            prt.part_x = 40
            prt.part_y = -40

        elif prt.part_c == 2:
            prt.part_x = -40
            prt.part_y = -40

        elif prt.part_c == 3 or prt.part_c == 4:
            prt.part_x = -40
            prt.part_y = 40

        elif prt.part_c == 5:
            prt.part_x = -40
            prt.part_y = -40

        elif prt.part_c == 6:
            prt.part_x = 40
            prt.part_y = -40

        else:
            prt.part_x = 40
            prt.part_y = 40
            prt.part_c = 0

        prt.part_c += 1

    def test_hp_damage(self, damage=0):

        if self.hpbar.now > damage > 0:
            self.hpbar.now -= damage
            self.hpbar.text = "HP:" + str(self.hpbar.now) + "/" + str(self.hpbar.max)
        else:
            self.hpbar.now = 0
            self.hpbar.text = "HP:0/" + str(self.hpbar.max)

    def arts_on_display(self: Ch):
        if self.hero_card.is_active != "acted":
            for i in range(3):
                if self.parent.children[i].is_active == "active":
                    self.parent.children[i].is_active = "standby"

            self.hero_card.is_active = "active"

            pnc = self.parent.parent.parent

            pnc.children[0].art_dict = self.arts_list
            # Buttonの名称を技名に変更
            pnc.children[0].a_btn.text = "技コスト:" + str(self.arts_list[0]["cost"]) + "\n　" + self.arts_list[0]["name"]
            pnc.children[0].b_btn.text = "技コスト:" + str(self.arts_list[1]["cost"]) + "\n　" + self.arts_list[1]["name"]
            pnc.children[0].c_btn.text = "技コスト:" + str(self.arts_list[2]["cost"]) + "\n　" + self.arts_list[2]["name"]

            pnc.text_label.text = "技を選択してください。"

        elif self.hero_card.is_active == "dead":
            pass
        else:
            pass


class EnemyField(ButtonBehavior, BoxLayout):
    """Heroウィジェットを設置するスペース兼Enemy表示
        継承クラスによる挙動の違い
        AnchorLayout = 重ねたカードが最前面へ
        BoxLayout = 重ねたカードが横に行きレイアウト内で共存
        """

    def __init__(self, character, **kwargs):
        super().__init__(**kwargs)
        self.enemy_name.text = character.name_txt()
        self.enemy_status.text = character.status_txt()

    def enemy_select(self):
        pa = self.parent.parent.children[0]
        pnc = self.parent.parent.parent.children[0]
        empty = ""
        for i in range(3):
            # for i in pa:
            if pa.children[i].hero_card.is_active == "active":
                pnc.is_ac_count += 1
                pa.children[i].hero_card.is_active = "acted"
                pa.children[i].hero_card.selected_arts.text = "決定"
                pnc.art_dict = empty
                pnc.a_btn.text = empty
                pnc.b_btn.text = empty
                pnc.c_btn.text = empty

            else:
                pass

        # if pa.children[0].hero_card.is_active == "acted" and pa.children[1].hero_card.is_active == "acted" and pa.children[2].hero_card.is_active == "acted":
        if pnc.is_ac_count == pnc.max_ac_count:
            pnc.is_ac_count = 0
            pnc.turn_end()


class BattleField(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 行動をここに格納し、行動時はここから呼び出す。
        self.act_1 = "is_not_Character"
        self.act_2 = "is_not_Character"
        self.act_3 = "is_not_Character"
        self.act_4 = "is_not_Character"
        self.act_5 = "is_not_Character"
        self.act_6 = "is_not_Character"


class MenuScreen(Screen):
    """メニューボタンを押すとメニューが開ける。
        下記にはkvファイルに登録した関数の処理を記述"""

    def main_slide(self):
        self.parent.transition = WipeTransition()
        self.parent.current = "root_screen"


class OSHero(BoxLayout):
    chara_name = ObjectProperty()

    def __init__(self, character, **kwargs):
        super().__init__(**kwargs)
        self.chara_name.text = character.name_txt()


class OSEnemy(BoxLayout):
    chara_name = ObjectProperty()

    def __init__(self, character, **kwargs):
        super().__init__(**kwargs)
        self.chara_name.text = character.name_txt()


class HeroesField(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EnemiesField(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EmptySpace(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
