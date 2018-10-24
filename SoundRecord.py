import sounddevice as sd
import wave


def rec(filename, duration, fs, channels, sampwidth):
    # Open/create the specified file in an overwrite mode
    wave_file = wave.open(filename, 'wb')
    wave_file.setframerate(fs)
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(sampwidth)

    # Actual recording, returns digital audio as an array of floats
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)

    # We synchonise to ensure that finish the recording before writing the array of floats
    sd.wait()

    # Actual file writing
    wave_file.writeframes(recording)
    wave_file.close()
