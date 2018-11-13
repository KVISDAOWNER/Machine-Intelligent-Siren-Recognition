import pandas as pd
import numpy as np
import sklearn.svm as svm
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import os
from PIL import Image
import Regression as R
import specgram_maker as SM
import ClipSplit as ClipSplit

waves = []


def get_training_data(directory, max_freq=442):
    _waves, time, labels = ClipSplit.extract(directory, max_freq)

    return _waves, labels


def cut(list):
    smallest_length = len(list[0])
    result = []
    for i in range(len(list)):
        if len(list[i]) < smallest_length:
            smallest_length = len(list[i])

    for i in range(len(list)):
        ls = []
        for j in range(smallest_length):
            ls.append(list[i][j])
        result.append(ls)
    return result


def cut_to_size(list, length):
    result = []
    for i in range(len(list)):
        ls = []
        for j in range(length):
            ls.append(list[i][j])
        result.append(ls)
    return result


def get_verification_data(path):
    r = R.Regression()

    _waves, time = r.extract(path)
    return _waves


if __name__ == "__main__":
    #  waves, labels = get_training_data("C:\\Users\\Magnus\\Downloads\\BGNLessThanOrEq\\")
    waves, labels = get_training_data("Wav\\", 40)
    model = svm.SVC(kernel="linear")
    waves = cut(waves)

    model.fit(waves, labels)
    # accurately predict new data point
    verify_data = get_verification_data("C:\\Users\\Magnus\\Downloads\\TestSet5Seconds\\")

    verify_data = cut_to_size(verify_data, 291)

    predictions = model.predict(verify_data)
    print(predictions)