import numpy as N
import matplotlib.pyplot as Plot
from scipy.io import wavfile as W
import specgram_maker as SM
import xlsxwriter as Xlsx
FREQUENCY_INTEVALS = 442
PATH = "C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\"
PATH2 = "C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Dataset\\NoSiren\\"


class Regression:

    #function for writing data to Xlsx document
    def filewrite(self, alist, t):

        RegressionWorkbook = Xlsx.Workbook("Datapointsfourth.xlsx")

        Worksheet = RegressionWorkbook.add_worksheet("Data for Regression")

        alistLength = len(alist)

        i = 0

        while(i < alistLength):
            Worksheet.write(i,1, alist[i])
            Worksheet.write(i, 0, t[i])
            i = i + 32

        RegressionWorkbook.close()

    #function for extracting relevant data from a list of wavfiles.
    def extract(self, files, filenames):

        columns = []
        FilesFrequenciesAr = []
        time = []
        sm = SM.SpecgramMaker()
        l=0
        for file in files:
            spec, freq, t = sm.get_specgram_data_from_wav(PATH, filenames[l])
            for i in range(len(spec[1])):
                MaxFrequencyValue = 0
                column = 0
                for j in range(FREQUENCY_INTEVALS):
                    if spec[j][i] > MaxFrequencyValue:
                        MaxFrequencyValue = spec[j][i]
                        column = j

            #A.append(H) not in use
                columns.append(50 * column)
            FilesFrequenciesAr.append(columns)
            columns.clear()
            time.append(t)

            l += 1
        return FilesFrequenciesAr, time





   # f = open("DataPoints.txt", "w+")

    #filewrite(colomns, t)

    """for i in range(len(t)):
        f.write(str(t[i]) + ", " + str(colomns[i]) + "\n")

    Plot.plot(t, colomns)
    Plot.show()"""



