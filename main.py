from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

Builder.load_file("track.kv")


class MainWidget(RelativeLayout):
    pass


class MrBeatApp(App):
    pass


MrBeatApp().run()