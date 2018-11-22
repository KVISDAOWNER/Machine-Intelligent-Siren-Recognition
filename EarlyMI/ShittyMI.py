from sklearn.linear_model import LogisticRegression
from scipy.io import wavfile
from EarlyMI import RegressionJacob as r
import os

CONST_CLIPSIZE = 150000  # shortest clip contains this number of samples
PATH = "C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\"
PATH2 = "C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\100to1\\"


# This function is for ensuring all the lists of wavfiles have the same number of samples.
def SetSize(files):
    # Getting the smallest number of samples in the folder
    Y = []
    # firstrun = True
    """for ls in files:
        if firstrun:
			#firstrun = False
			min = len(ls)

		if len(ls) < CONST_CLIPSIZE:  #This only works because i know the shortest clip is a sirene clip, soo, it's not good
			min = len(ls)"""

    for ls in files:
        Y.append(ls[:CONST_CLIPSIZE])  # copiest the first min characters

    return Y


def LoadFolder():
    directory = os.listdir(PATH2)
    Sirens = []
    Noises = []
    SirenFileName = []
    NoiseFileName = []

    for filename in directory:
        if filename.startswith("Siren"):
            arraydata, arrayfs = wavfile.read(PATH + filename)  # it's possible that this right here doesn't reset arrayfs
            Sirens.append(arrayfs.copy())
            SirenFileName.append(filename)
        else:
            arraydata, arrayfs = wavfile.read(PATH + filename)  # it's possible that this right here doesn't reset arrayfs
            Noises.append(arrayfs.copy())
            NoiseFileName.append(filename)

    Sirens = SetSize(Sirens)
    Noises = SetSize(Noises)
    return Sirens, Noises, SirenFileName, NoiseFileName

def TrainigSplit(SirenList, NoiseList):
    NumberOfSirens = len(SirenList)
    NumberOfNoises = len(NoiseList)

    X = []
    Y = []
    Z = []

    for i in range(NumberOfSirens-2):
        X.append(SirenList[i])
        Y.append(True)

    for j in range(NumberOfNoises - 5):
        X.append([NoiseList[j]])
        Y.append(False)

    Z.append(SirenList[NumberOfSirens-2:NumberOfSirens])
    Z.append(NoiseList[NumberOfNoises-5:NumberOfNoises])

    return X, Y, Z



if __name__ == "__main__":

    #Sirens, Noises, SirenFileName, NoiseFileName = LoadFolder()

    reg = r.Regression()

    FileData, DataTime = reg.extract(PATH2)
    FileDataLength = len(FileData)

    Y = []
    X = []
    Z = []

    for i in range(FileDataLength-10):

        X.append(FileData[i])

        if((i+1) % 100 == 0):
            Y.append(True)
        else:
            Y.append(False)

    Z = FileData[990:]

# Test
LR = LogisticRegression(solver='liblinear')
LR.fit(X, Y)
prediction = LR.predict(Z)
print(prediction)
