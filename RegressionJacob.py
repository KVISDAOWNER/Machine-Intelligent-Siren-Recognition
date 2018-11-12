import os
import specgram_maker
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
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

    def get_vector_between_two_points(self, p1, p2):
        print()


class Point:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init


if __name__ == "__main__":
    reg = Regression()
    f, t = reg.extract("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Dataset\\SirenClips\\test\\")
    # to plot the first call plt.plot(t[0],f[0]) and then plt.show()

    # so coloum 0 in spec are the frequencies in at the time given in t[0]
    # so if t[10] is equal to 100 milisec, then the frequencies in the
    # coloums of spec 0 to 10 are the frequencies for the first 100 miliseconds.

    vectors = []

    for i in range(0, len(f)):
        ff = f[i]
        ft = t[i]
        fPoints = []
        for j in range(0, len(ft)):
            fPoints.append(Point(ft[j], ff[j]))

        vectorsforfile = []

        for j in range(1, len(fPoints)):
            vectorsforfile.append([fPoints[j].x - fPoints[j-1].x, fPoints[j].y - fPoints[j-1].y])

        vectors.append(vectorsforfile)

    LR = LogisticRegression(solver='liblinear')

    X = [vectors[0], vectors[2]]
    Y = [False, True]
    Z = [vectors[1]]

    LR.fit(X, Y)
    Prediction = LR.predict(Z)
    print(Prediction)

    



