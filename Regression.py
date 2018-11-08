import os
import specgram_maker
import matplotlib.pyplot as plt
FREQUENCY_INTEVALS = 442


class Regression:

    # function for extracting relevant data from a list of wavfiles.
    def extract(self, path):

        rows = []
        FilesFrequenciesAr = []
        time = []
        sm = specgram_maker.SpecgramMaker()

        directory = os.listdir(path)
        for filename in directory:
            if not filename.endswith(".wav"):
                continue
            spec, freq, t = sm.get_specgram_data_from_wav(path, filename)
            for i in range(len(spec[1])):  # iterating over coloums.
                MaxFrequencyValue = 0
                row = 0
                for j in range(FREQUENCY_INTEVALS):  # Finding the row with highest frequency.
                    if spec[j][i] > MaxFrequencyValue:
                        MaxFrequencyValue = spec[j][i]
                        row = j
                rows.append(50 * row)
            FilesFrequenciesAr.append(rows.copy())
            rows.clear()
            time.append(t)

        return FilesFrequenciesAr, time


if __name__ == "__main__":
    reg = Regression()
    f, t = reg.extract("C:\\Users\\Jacob\\Music\\Samples\\Comp5\\")
    for x in range(0, len(t)):
        plt.plot(t[x],f[x])
        plt.show()
        a = input()
