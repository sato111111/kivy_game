import random

from supers import *

# 指定したkvファイル読み込み
# Builder.load_file("my.kv")

global g_player


class KiApp(App):
    def build(self):
        """ビルドされた時に1度だけ実行"""

        Window.size = (720, 1280)
        self.title = ''
        self.icon = "image/icon.png"

        he = [
            Ch(-1, 1),
            #Ch(-1, 1),
            #Ch(-1, 1)
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
    def __init__(self, tplbl="", **kwargs):  # スタンプ結合
        super().__init__(**kwargs)
        self.top_label.text = tplbl if tplbl != "" else "ゲームスタート(MTL)"

    def top_menu_btn(self):  # メッセージ結合
        self.reset()

    def reset(self):  # 手続き型凝集、スタンプ結合

        self.clear_widgets()
        self.parent.add_widget(MainTopLayout("リセットしました"))
        self.parent.children[0].add_widget(MainButtonLayout())

    def menu_btn(self):  # 機能的凝集、スタンプ結合
        # setting_screen呼び出し
        self.change_screen("m_s_s")


class BattleTopLayout(SuperTopLayout):
    def __init__(self, tplbl="", **kwargs):  # スタンプ結合
        super().__init__(**kwargs)
        self.top_label.text = tplbl if tplbl != "" else "ゲームスタート(BTL)"

    def top_menu_btn(self):  # メッセージ結合
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

    art_dict = ObjectProperty("")
    acted_list = ObjectProperty([])
    act_arts = ObjectProperty([])
    global g_player

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_ac_count = 0
        self.max_ac_count = 0
        self.current_turn = 0

        self.player = g_player
        self.enemy_party = self.enemies_generate()
        Clock.schedule_once(self.update_btn)

    # buttonから呼び出される
    def action_exe(self, t, _=None):
        return [self.target_select(arts) if arts["name"] == t else _ for arts in di.arts_dict_list]

    def order_list_insert(self):
        [self.parent.children[3].children[0].add_widget(chara_in_widget) for chara_in_widget in
         [OrderListHero(c) if c.is_hero == 1 else OrderListEnemy(c) for c in
          sorted([c for c in self.player.party + self.enemy_party if c != "empty"], reverse=True,
                 key=attrgetter("spd"))]]

    def enemies_generate(self):
        en = [
            Ch(random.randrange(1, 10)),
            Ch(random.randrange(1, 10)),
            Ch(random.randrange(1, 10)),
        ]
        return en

    def update_btn(self, dt):
        # self.parent.top_label.text = "テスト環境" + str(self.current_turn) + "ターン目"
        # self.parent.text_label.text = "テストテキスト"
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

    def text_change(self, t, _=None):

        super().text_change(t)
        if t == "戦闘開始(テスト)":
            self.btn_ins()
            self.order_list_insert()
            self.turn_start()
        elif t == "戦闘実行(本番)":
            pass

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

    def action_start(self):
        print("acted_list:", self.acted_list)
        action_list = []
        for i in range(len(self.acted_list)):
            action_list.append(
                [
                    self.acted_list[i],
                    self.act_arts[i],
                ]
            )

        print(action_list[0][0])

        srtd_actd_lst = sorted([chara[0]for chara in action_list], reverse=True, key=attrgetter("spd"))
        print(srtd_actd_lst)
        srtd_actn_lst = [[g[0], g[1]] for g in srtd_actd_lst]

        for act in srtd_actn_lst:
            print(act[0].name)
            print(act[1]["name"])

        return self.turn_end()

    def turn_end(self):

        pa = self.parent.children[2].children[0]
        for i in range(3):
            if pa.children[i].hero_card.is_active != "down" and pa.children[i].hero_card.is_active != "empty":
                pa.children[i].hero_card.is_active = "standby"
                pa.children[i].hero_card.selected_arts.text = pa.children[i].sel_arts_bs
            else:
                pass
        self.acted_list = ObjectProperty([])
        return self.turn_start()

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

        """HeroFieldに(右側)にカードを挿入"""
        left_pt_full = self.player.party + ["", ""]  # 先に空(empty)を挿入

        [self.parent.children[2].children[0].add_widget(chara_in_widget) for chara_in_widget in
         [HeroCard(c) if c != "" else EmptySpace() for c in left_pt_full[0:3]]]

        # 右画面にEnemyボタンを挿入

        bfr_pt_full = self.enemy_party + ["", ""]  # 後続に空を挿入

        [self.parent.children[2].children[2].add_widget(chara_in_widget) for chara_in_widget in
         [EnemyCard(c) if c != "" else EmptySpace() for c in bfr_pt_full[0:3]]]


class HeroCard(ButtonBehavior, BoxLayout):
    """自陣カードの表示設定"""
    selected_arts_no = ObjectProperty(None)

    def __init__(self, character: Ch, **kwargs):
        super().__init__(**kwargs)
        self.chara = character

        self.name.text = self.chara.name_txt()
        self.hpbar.max = self.chara.maxhp
        self.hpbar.now = self.chara.hp
        self.hpbar.text = "HP:" + str(self.hpbar.now) + "/" + str(self.hpbar.max)

        self.hero_card.atk = self.chara.atk
        self.hero_card.spd = self.chara.spd
        self.arts_list = self.chara.arts

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
        # バー動作確認用の自傷ダメージ処理
        if self.hpbar.now > damage > 0:
            self.hpbar.now -= damage
            self.hpbar.text = "HP:" + str(self.hpbar.now) + "/" + str(self.hpbar.max)
        else:
            self.hpbar.now = 0
            self.hpbar.text = "HP:0/" + str(self.hpbar.max)

    def arts_on_display(self: Ch):
        # HeroCardを選択した後にBattleButtonLayoutのButtonのテキストにHeroの技(Arts)を表示させる処理
        if self.hero_card.is_active != "acted":
            for i in range(3):
                if self.parent.children[i].is_active == "active":
                    self.parent.children[i].is_active = "standby"

            self.hero_card.is_active = "active"

            # BattleButtonLayoutへ送る
            pnc = self.parent.parent.parent

            pnc.children[0].acted_list.append(self.chara)
            pnc.children[0].art_dict = self.arts_list
            # Buttonの名称を技名に変更
            for i, btn in enumerate(["a", "b", "c"]):
                pnc.children[0].ids[f"{btn}_btn"].text = "技コスト:" + str(self.arts_list[i]["cost"]) + "\n　" + \
                                                         self.arts_list[i]["name"]

            pnc.text_label.text = "技を選択してください。"

        elif self.hero_card.is_active == "dead":
            pass
        else:
            pass


class EnemyCard(ButtonBehavior, BoxLayout):
    """
    Enemyカード
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
            hc = pa.children[i]
            if hc.hero_card.is_active == "active":
                pnc.is_ac_count += 1
                hc.hero_card.is_active = "acted"
                # self.parent.parent.battle_field.act_list.append(self.parent.parent.children[2].hero_card.chara)
                hc.selected_arts.text = "決定"
                pnc.art_dict = empty
                for btn in ["a", "b", "c"]:
                    pnc.ids[f"{btn}_btn"].text = empty


            else:
                pass

        # if pa.children[0].hero_card.is_active == "acted" and pa.children[1].hero_card.is_active == "acted" and pa.children[2].hero_card.is_active == "acted":
        if pnc.is_ac_count == pnc.max_ac_count:
            pnc.is_ac_count = 0
            pnc.action_start()


class BattleField(BoxLayout):
    act_list = ObjectProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 行動をここに格納し、行動時はここから呼び出す。
