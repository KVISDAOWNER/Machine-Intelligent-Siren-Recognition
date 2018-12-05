import pyaudio
import numpy as np


# class used to record from the microphone by a given span.
class MicRecorder:
    # constructor, giving the required span time for each recording (input_length)
    def __init__(self, sample_length, formattype=pyaudio.paInt16, channels=1, rate=44100):
        self.formattype = formattype
        self.channels = channels
        self.rate = rate
        self.sample_length = sample_length
        self.input_frames_per_block = int(rate * self.sample_length)
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
        # read from the mic for input_frames_per_block amount of time.
        sound_info = stream.read(self.input_frames_per_block)

        # converting the data into an array.
        data = np.frombuffer(sound_info, dtype=np.int16)
        return data
