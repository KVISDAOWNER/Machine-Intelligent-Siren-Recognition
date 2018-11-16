import os
import specgram_maker
from sklearn.linear_model import LogisticRegression
FREQUENCY_INTEVALS = 442


class Point:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init


class Regression:

    # function for extracting relevant data from a list of wavfiles.
    # gets the y and x values for the higest pixels in each coloum.
    def extract(self, path):
        index_of_sirens = []
        index_of_not_sirens = []
        rows = []
        files_frequencies_ar = []
        time = []
        sm = specgram_maker.SpecgramMaker()

        directory = os.listdir(path)
        l = 0  # used to count the index of the files.
        for filename in directory:
            if not filename.endswith(".wav"):
                continue
            if filename.__contains__("siren"):
                index_of_sirens.append(l)
            else:
                index_of_not_sirens.append(l)

            spec, freq, t = sm.get_specgram_data_from_wav(path, filename)
            for i in range(len(spec[1])):  # iterating over coloums.
                max_frequency_value = 0
                row = 0
                for j in range(FREQUENCY_INTEVALS):  # Finding the row with highest frequency.
                    if spec[j][i] > max_frequency_value:
                        max_frequency_value = spec[j][i]
                        row = j
                rows.append(50 * row)
            files_frequencies_ar.append(rows.copy())
            rows.clear()
            time.append(t)
            l += 1
        return files_frequencies_ar, time, index_of_sirens, index_of_not_sirens

    # gets the vectors for the files represented by the f and t.
    def get_vectors_for_files(self, f, t):
        # each index is equal to the vectors for that file
        vectors = []

        # each index in f and t corresponds to all the points (t,f) for the wav-file.
        # i.e  f[0] and t[0] is all the y-values and all the x-values for that wav-file,
        # respectively.
        for i in range(0, len(f)):
            ff = f[i]
            ft = t[i]
            fPoints = []
            # represents them as points.
            for j in range(0, len(ft)):
                fPoints.append(Point(ft[j], ff[j]))

            # used to contain all the vectors for the given file
            vectorsforfile = []

            for j in range(1, len(fPoints)):
                # instead of representing a vector as a list of two elements,
                # we simply append each x and y value together
                # in that way, we remove one dimension from the final list.
                # so vectors[0] is a list of alle the x and y values for the vectors of the 0-file,
                # instead of vectors[0] being a list of vectors, where each vector is a list of 2 elements.
                vectorsforfile.append(fPoints[j].x - fPoints[j - 1].x)
                vectorsforfile.append(fPoints[j].y - fPoints[j - 1].y)

                # if it is wished to represent them as vectors use this.
                # vectorsforfile.append([fPoints[j].x - fPoints[j-1].x, fPoints[j].y - fPoints[j-1].y])

            # and add that to the overall list.
            # This makes it so each index in vectors is the vectors for a given file.
            vectors.append(vectorsforfile)
        return vectors

    def get_average_vectors_for_files_Xms(self, f, t, interval):
        # each index is equal to the vectors for that file
        vectors = []

        # each index in f and t corresponds to all the points (t,f) for the wav-file.
        # i.e  f[0] and t[0] is all the y-values and all the x-values for that wav-file,
        # respectively.
        for i in range(0, len(f)):
            ff = f[i]
            ft = t[i]
            fPoints = []
            # represents them as points.
            for j in range(0, len(ft)):
                fPoints.append(Point(ft[j], ff[j]))

            # used to contain all the vectors for the given file
            vectorsforfile = []

            # we start out by summing up x and y values until we hit the 0.1 mark
            margin = 0.1

            # used to contain all the different summed up X'es and Y'es
            his_sumX = []
            his_sumY = []
            sumX = 0
            sumY = 0

            i = 0 # we start with 0 summations
            for j in range(0, len(fPoints)):
                if ft[j] >= margin:  # if we with the mark
                    margin += interval / 1000  # we increase it by inteval/1000, so if 100ms it is 0.1
                    his_sumX.append(sumX/i)  # add the sumX and sumY to the history
                    his_sumY.append(sumY/i)
                    i=0 # then we restart
                    sumX = fPoints[j].x  # and start the new summations of X'es and Y'es
                    sumY = fPoints[j].y
                else:  # if we havent hit the mark, just keep adding.
                    sumX += fPoints[j].x
                    sumY += fPoints[j].y
                i += 1  # then we add one to the number of summations.

            # then we calculate the vectors X and Y values.
            for j in range(1, len(his_sumX)):
                # we take the X'es and Y'es in the 0.2 sec and
                # subtracts from the 0.1 sec X's and Y's
                vectorsforfile.append(his_sumX[j] - his_sumX[j - 1])
                vectorsforfile.append(his_sumY[j] - his_sumY[j - 1])
                # doing it this way makes it so the final list is 2D.

            # and add that to the overall list.
            # This makes it so each index in vectors is the vectors for a given file.
            # if there are 200 vectors in file 1 vectors[0] will contain 400 values,
            # since each vector is 2 numbers
            vectors.append(vectorsforfile)
        return vectors


    def get_vectors_for_files_Xms(self,f,t,interval):
        # each index is equal to the vectors for that file
        vectors = []

        # each index in f and t corresponds to all the points (t,f) for the wav-file.
        # i.e  f[0] and t[0] is all the y-values and all the x-values for that wav-file,
        # respectively.
        for i in range(0, len(f)):
            ff = f[i]
            ft = t[i]
            fPoints = []
            # represents them as points.
            for j in range(0, len(ft)):
                fPoints.append(Point(ft[j], ff[j]))

            # used to contain all the vectors for the given file
            vectorsforfile = []

            # we start out by summing up x and y values until we hit the 0.1 mark
            margin = 0.1

            # used to contain all the different summed up X'es and Y'es
            his_sum_x = []
            his_sum_y = []
            sum_x = 0
            sum_y = 0
            for j in range(0, len(fPoints)):
                if ft[j] >= margin:  # if we with the mark
                    margin += interval/1000  # we increase it by inteval/1000, so if 100ms it is 0.1
                    his_sum_x.append(sum_x)  # add the sum_x and sum_y to the history
                    his_sum_y.append(sum_y)
                    sum_x = fPoints[j].x  # and start the new summations of X'es and Y'es
                    sum_y = fPoints[j].y
                else:  # if we havent hit the mark, just keep adding.
                    sum_x += fPoints[j].x
                    sum_y += fPoints[j].y

            # then we calculate the vectors X and Y values.
            for j in range(1, len(his_sum_x)):
                # we take the X'es and Y'es in the 0.2 sec and
                # subtracts from the 0.1 sec X's and Y's
                vectorsforfile.append(his_sum_x[j] - his_sum_x[j-1])
                vectorsforfile.append(his_sum_y[j] - his_sum_y[j-1])
                # doing it this way makes it so the final list is 2D.

            # and add that to the overall list.
            # This makes it so each index in vectors is the vectors for a given file.
            # if there are 200 vectors in file 1 vectors[0] will contain 400 values,
            # since each vector is 2 numbers
            vectors.append(vectorsforfile)
        return vectors

    # this is the main Jacob had before committing.
    def fit_and_predict_with_vectors(self):
        # Extracting training files
        f, t, index_of_sirens, index_of_not_sirens = self.extract("C:\\Users\\Jacob\\Music\\100til1\\")
        number_of_files = len(f)
        # to plot the first call plt.plot(t[0],f[0]) and then plt.show()

        # so coloum 0 in spec are the frequencies in at the time given in t[0]
        # so if t[10] is equal to 100 milisec, then the frequencies in the
        # coloums of spec 0 to 10 are the frequencies for the first 100 miliseconds.

        LR = LogisticRegression(solver='liblinear')

        X = []
        Y = []
        Z = []

        # Calculating vectors for training files
        vectors = self.get_average_vectors_for_files_Xms(f, t, 200)

        # Appending the vectors with sirens to X
        for i in index_of_sirens:
            X.append(vectors[i])
            Y.append(True)

        # Appending the vectors without sirens to X
        for i in index_of_not_sirens:
            X.append(vectors[i])
            Y.append(False)

        # Extracting test files
        f, t, index_of_sirens, index_of_not_sirens = self.extract("C:\\Users\\Jacob\\Music\\Teest\\")

        # Calculating vectors for test files
        vectors = self.get_average_vectors_for_files_Xms(f, t, 200)

        # Appending vectors to Z
        for i in range(0, len(vectors)):
            Z.append(vectors[i])

        # Fitting
        LR.fit(X, Y)

        # Predicting
        prediction = LR.predict(Z)
        print(prediction)


if __name__ == "__main__":
    reg = Regression()
    f, t, index_of_sirens, index_without_sirens = reg.extract("C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Dataset\\SirenClips\\test\\")
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
            vectorsforfile.append([fPoints[j].x - fPoints[j - 1].x, fPoints[j].y - fPoints[j - 1].y])

        vectors.append(vectorsforfile)

    LR = LogisticRegression(solver='liblinear')

    X = [vectors[0], vectors[2]]
    Y = [False, True]
    Z = [vectors[1]]

    LR.fit(X, Y)
    Prediction = LR.predict(Z)
    print(Prediction)




