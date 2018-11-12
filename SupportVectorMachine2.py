import pandas as pd
import numpy as np
import sklearn.svm as svm
from sklearn.linear_model import LogisticRegression
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

    _waves, freq = r.extract(directory)
    for i in range(len(_waves)):
        if "siren" in os.listdir(directory)[i]:
            labels.append(True)
        else:
            labels.append(False)
    return _waves


def flatten_list(list_of_list):
    for i in range(len(list_of_list)):
        for j in range(len(list_of_list[i])):
            flat_waves.append(list_of_list[i][j])


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


def cut_to_size(input_list, size):
    list = []
    for i in range(size):
        list.append(input_list[i])
    return list


def verify_list(list):
    supposed_length = len(list[0])
    print("Length is supposed to be " + str(supposed_length))
    for i in range(len(list)):
        if len(list[i]) != supposed_length:
            print("list " + str(i) + " has " + str(len(list)) + " elements rather than " + str(supposed_length))
    return True


def get_data_from_file(path):
    r = R.Regression()
    data, freq = r.extract_single_file(path)
    return data[0]


if __name__ == "__main__":
    waves = get_training_data("C:\\Users\\Magnus\\Downloads\\TræningUnderLinjen\\")
    model = svm.SVC(kernel="linear")
    LR_model = LogisticRegression()

    # flatten_list(waves)
    # print(verify_list(flat_waves))

    waves = cut(waves)

    model.fit(waves, labels)
    LR_model.fit(waves, labels)
    # accurately predict new data point
    verify_data = get_training_data("Wav\\")

    predictions = model.predict(verify_data)
    print(predictions)
