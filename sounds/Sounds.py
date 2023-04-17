from pygame import mixer


class Sounds:
    def __init__(self):
        mixer.init()

    def se_play(self, se_select=None, play_spd=1):
        mixer.music.load("sounds/"+se_select)
        mixer.music.play(play_spd)
