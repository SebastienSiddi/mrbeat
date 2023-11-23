from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton


class TrackStepButton(ToggleButton):
    pass


class TrackSoundButton(Button):
    pass


class TrackWidget(BoxLayout):
    def __init__(self, sound, audio_engine, nb_steps, track_source, steps_left_align, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)
        sound_button = TrackSoundButton()
        sound_button.text = sound.displayname
        sound_button.width = steps_left_align
        sound_button.on_press = self.on_sound_button_press
        self.add_widget(sound_button)
        self.audio_engine = audio_engine
        self.sound = sound
        self.track_source = track_source
        self.step_buttons = []
        self.nb_steps = nb_steps

        for i in range(0, nb_steps):
            step_button = TrackStepButton()
            step_button.bind(state=self.on_step_button_state)
            self.step_buttons.append(step_button)
            self.add_widget(step_button)

    def on_sound_button_press(self):
        self.audio_engine.play_sound(self.sound.samples)

    def on_step_button_state(self, widget, value):
        steps = []
        for i in range(0, self.nb_steps):
            if self.step_buttons[i].state == "down":
                steps.append(1)
            else:
                steps.append(0)
        self.track_source.set_steps(steps)
