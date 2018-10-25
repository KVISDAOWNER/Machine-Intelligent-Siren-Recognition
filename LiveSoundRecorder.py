import SoundRecord as sr
import os


# Class containing info on sample duration, frame rate,
class RecordSpecs:
    def __init__(self, sample_secs=1, fs=44100, channels=1, samp_width=4):
        self.sample_secs = sample_secs
        self.fs = fs
        self.ch = channels
        self.sw = samp_width


# Records and saves the samples in a queue like folder, deleting oldest sample before reaching the samples_kept
def live_audio_rec(dir, samples_kept, r_spec):
    for i in range (0, samples_kept):
        sr.rec(dir +"sample" + str(i) +".wav", r_spec.sample_secs, r_spec.fs, r_spec.ch, r_spec.sw)
    while True:
        os.remove(dir+"sample0.wav")
        for j in range (0, samples_kept-1):
            os.rename(dir+"sample"+str(j+1)+".wav", dir+"sample"+str(j)+".wav")
        sr.rec(dir +"sample" + str(samples_kept-1) +".wav", r_spec.sample_secs, r_spec.fs, r_spec.ch, r_spec.sw)


if __name__ == '__main__':
    record_specs = RecordSpecs()
    live_audio_rec('LiveSamples/', 4, record_specs)
