from sklearn.linear_model import LogisticRegression
from scipy.io import wavfile
import Regression as r
import os
from numpy import fft

import numpy as np

CONST_CLIPSIZE = 150000  # shortest clip contains this number of samples
PATH = "C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Lydeksempler\\"
PATH2 = "C:\\Users\\Bjarke\\Desktop\\Universitet\\5.semester\\Dataset\\NoSiren\\"


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
    directory = os.listdir(PATH)
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


Sirens, Noises, SirenFileName, NoiseFileName = LoadFolder()

reg = r.Regression()

SirensData, SirensTime = reg.extract(Sirens,SirenFileName)
NoisesData, NoisesTime = reg.extract(Noises,NoiseFileName)


NumberOfSirens = len(SirensData)
NumberOfNoises = len(NoisesData)

X = NoisesData[:2]  #
Y = []
Z = []

for element in X:
    Y.append(False)



for i in range(NumberOfSirens-10):
    X.append(SirensData[i])
    Y.append(True)


# Test
Z.append(NoisesData[2])
Z.append(SirensData[NumberOfSirens-10:])

LR = LogisticRegression(solver='liblinear')
LR.fit(X, Y)
prediction = LR.predict(Z)
print(prediction)
