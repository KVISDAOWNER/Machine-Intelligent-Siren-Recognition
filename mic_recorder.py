import pyaudio
import numpy as np


# class used to record from the microphone by a given span.
class MicRecorder:
    # constructor, giving the required span time for each recording (input_length)
    def __init__(self, input_length, formattype=pyaudio.paInt16, channels=1, rate=44100):
        self.formattype = formattype
        self.channels = channels
        self.rate = rate
        self.input_length = input_length
        self.input_frames_per_block = int(rate * self.input_length)
        self.pa = pyaudio.PyAudio()

    # used to get the stream for recording from the mic.
    # callers responsibility to close the stream again.
    def get_stream(self):
        stream = self.pa.open(format=self.formattype,
                              channels=self.channels,
                              rate=self.rate,
                              input=True,
                              frames_per_buffer=self.input_frames_per_block)
        return stream

    # getting the data for the recorded time span.
    def get_data_from_mic(self, stream):
        sound_info = stream.read(self.input_frames_per_block)

        data = np.frombuffer(sound_info, dtype=np.int16)
        return data
