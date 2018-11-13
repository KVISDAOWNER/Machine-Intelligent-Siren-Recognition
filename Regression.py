import os
import specgram_maker
import matplotlib.pyplot as plt
FREQUENCY_INTEVALS = 442


class Regression:

    # function for extracting relevant data from a list of wavfiles.
    def extract(self, path):
        labels = []
        rows = []
        FilesFrequenciesAr = []
        time = []
        sm = specgram_maker.SpecgramMaker()

        directory = os.listdir(path)
        for filename in directory:
            if not filename.endswith(".wav"):
                continue

            if "SPCSiren" in filename or "siren" in filename or "sirenAt" in filename:
                labels.append(True)
            else:
                labels.append(False)

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
            print("Done importing " + filename + ".", labels[len(time) - 1], str(len(time) * 100 / len(directory)) + " %")
        return FilesFrequenciesAr, time


    def extract_single_file(self, filename):
        sm = specgram_maker.SpecgramMaker()
        rows = []
        FilesFrequenciesAr = []
        time = []
        spec, freq, t = sm.get_specgram_data_from_wav("", filename)
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
    f, t = reg.extract("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\SirenClips\\")
    for x in range(0, len(t)):
        plt.plot(t[x], f[x])
        plt.show()
        a = input()
