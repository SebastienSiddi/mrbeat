from array import array
from audiostream.sources.thread import ThreadSource


class AudioSourceTrack(ThreadSource):
    steps = ()
    step_nb_samples = 0
    buf = None

    def __init__(self, output_stream, wav_samples, bpm, sample_rate, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.current_sample_index = 0
        self.current_step_index = 0
        self.wav_samples = wav_samples
        self.nb_wav_samples = len(wav_samples)
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.compute_step_nb_sample_and_alloc_buffer()
        self.last_sound_sample_start_index = 0

    def set_steps(self, steps):
        if not len(steps) == len(self.steps):
            self.current_step_index = 0
        self.steps = steps

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.compute_step_nb_sample_and_alloc_buffer()

    def compute_step_nb_sample_and_alloc_buffer(self):
        if not self.bpm == 0:
            n = int(self.sample_rate * 15 / self.bpm)
            if not n == self.step_nb_samples:
                self.step_nb_samples = n
                self.buf = array("h", b"\x00\x00" * self.step_nb_samples)

    def no_steps_activated(self):
        if len(self.steps) == 0:
            return True
        for i in range(len(self.steps)):
            if self.steps[i] == 1:
                return False
        return True

    def get_bytes_array(self):
        for i in range(0, self.step_nb_samples):
            if len(self.steps) > 0 and not self.no_steps_activated():
                if self.steps[self.current_step_index] == 1 and i < self.nb_wav_samples:
                    # Jouer le son
                    self.buf[i] = self.wav_samples[i]
                    if i == 0:
                        self.last_sound_sample_start_index = self.current_sample_index
                else:
                    index = self.current_sample_index - self.last_sound_sample_start_index
                    if index < self.nb_wav_samples:
                        self.buf[i] = self.wav_samples[index]
                    else:
                        self.buf[i] = 0
            else:
                self.buf[i] = 0
            self.current_sample_index += 1

        self.current_step_index += 1
        if self.current_step_index >= len(self.steps):
            self.current_step_index = 0

        return self.buf

    def get_bytes(self, *args, **kwargs):
        return self.get_bytes_array().tobytes()