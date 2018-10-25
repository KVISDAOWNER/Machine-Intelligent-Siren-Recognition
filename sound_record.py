import sounddevice as sd
import wave


# Records sound from mic, with the specifications given in parameters, and saves to wav type file
def rec(filename, duration, fs, channels, samp_width):
    # Open/create the specified file in an overwrite mode
    wave_file = wave.open(filename, 'wb')
    wave_file.setframerate(fs)
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(samp_width)

    # Actual recording, returns digital audio as an array of floats
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)

    # We synchronise to ensure that finish the recording before writing the array of floats
    sd.wait()

    # Actual file writing
    wave_file.writeframes(recording)
    wave_file.close()
