import pandas as pd
import numpy as np
import sklearn.svm as svm
import matplotlib.pyplot as plt
import os
from PIL import Image
import Regression as R
import specgram_maker as SM

waves = []
labels = []
flat_waves = []


def get_training_data(directory):
    sm = SM.SpecgramMaker()
    r = R.Regression()

    for filename in os.listdir(directory):
        if filename == "Sirene21.wav":
            labels.append(True)
            sp, freq, t = sm.get_specgram_data_from_wav(directory, filename)

            waves.append(sp)
            print("Done importing from " + filename)


def flatten_list(listlist):
    for i in range(len(listlist)):
        for j in range(len(listlist[i])):
            flat_waves.append(listlist[i][j])


def verify_list(list):
    supposed_length = len(list[0])
    print("Length is supposed to be " + str(supposed_length))
    for i in range(len(list)):
        if len(list[i]) != supposed_length:
            print("list " + str(i) + " has " + str(len(list)) + " elements rather than " + str(supposed_length))
    return True


if __name__ == "__main__":
    get_training_data("Wav\\")
    model = svm.SVC(kernel="linear")
    # flatten_list(waves)
    # print(verify_list(flat_waves))
    model.fit(waves, labels)
    # accurately predict new data point
    print("Done!")
