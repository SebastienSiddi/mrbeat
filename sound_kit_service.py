

class Sound:
    def __init__(self, filename, displayname):
        self.filename = filename
        self.displayname = displayname


class SoundKit:
    sounds = ()

    def get_nb_tracks(self):
        return len(self.sounds)


class SoundKit1(SoundKit):
    sounds = (Sound("sounds/kit1/kick.wav", "KICK"),
              Sound("sounds/kit1/clap.wav", "CLAP"),
              Sound("sounds/kit1/shaker.wav", "SHAKER"),
              Sound("sounds/kit1/snare.wav", "SNARE"))


class SoundKitService:
    soundkit = SoundKit1()

    def get_nb_tracks(self):
        return self.soundkit.get_nb_tracks()

    def get_sound_at(self, index):
        if index >= len(self.soundkit.sounds):
            return None
        return self.soundkit.sounds[index]
