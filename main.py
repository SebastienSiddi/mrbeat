from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout

from audio_engine import AudioEngine
from sound_kit_service import SoundKitService
from track import TrackWidget

Builder.load_file("track.kv")


class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.sound_kit_service = SoundKitService()

        # kick_sound = self.sound_kit_service.get_sound_at(0)

        self.audio_engine = AudioEngine()
        # self.audio_engine.play_sound(kick_sound.samples)

    def on_parent(self, widget, parent):
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound = self.sound_kit_service.get_sound_at(i)
            self.tracks_layout.add_widget(TrackWidget(sound, self.audio_engine))


class MrBeatApp(App):
    pass


MrBeatApp().run()
