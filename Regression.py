import numpy as N
import matplotlib.pyplot as Plot
from scipy import optimize
import specgram_maker as SM
# nu ændret
columns = []


def test_func(x, a, b, c, d):
    return a * N.cos(b * x + c) + d


def write_out(array, comma=False):
    f = open("DataPoints.txt", "w+")
    for i in range(len(array)):
        if comma:
            s = str(array[i]).split('.')[0] + ',' + str(array[i]).split('.')[1]
        else:
            s = str(array[i])
        f.write(s + "\n")


if __name__ == "__main__":
    sm = SM.SpecgramMaker()

    spec, freq, t = sm.get_specgram_data_from_wav("Wav\\", "Sirene23.wav")

    for i in range(int(len(spec[1]))):
        H = 0
        column = 0
        for j in range(442):
            if spec[j][i] > H:
                H = spec[j][i]
                column = j
        columns.append(50 * column)

    write_out(columns)
    write_out(t)



