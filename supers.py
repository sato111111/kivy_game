from operator import attrgetter

import japanize_kivy  # import するだけで機能する。
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.widget import Widget

from kivy.uix.popup import Popup
from Player import Player as Pl
from Character import Character as Ch, Empty
from Character import Hero as He
from Character import Enemy as En

from time import sleep
from sounds.Sounds import Sounds as Se
from Battle import Battle
import dictionaries as di


a="""def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"LOG: {func.__name__} was called with {args} and {kwargs}")

        return func(*args, **kwargs)

    return wrapper"""


class MainScreen(Screen):
    pass

class BattleScreen(Screen):
    pass
class SettingScreen(Screen):
    """メニューボタンを押すとメニューが開ける。
        下記にはkvファイルに登録した関数の処理を記述"""
    before_screen = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)
        self.before_screen = ""
    def main_slide(self):
        self.parent.transition = WipeTransition()
        self.parent.current = self.before_screen

class SuperTopLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def top_update_text_label(self, dt):
        self.text_label.text = self.txt_lbl

    def top_update_top_label(self, dt):
        self.top_label.text = self.top_lbl

    def change_screen(self, screen_name: str):
        self.parent.manager.transition = WipeTransition()
        self.parent.manager.current = screen_name


    def change_setting_screen(self,):
        self.parent.manager.change_setting_screen(self.current_screen_name)


class SuperButtonLayout(GridLayout):
    """MainWidget,BattleWidget専用の継承クラス"""

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


class SuperCard(ButtonBehavior, BoxLayout):
    chara = ObjectProperty()
    hp = NumericProperty(None)
    hp_bar = ObjectProperty(None)
    hero_target_no = NumericProperty(None)
    enemy_target_no = NumericProperty(None)
    is_down = BooleanProperty(False)
    is_start = BooleanProperty(True)
    is_active = StringProperty("standby")
    select_art = ObjectProperty("")

    def __init__(self, character: Ch, **kwargs):
        super().__init__(**kwargs)
        self.party_no = None
        self.chara = character
        self.name.text = self.chara.name_txt()
        self.hp = self.chara.hp
        self.hp_bar.max = self.chara.maxhp
        self.hp_bar.now = self.chara.hp
        self.hp_bar.text = f"HP:{int(self.hp)}/{self.chara.maxhp}"
        self.PARTY_MAX_PEOPLE = 3

    def on_hp(self, instance, value):
        if self.is_start != True:
            if value != self.hp_bar.now:
                if value <= 0:
                    self.hp = 0
                self.chara.hp = self.hp
                Clock.schedule_interval(self.update_hp_bar, 0.01)
        else:
            self.is_start = False

    def update_hp_bar(self, dt):

        if self.hp <= 0:
            self.hp = 0
        if self.hp == self.hp_bar.now:
            Clock.unschedule(self.update_hp_bar)
            return self.parent.party_hp_checker()

        if self.hp_bar.now > self.hp:
            self.hp_bar.now -= 1
        elif self.hp_bar.now < self.hp:
            self.hp_bar.now += 1
        elif self.hp_bar.now == 0:
            self.is_down = True

        self.hp_bar.text = f"HP:{int(self.hp_bar.now)}/{self.hp_bar.max}"


class SettingScreen(Screen):
    """メニューボタンを押すとメニューが開ける。
        下記にはkvファイルに登録した関数の処理を記述"""


    def __init__(self, **kw):
        super().__init__(**kw)
        self.before_screen = ""
    def change_screen_before(self):
        self.manager.transition = WipeTransition()
        self.manager.current = self.before_screen




class OrderListHero(BoxLayout):
    chara_name = ObjectProperty()

    def __init__(self, character, **kwargs):
        super().__init__(**kwargs)
        self.chara_name.text = character.name_txt()


class OrderListEnemy(BoxLayout):
    chara_name = ObjectProperty()

    def __init__(self, character, **kwargs):
        super().__init__(**kwargs)
        self.chara_name.text = character.name_txt()


class SuperField(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.PARTY_MAX_PEOPLE = 3

    def get_party_checker(self, dt):
        return self.party_hp_checker()

    def party_hp_checker(self):
        cckr = 0
        for i in range(self.PARTY_MAX_PEOPLE):
            party = self.children[i]
            if hasattr(party, "hp_bar"):
                if int(party.hp_bar.now) != int(party.hp):
                    cckr += 1
        if cckr != 0:
            return Clock.schedule_once(self.get_party_checker)
        elif cckr == 0:
            return self.party_down_checker()

    def party_down_checker(self):
        alive = 0
        for i in range(self.PARTY_MAX_PEOPLE):
            party = self.children[i]
            if hasattr(party, "hp_bar"):
                if party.hp_bar.now > 0:
                    alive += 1
        if alive >= 1:
            self.parent.parent.parent.parent.children[0].children[0].children[0].turn_end_call_count += 1
            return
        elif alive == 0:
            if hasattr(self.parent.parent, "parent"):
                self.parent.parent.parent.parent.children[0].children[0].children[0].battle_end()
            return


class EnemiesField(SuperField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EmptyCard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.party_no = None


class PopupMenu(BoxLayout):
    popup_no = ObjectProperty(None)
    popup_yes = ObjectProperty(None)
