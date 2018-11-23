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

    waves, labels = get_training_data("C:\\Users\\Magnus\\Desktop\\University\\5semester\\FirstHalf\\", max_freq=40,
                                      training=True, split=True, min_freq=14)
    lr_model = LogisticRegression()
    tree_model = tree.DecisionTreeClassifier()

    print("Begin cutting")
    waves = cut(waves)

    print("Begin fitting")
    lr_model.fit(waves, labels)
    tree_model.fit(waves, labels)

    # pickle.dump(lr_model, open("mi_files\\James.pkl", "wb"))

    # lr_model = pickle.load(open("mi_files\\James.pkl", "rb"))

    verify_data, actual_labels = get_training_data("C:\\Users\\Magnus\\Desktop\\University\\5semester\\RealLife\\",
                                                   max_freq=40, training=False, split=True, min_freq=14)

    print("Cut verify data")
    verify_data = cut_to_size(verify_data, _find_smallest_length(verify_data))

    lr_predictions = lr_model.predict(verify_data)
    tree_predictions = tree_model.predict(verify_data)

    true_positive, false_positive, true_negative, false_negative = 0, 0, 0, 0

    print("begin calculate accuracy", "lr")
    for i in range(len(lr_predictions)):
        if lr_predictions[i] and actual_labels[i]:
            true_positive += 1
        elif lr_predictions[i] and not actual_labels[i]:
            false_positive += 1
        elif not lr_predictions[i] and actual_labels[i]:
            false_negative += 1
        else:
            true_negative += 1

    print("true positive", true_positive, "true negative", true_negative, "false positive", false_positive,
          "false negative", false_negative)

    true_positive, false_positive, true_negative, false_negative = 0, 0, 0, 0
    
    print("tree")
    for i in range(len(tree_predictions)):
        if tree_predictions[i] and actual_labels[i]:
            true_positive += 1
        elif tree_predictions[i] and not actual_labels[i]:
            false_positive += 1
        elif not tree_predictions[i] and actual_labels[i]:
            false_negative += 1
        else:
            true_negative += 1
    print("true positive", true_positive, "true negative", true_negative, "false positive", false_positive,
          "false negative", false_negative)


