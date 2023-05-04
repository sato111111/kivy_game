import random
import debug
from kivy.graphics import Line

from supers import *

# 指定したkvファイル読み込み
# Builder.load_file("my.kv")

global g_player
global g_battle_party


class KiApp(App):
    def build(self):
        """ビルドされた時に1度だけ実行"""

        Window.size = (720, 1280)
        self.title = ''
        self.icon = "image/icon.png"

        he = [
            He(-1),
            He(-1),
            He(-1)
        ]

        global g_player
        g_player = Pl("テストプレイヤー", he)

        return self.env_execute()

    def env_execute(self, ):  # 手続き型凝集、スタンプ結合

        sm = RootScreenManager()  # スクリーンマネージャを起動

        return sm

    def screen_layout(self, sm, top_layout, btn_layout=None, current_screen=None):
        sm.current = current_screen if current_screen is not None else None
        sm.children[0].add_widget(top_layout)
        sm.children[0].children[0].add_widget(btn_layout) if btn_layout != None else None

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


class RootScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__ms__ = "main_screen"
        self.__bs__ = "battle_screen"
        self.__ss__ = "setting_screen"
        self.__create__()

    def __create__(self):
        btl = BattleTopLayout()
        bbl = BattleButtonLayout()
        mtl = MainTopLayout()

        self.add_widget(BattleScreen(name=self.__bs__))
        self.children[0].add_widget(btl)
        self.children[0].children[0].add_widget(bbl)

        self.add_widget(MainScreen(name=self.__ms__))
        self.current = self.__ms__
        self.children[0].add_widget(mtl)
        self.add_widget(SettingScreen(name=self.__ss__))

    def change_setting_screen(self, current_screen_name: str):
        self.transition = WipeTransition()
        self.current = self.__ss__
        self.current_screen.before_screen = current_screen_name


class MainTopLayout(SuperTopLayout):
    def __init__(self, tplbl="", **kwargs):
        super().__init__(**kwargs)
        self.top_label.text = tplbl if tplbl != "" else "ゲームスタート"
        self.current_screen_name = "main_screen"

    def top_menu_btn(self):
        self.reset()

    def reset(self):
        self.clear_widgets()
        self.parent.add_widget(MainTopLayout("リセットしました"))

    def battle_start(self):
        self.change_screen("battle_screen")

    def menu_btn(self):
        # setting_screen呼び出し
        self.change_setting_screen()


class BattleTopLayout(SuperTopLayout):
    def __init__(self, tplbl="", **kwargs):
        super().__init__(**kwargs)
        self.top_label.text = tplbl if tplbl != "" else "ゲームスタート"
        self.current_screen_name = "battle_screen"

    def top_menu_btn(self):
        content = PopupMenu(popup_no=self.popup_close, popup_yes=self.popup_run_away)
        self.popup = Popup(title="逃げますか？", content=content, size_hint=(0.5, 0.3))
        self.popup.open()

    def popup_run_away(self):
        self.reset()
        self.popup.dismiss()

    def popup_close(self):
        self.popup.dismiss()

    def reset(self):  # 手続き型凝集、スタンプ結合

        self.parent.manager.current = "main_screen"
        self.clear_widgets()
        self.remove_widget(self)
        self.parent.add_widget(BattleTopLayout("リセットしました"))
        self.parent.children[0].add_widget(BattleButtonLayout())

    def menu_btn(self):  # 機能的凝集、スタンプ結合
        # setting_screen呼び出し
        self.change_setting_screen()


class BattleButtonLayout(SuperButtonLayout):
    """戦闘用レイアウトBattleScreenに紐付ける"""
    global g_player
    global g_battle_party
    global G_PARTY_MEMBER_MAX
    current_turn_call_count = NumericProperty(0)
    turn_end_call_count = NumericProperty(0)
    select_hero_card = ObjectProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_turn = 1
        self.player = g_player
        self.is_ac_count = 0
        self.max_ac_count = 0
        self.acted_list = []
        self.sorted_acted_lst = []
        self.enemy_party = debug.enemies_generate(En)
        self.DEBUG_BTN()

    def on_turn_end_call_count(self, instance, value):

        if value == 1:
            self.turn_end()
        else:
            pass

    def on_current_turn_call_count(self, instance, value):
        if value < 1:
            self.current_turn += 1
        else:
            pass

    def order_list_insert(self):
        sort_order_list = sorted(
            [c for c in [c_not_empty for c_not_empty in self.player.party + self.enemy_party if c_not_empty != "EMPTY"]
             if c.hp > 0], reverse=True,
            key=attrgetter("spd"))

        [self.parent.action_list.order_space.add_widget(chara_card) for chara_card in
         [OrderListHero(c) if c.IS_TYPE is "HERO" else OrderListEnemy(c) for c in sort_order_list]]

    def order_list_update(self):
        self.parent.action_list.order_space.clear_widgets()
        self.order_list_insert()

    def DEBUG_BTN(self):
        self.a_btn.text = "戦闘開始(テスト)"
        self.b_btn.text = "(未実装)"
        self.c_btn.text = "(未実装)"

    def update_battle_text(self):
        self.current_turn_call_count += 1
        self.parent.top_label.text = "戦闘：" + str(self.current_turn) + "ターン目"
        self.parent.text_label.text = "行動したいキャラクターを選択してください"
        self.a_btn.text = ""
        self.b_btn.text = ""
        self.c_btn.text = ""

    def text_change(self, t, ):
        super().text_change(t)
        if t is "戦闘開始(テスト)":
            self.card_insert()
            self.order_list_insert()
            self.turn_start()


        elif t == "戦闘実行(本番)":
            pass

    def action_exe(self, btn_int, ):

        self.select_hero_card.select_art = self.select_hero_card.chara.arts_list[btn_int]
        return self.target_select()

    def turn_start(self):
        self.update_battle_text()
        hero_count = 0
        hc = self.parent.children[2].children[0]
        self.current_turn_call_count += 1
        # パーティの人数確認=============================
        for i in range(G_PARTY_MEMBER_MAX):
            if hc.children[i].is_active is "EMPTY" or hc.children[i].is_active is "DOWN":
                pass
            else:
                hero_count += 1
        print(f"hero_count:{hero_count}")
        self.max_ac_count = hero_count

    # == == == == == == == == == == == == == ==

    def action_start(self):
        """
        各種カウントの初期化
        current_turn_call_count ：ターン数経過の呼び出したが重複しないようにする
        turn_end_call_count ：turn_endの呼び出したが重複しないようにする
        :return:
        """
        self.current_turn_call_count = 0
        self.turn_end_call_count = 0
        ###デバッグ用にenemyの行動を強制決定↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        for enemy_card in self.parent.battle_field.enemies_field.children:
            if hasattr(enemy_card, "hp"):
                if enemy_card.hp > 0:
                    # enemy_card.select_art = enemy_card.chara.arts_list[random.randrange(2) + 1]
                    enemy_card.select_art = enemy_card.chara.arts_list[0]
                    enemy_card.visitor_target_no = 0
                    self.acted_list.append(enemy_card)

        ###デバッグ用↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        # 素早さ順にアクションを起こすようにリストをソート
        self.sorted_acted_lst = sorted(self.acted_list, reverse=True, key=attrgetter("spd"))

        # アクションスタート

        for c in self.sorted_acted_lst:
            if c.chara.IS_TYPE is "HERO":
                e = self.parent.battle_field.enemies_field.children[c.visitor_target_no]
                e.hp -= c.select_art.normal_attack()
            elif c.chara.IS_TYPE is not "HERO":
                h = self.parent.battle_field.heroes_field.children[c.visitor_target_no]
                h.hp -= c.select_art.normal_attack()

    def turn_end(self, ):
        # self.parent.parent.canvas.remove()

        for i in range(G_PARTY_MEMBER_MAX):
            pc2c = self.parent.children[2].children[0].children[i]

            if pc2c.is_active != "DOWN" and pc2c.is_active != "EMPTY":
                pc2c.is_active = "STANDBY"
                pc2c.selected_art.text = ''
        self.order_list_update()
        self.acted_list = []
        self.select_hero_card = ""

        return self.turn_start()

    def battle_end(self):
        for i in range(G_PARTY_MEMBER_MAX):
            self.parent.battle_field.heroes_field.children[i].alive = False
        self.parent.reset()

    def target_select(self, ):
        txt_lbl = ""
        if self.select_hero_card.select_art.target_type == "VISITOR":
            txt_lbl = "対象の敵を選択しよう"

            # canvasで選択対象を光らせるメソッド追加予定
        elif self.select_hero_card.select_art.target_type == "VISITORS":
            pass

        elif self.select_hero_card.select_art.target_type == "OWN":
            txt_lbl = "対象を選択しよう"
            # canvasで選択対象を光らせるメソッド追加予定
        elif self.select_hero_card.select_art.target_type == "OWNS":
            pass
        else:
            pass
        self.parent.text_label.text = txt_lbl

    def card_insert(self, ):

        """HeroFieldに(右側)にカードを挿入"""
        hero_full_pt = self.player.party + ["", ""]  # 先に空(empty)を挿入

        [self.parent.battle_field.heroes_field.add_widget(h_in_widget) for h_in_widget in
         [HeroCard(h) if h != "" else EmptyCard() for h in hero_full_pt[0:G_PARTY_MEMBER_MAX]]]

        for i, _ in enumerate([2, 1, 0]):
            self.parent.battle_field.heroes_field.children[i].party_no = i
        # 右画面にEnemyボタンを挿入

        enemy_full_pt = self.enemy_party + ["", ""]  # 後続に空を挿入

        [self.parent.battle_field.enemies_field.add_widget(e_in_widget) for e_in_widget in
         [EnemyCard(e) if e != "" else EmptyCard() for e in enemy_full_pt[0:G_PARTY_MEMBER_MAX]]]

        for i, _ in enumerate([0, 1, 2]):
            self.parent.battle_field.enemies_field.children[i].party_no = i


class HeroesField(SuperField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class HeroCard(SuperCard):
    """is HeroCard表示設定"""

    def __init__(self, character: He, **kwargs):
        super().__init__(character, **kwargs)
        self.selected_art.text = ''
        self.card_pos_x = ""
        self.card_pos_y = ""
        self.alive = True

        # standby=行動前,active=行動中(原則一人),acted=行動済

    def on_alive(self, instance, boolean: bool):
        if boolean:
            Clock.schedule_interval(self.particle_animation, 2)

        elif boolean is False:
            Clock.unschedule(self.particle_animation)

    def on_is_active(self, instance, word: str):
        """
        :param instance:
        :param str: activeステータス(standby,active,acted)がある。
        :return: (standby=未選択状態なら)select_artを初期化
        """
        if word is "STANDBY":
            self.select_art = ""
        elif word is "DOWN":
            self.selected_art.text = ""

    def particle_animation(self, dt:object):
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

    def arts_on_display(self):
        """
        選択したHeroCard対象にreturnを返す
        :return: BattleButtonLayoutのボタンに技名を表示する
        """
        # HeroCardを選択した後にBattleButtonLayoutのButtonのテキストにHeroの技(Arts)を表示させる処理
        ppp = self.parent.parent.parent
        if self.is_active is "STANDBY":

            for i in range(G_PARTY_MEMBER_MAX):
                if self.parent.children[i].is_active == "ACTIVE":
                    self.parent.children[i].is_active = "STANDBY"

            self.is_active = "ACTIVE"

            # BattleButtonLayoutへ送る

            ppp.children[0].select_hero_card = self
            # Buttonの名称を技名に変更
            for i, btn in enumerate(["a", "b", "c"]):
                c = self.chara.arts_list[i]
                ppp.children[0].ids[f"{btn}_btn"].text = f'技コスト:{c.cost} \n {c.name}'

            ppp.text_label.text = "技を選択してください。"

        elif self.is_active is "DOWN":
            pass
        else:
            pass


class EnemyCard(SuperCard):
    """IS_TYPE = ENEMY 表示設定"""

    def __init__(self, character: En, **kwargs):
        super().__init__(character, **kwargs)
        self.strt_x = 0
        self.strt_y = 0
        global G_PARTY_MEMBER_MAX

    def enemy_select(self):
        pppc = self.parent.parent.parent.children[0]
        if hasattr(pppc.select_hero_card, "select_art") and hasattr(pppc.select_hero_card.select_art, "target_type"):
            if pppc.select_hero_card.select_art.target_type == "VISITOR" and pppc.select_hero_card.select_art is not None:
                return self.enemy_selected()

    def enemy_selected(self, ):
        """


        :return:
        """
        ppc = self.parent.parent.children[0]
        pppc = self.parent.parent.parent.children[0]
        empty = ""
        print(self.chara.name)
        for i in range(G_PARTY_MEMBER_MAX):
            hc = ppc.children[i]
            if hc.is_active is "ACTIVE":

                pppc.is_ac_count += 1

                self.strt_x = hc.card_pos_x
                self.strt_y = hc.card_pos_y
                # BattleScreenにCanvasを追加しLineを描写
                # self.parent.parent.parent.parent.canvas.add(Line(points=[self.strt_x, self.strt_y, self.goal_x - self.tri_x, self.goal_y], width=7),)

                hc.selected_art.text = f"『　{pppc.select_hero_card.select_art.name}　』"

                hc.visitor_target_no = self.party_no
                hc.is_active = "ACTED"

                for btn in ["a", "b", "c"]:
                    pppc.ids[f"{btn}_btn"].text = empty
                pppc.acted_list.append(pppc.select_hero_card)
            else:
                pass
        if pppc.is_ac_count == pppc.max_ac_count:
            pppc.is_ac_count = 0

            return pppc.action_start()

        else:
            pass


class BattleField(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 行動をここに格納し、行動時はここから呼び出す。
