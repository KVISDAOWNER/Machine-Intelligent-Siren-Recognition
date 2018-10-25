import sound_record as sr
import os


# Class containing info on sample duration, frame rate,
class RecordSpecs:
    def __init__(self, sample_secs=1, fs=44100, channels=1, sample_width=4):
        self.sample_secs = sample_secs
        self.fs = fs
        self.ch = channels
        self.sw = sample_width


# Records and saves the samples in a queue like folder, deleting oldest sample before reaching the samples_kept
def live_audio_rec(dir, samples_kept, r_spec):
    basename = "sample"
    file_type =".wav"
    for i in range(0, samples_kept):
        sr.rec(dir + basename + str(i)+file_type, r_spec.sample_secs, r_spec.fs, r_spec.ch, r_spec.sw)
    while True:
        os.remove(dir + basename + "0" + file_type)
        for j in range(0, samples_kept-1):
            os.rename(dir + basename + str(j+1) + file_type, dir + basename + str(j) + file_type)
        sr.rec(dir + basename + str(samples_kept-1) + file_type, r_spec.sample_secs, r_spec.fs, r_spec.ch, r_spec.sw)


if __name__ == '__main__':
    record_specs = RecordSpecs()
    live_audio_rec('LiveSamples/', 4, record_specs)
