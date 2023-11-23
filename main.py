from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty, Clock
from kivy.uix.relativelayout import RelativeLayout
from audio_engine import AudioEngine
from sound_kit_service import SoundKitService
from track import TrackWidget

Builder.load_file("track.kv")
Builder.load_file("play_indicator.kv")

TRACK_NB_STEPS = 16
TRACKS_STEPS_LEFT_ALIGN = dp(100)


class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()
    play_indicator_widget= ObjectProperty()
    TRACKS_STEPS_LEFT_ALIGN = NumericProperty(dp(100))
    step_index = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.sound_kit_service = SoundKitService()
        self.audio_engine = AudioEngine()

        self.mixer = self.audio_engine.create_mixer(self.sound_kit_service.soundkit.get_all_samples(), 120, TRACK_NB_STEPS, self.on_mixer_current_step_changed)

    def on_parent(self, widget, parent):
        self.play_indicator_widget.set_nb_steps(TRACK_NB_STEPS)
        # self.play_indicator_widget.set_current_step_index(1)
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound = self.sound_kit_service.get_sound_at(i)
            self.tracks_layout.add_widget(TrackWidget(sound, self.audio_engine, TRACK_NB_STEPS, self.mixer.tracks[i], self.TRACKS_STEPS_LEFT_ALIGN))

    def on_mixer_current_step_changed(self, step_index):
        self.step_index = step_index
        Clock.schedule_once(self.update_play_indicator_cbk, 0)

    def update_play_indicator_cbk(self, dt):
        if self.play_indicator_widget is not None:
            self.play_indicator_widget.set_current_step_index(self.step_index)


class MrBeatApp(App):
    pass


MrBeatApp().run()
