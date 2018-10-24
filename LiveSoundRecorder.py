import SoundRecord as sr
import os


# Records and saves the samples in a stack like folder, deleting oldest sample before reaching the samples_kept
def live_audio_rec(dir, samples_kept, sample_size):
    for i in range (0, samples_kept):
        sr.rec(dir + "sample" + str(i) + ".wav", sample_size, 44100, 1, 4)
    while True:
        os.remove(dir + "sample0.wav")
        for j in range (0, samples_kept-1):
            print(dir + "sample" + str(j+1) + ".wav ->" + dir + "sample" + str(j) + ".wav")
            os.rename(dir + "sample" + str(j+1) + ".wav", dir + "sample" + str(j) + ".wav")
        print(dir + "sample" + str(samples_kept) + ".wav")
        sr.rec(dir + "sample" + str(samples_kept-1) + ".wav", sample_size, 44100, 1, 4)


if __name__ == '__main__':
    live_audio_rec('LiveSamples/', 4, 1)
