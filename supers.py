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

from kivy.uix.popup import Popup
from Player import Player as Pl
from Character import Character as Ch, Empty
from Character import Hero as He
from Character import Enemy as En

from time import sleep
from sounds.Sounds import Sounds as Se
from Battle import Battle
import dictionaries as di


class MainScreen(Screen):
    pass


class BattleScreen(Screen):
    pass


class SuperTopLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def top_update_text_label(self, dt):
        self.text_label.text = self.txt_lbl

    def top_update_top_label(self, dt):
        self.top_label.text = self.top_lbl

    def change_screen(self, screen_name: str):
        pa = self.parent
        pa.manager.transition = WipeTransition()
        pa.manager.current = screen_name


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
    def __init__(self, character: Ch, **kwargs):
        super().__init__(**kwargs)
        self.chara = character
       # self.chara.card_no = card_no
        self.name.text = self.chara.name_txt()
        self.hpbar.max = self.chara.maxhp
        self.hpbar.now = self.chara.hp
        self.hpbar.text = f"HP:{self.chara.hp}/{self.chara.maxhp}"



    def hpbar_update(self, damage=0):
        # バー動作確認用の自傷ダメージ処理
        if self.chara.hp > damage > 0:
            self.chara.hp -= damage
            self.hpbar.text = f"HP:{self.chara.hp}/{self.chara.maxhp}"
        else:
            self.chara.hp = 0
            self.hpbar.text = f"HP:0/{self.chara.maxhp}"


class MSettingScreen(Screen):
    """メニューボタンを押すとメニューが開ける。
        下記にはkvファイルに登録した関数の処理を記述"""

    def __init__(self, **kw):
        super().__init__(**kw)

    def main_slide(self):
        self.parent.transition = WipeTransition()
        self.parent.current = "main_screen"


class BSettingScreen(Screen):
    """メニューボタンを押すとメニューが開ける。
        下記にはkvファイルに登録した関数の処理を記述"""

    def __init__(self, **kw):
        super().__init__(**kw)

    def main_slide(self):
        self.parent.transition = WipeTransition()
        self.parent.current = "battle_screen"


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


class HeroesField(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EnemiesField(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EmptySpace(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chara = Empty()


class PopupMenu(BoxLayout):
    popup_no = ObjectProperty(None)
    popup_yes = ObjectProperty(None)
