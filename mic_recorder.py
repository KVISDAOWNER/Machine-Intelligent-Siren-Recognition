import pyaudio
import numpy as np


class MicRecorder:
    def __init__(self, input_length, formattype=pyaudio.paInt16, channels=1, rate=44100):
        self.formattype = formattype
        self.channels = channels
        self.rate = rate
        self.input_length = input_length
        self.input_frames_per_block = int(rate * self.input_length)
        self.pa = pyaudio.PyAudio()

    def get_stream(self):
        stream = self.pa.open(format=self.formattype,
                              channels=self.channels,
                              rate=self.rate,
                              input=True,
                              frames_per_buffer=self.input_frames_per_block)
        return stream

    def get_data_from_mic(self, stream):
        sound_info = stream.read(self.input_frames_per_block)

        data = np.frombuffer(sound_info, dtype=np.int16)
        return data
