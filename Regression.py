import numpy as N
import matplotlib.pyplot as Plot
from scipy.io import wavfile as W
import specgram_maker as SM

A = []
colomns = []

if __name__ == "__main__":
    sm = SM.SpecgramMaker()

    spec, freq, t = sm.get_specgram_data_from_wav("Wav\\", "Sirene23-Edited.wav")

    for i in range(len(spec[1])):
        H = 0
        column = 0
        for j in range(442):
            if spec[j][i] > H:
                H = spec[j][i]
                column = j

        A.append(H)
        colomns.append(50 * column)

    f = open("DataPoints.txt", "w+")

    for i in range(len(t)):
        f.write(str(t[i]) + ", " + str(colomns[i]) + "\n")

    Plot.plot(t, colomns)
    Plot.show()



