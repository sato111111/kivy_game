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
            # He(-1)
        ]

        global g_player
        g_player = Pl("テストプレイヤー", he)

        return self.env_execute()

    def env_execute(self, ):  # 手続き型凝集、スタンプ結合

        sm = ScreenManager()  # スクリーンマネージャを起動
        [
            sm.add_widget(screen) for screen in
            (
                BattleScreen(name="battle_screen"),
                MainScreen(name="main_screen"),
                BSettingScreen(name="b_s_s"),
                MSettingScreen(name="m_s_s"),
            )
        ]

        btl = BattleTopLayout()
        mtl = MainTopLayout()

        bl = BattleButtonLayout()
        ml = MainButtonLayout()

        self.screen_layout(sm, btl, bl)
        self.screen_layout(sm, mtl, ml, "main_screen")

        return sm

    def screen_layout(self, sm, top_layout, btn_layout, current_screen=None):
        sm.current = current_screen if current_screen is not None else None
        sm.children[0].add_widget(top_layout)
        sm.children[0].children[0].add_widget(btn_layout)

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


class MainTopLayout(SuperTopLayout):
    def __init__(self, tplbl="", **kwargs):
        super().__init__(**kwargs)
        self.top_label.text = tplbl if tplbl != "" else "ゲームスタート"

    def top_menu_btn(self):
        self.reset()

    def reset(self):
        self.clear_widgets()
        self.parent.add_widget(MainTopLayout("リセットしました"))
        self.parent.children[0].add_widget(MainButtonLayout())

    def menu_btn(self):
        # setting_screen呼び出し
        self.change_screen("m_s_s")


class BattleTopLayout(SuperTopLayout):
    def __init__(self, tplbl="", **kwargs):
        super().__init__(**kwargs)
        self.top_label.text = tplbl if tplbl != "" else "ゲームスタート"

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
        self.parent.add_widget(BattleTopLayout("リセットしました"))
        self.parent.children[0].add_widget(BattleButtonLayout())

    def menu_btn(self):  # 機能的凝集、スタンプ結合
        # setting_screen呼び出し
        self.change_screen("b_s_s")


class MainButtonLayout(SuperButtonLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def text_change(self, t):
        super().text_change(t)

        if t == "A":
            self.parent.change_screen("battle_screen")

        elif t == "B":
            pass

        elif t == "C":
            pass

        else:
            pass


class BattleButtonLayout(SuperButtonLayout):
    """戦闘用レイアウトBattleScreenに紐付ける"""
    global g_player
    global g_battle_party

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = g_player
        self.is_ac_count = 0
        self.max_ac_count = 0
        self.current_turn = 0
        self.acted_list = []
        self.select_hero = ""
        self.enemy_party = debug.enemies_generate(En)
        Clock.schedule_once(self.update_btn)

    def order_list_insert(self):
        [self.parent.children[3].children[0].add_widget(chara_in_widget) for chara_in_widget in
         [OrderListHero(c) if c.IS_TYPE is "HERO" else OrderListEnemy(c) for c in
          sorted([c for c in self.player.party + self.enemy_party if c != "empty"], reverse=True,
                 key=attrgetter("spd"))]]

    def update_btn(self, dt):
        self.a_btn.text = "戦闘開始(テスト)"
        self.b_btn.text = "(未実装)"
        self.c_btn.text = "(未実装)"

    def update_battle_text(self, dt):
        self.current_turn += 1
        self.parent.top_label.text = "戦闘：" + str(self.current_turn) + "ターン目"
        self.parent.text_label.text = "行動したいキャラクターを選択してください"
        self.a_btn.text = ""
        self.b_btn.text = ""
        self.c_btn.text = ""

    def text_change(self, t, ):
        super().text_change(t)
        if t == "戦闘開始(テスト)":
            self.btn_ins()
            self.order_list_insert()
            self.turn_start()

        elif t == "戦闘実行(本番)":
            pass

    def action_exe(self, btn_int, ):
        r = None
        try:

            self.select_hero.select_art = self.select_hero.arts_list[btn_int]
            r = self.target_select()
        except AttributeError:
            pass
        return r

    def turn_start(self):

        Clock.schedule_once(self.update_battle_text)
        hero_count = 0
        hc = self.parent.children[2].children[0]

        # パーティの人数確認=============================
        for i in range(3):
            if hc.children[i].hero_card.is_active != "empty":
                hero_count += 1
            else:
                pass

        self.max_ac_count = hero_count

    # == == == == == == == == == == == == == ==

    def action_start(self):
        # ソートしたアクション決定済みリスト
        self.srtd_actd_lst = sorted(self.acted_list, reverse=True, key=attrgetter("spd"))
        # これからアクションを起こすリスト
        for c in self.srtd_actd_lst:
            print(c.IS_TYPE)
            if c.IS_TYPE == "HERO":
                c.hp -= 10
                print(c.hp)
            else:
                pass

        Clock.schedule_once(self.hero_hp_update)

        return self.turn_end()

    def hero_hp_update(self, dt):
        for i, c in enumerate(self.player.party,start=1):
            hc = self.parent.children[2].children[0].children[i]
            if hasattr(hc.chara, "hp"):
                if hc.chara.hp > 0:

                    hc.hpbar.now = hc.chara.hp
                    hc.hpbar.text = f"HP:{hc.chara.hp}/{hc.chara.maxhp}"
                else:
                    hc.hpbar.text = f"HP:0/{hc.chara.maxhp}"
            else:
                pass

    def turn_end(self, ):

        print("turn_end1")
        # self.parent.parent.canvas.remove()

        for i in range(3):
            pc2c = self.parent.children[2].children[0].children[i]

            if pc2c.hero_card.is_active != "down" and pc2c.hero_card.is_active != "empty":
                pc2c.hero_card.is_active = "standby"
                pc2c.hero_card.selected_art.text = '(技名スペース)'
                print("turn_end2")

            else:
                pass
        print("turn_end3")

        self.acted_list = []
        self.select_hero = ObjectProperty("")
        return self.turn_start()

    def target_select(self, ):
        txt_lbl = ""
        if self.select_hero.select_art.target_type == "enemy":
            txt_lbl = "対象の敵を選択しよう"

            # canvasで選択対象を光らせるメソッド追加予定
        elif self.select_hero.select_art.target_type == "enemies":
            pass

        elif self.select_hero.select_art.target_type == "hero":
            txt_lbl = "対象を選択しよう"
            self.enemy_target_state = 1
            # canvasで選択対象を光らせるメソッド追加予定
        elif self.select_hero.select_art.target_type == "heroes":
            pass
        else:
            pass
        self.parent.text_label.text = txt_lbl

    def btn_ins(self, ):

        """HeroFieldに(右側)にカードを挿入"""
        left_pt_full = self.player.party + ["", ""]  # 先に空(empty)を挿入
        print(
        [self.parent.children[2].children[0].add_widget(chara_in_widget) for chara_in_widget in
         [HeroCard(h) if h != "" else EmptySpace() for h in left_pt_full[0:3]]]
        )
        # 右画面にEnemyボタンを挿入

        bfr_pt_full = self.enemy_party + ["", ""]  # 後続に空を挿入

        [self.parent.children[2].children[2].add_widget(chara_in_widget) for chara_in_widget in
         [EnemyCard(e) if e != "" else EmptySpace() for e in bfr_pt_full[0:3]]]


class HeroCard(SuperCard):
    """is HeroCard表示設定"""


    def __init__(self, character: He, **kwargs):
        super().__init__(character, **kwargs)
        self.hero_card.is_active = "standby"

        self.selected_art.text = '(技名スペース)'
        # standby=行動前,active=行動中(原則一人),acted=行動済

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

    def arts_on_display(self):
        # HeroCardを選択した後にBattleButtonLayoutのButtonのテキストにHeroの技(Arts)を表示させる処理

        if self.hero_card.is_active != "acted":

            for i in range(3):
                if self.parent.children[i].is_active == "active":
                    self.parent.children[i].is_active = "standby"

            self.hero_card.is_active = "active"

            # BattleButtonLayoutへ送る

            ppp = self.parent.parent.parent
            ppp.children[0].select_hero = self.chara
            # ppp.children[0].hero_action_art = self.chara.arts_list
            # Buttonの名称を技名に変更
            for i, btn in enumerate(["a", "b", "c"]):
                ppp.children[0].ids[
                    f"{btn}_btn"].text = f'技コスト:{self.chara.arts_list[i].cost} \n {self.chara.arts_list[i].name}'

            ppp.text_label.text = "技を選択してください。"

        elif self.hero_card.is_active == "down":
            pass
        else:
            pass


class EnemyCard(SuperCard):
    """IS_TYPE = ENEMY 表示設定"""

    def __init__(self, character: En, **kwargs):
        super().__init__(character, **kwargs)
        self.strt_x = 0
        self.strt_y = 0

    def enemy_select(self):
        r = None

        pppc = self.parent.parent.parent.children[0]

        if hasattr(pppc.select_hero.select_art, "target_type"):
            if pppc.select_hero.select_art.target_type == "enemy" and pppc.select_hero.select_art is not None:
                r = self.enemy_selected()
            else:
                pass

        else:
            pass
        return r

    def enemy_selected(self):
        ppc = self.parent.parent.children[0]
        pppc = self.parent.parent.parent.children[0]
        empty = ""

        for i in range(3):
            hc = ppc.children[i]
            r = None
            if hc.hero_card.is_active is "active":

                pppc.is_ac_count += 1

                self.strt_x = hc.hero_card.card_pos_x
                self.strt_y = hc.hero_card.card_pos_y
                # BattleScreenにCanvasを追加
                # self.parent.parent.parent.parent.canvas.add(Line(points=[self.strt_x, self.strt_y, self.goal_x - self.tri_x, self.goal_y], width=7),)

                hc.selected_art.text = f"『　{pppc.select_hero.select_art.name}　』"
                pppc.select_hero.select_art = None
                hc.hero_card.is_active = "acted"

                for btn in ["a", "b", "c"]:
                    pppc.ids[f"{btn}_btn"].text = empty
                pppc.acted_list.append(pppc.select_hero)

            else:
                pass
        # if pa.children[0].hero_card.is_active == "acted" and pa.children[1].hero_card.is_active == "acted" and pa.children[2].hero_card.is_active == "acted":
        if pppc.is_ac_count == pppc.max_ac_count:
            r = pppc.action_start()
            pppc.is_ac_count = 0

        else:
            pass
            return r


class BattleField(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 行動をここに格納し、行動時はここから呼び出す。
