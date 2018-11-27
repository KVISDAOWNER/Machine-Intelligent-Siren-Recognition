import pandas as pd
import numpy as np
import sklearn.svm as svm
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import os
from PIL import Image
import specgram_maker as SM
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model
from sklearn import tree
import clip_split as ClipSplit
import pickle


def get_training_data(directory, max_freq=442, training=True, split=True, divisions=5, min_freq=14):
    _waves, time, labels = ClipSplit.extract(directory, max_freq, training, split, divisions=divisions,
                                             min_freq=min_freq)

    return _waves, labels


def _find_smallest_length(list):
    smallest_length = len(list[0])
    for i in range(len(list)):
        if len(list[i]) < smallest_length:
            smallest_length = len(list[i])
    return smallest_length


def cut(list):
    smallest_length = _find_smallest_length(list)
    result = []

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


if __name__ == "__main__":
    nb_model = GaussianNB()

    waves, labels = get_training_data("Wav\\", max_freq=40,
                                      training=True, split=True, min_freq=14, divisions=6)

    print("Begin cutting")
    waves = cut(waves)

    print("Begin fitting")
    nb_model.fit(waves, labels)

    print("Begin Get verify data")
    verify_data, actual_labels = get_training_data("C:\\Users\Magnus\\Desktop\\University\\5semester\\UCN\\",
                                                   max_freq=40, training=False, split=True, min_freq=14, divisions=6)

    print("Cut verify data")
    verify_data = cut_to_size(verify_data, _find_smallest_length(waves))

    predictions = nb_model.predict(verify_data)

    tp, fp, fn, tn = 0, 0, 0, 0
    for j in range(len(predictions)):
        answer, actual_value = predictions[j], actual_labels[j]
        if answer and actual_value:
            tp += 1
        elif answer and not actual_value:
            fp += 1
        elif not answer and actual_value:
            fn += 1
        else:
            tn += 1

    print("true positive", tp, "true negative", tn, "false positive", fp, "false negative", fn)

