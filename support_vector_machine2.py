import pandas as pd
import numpy as np
import sklearn.svm as svm
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import os
from PIL import Image
import regression as R
import specgram_maker as SM
import ClipSplit as ClipSplit
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model
import clip_split as ClipSplit

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


def get_verification_data(path, max_freq=442):
    r = R.Regression()

    _waves, time = r.extract(path, max_freq)
    return _waves


if __name__ == "__main__":
    #  waves, labels = get_training_data("C:\\Users\\Magnus\\Downloads\\BGNLessThanOrEq\\")
    waves, labels = get_training_data("C:\\Users\\Magnus\\Desktop\\University\\5semester\\FirstHalf\\", 40)
    svm_model = svm.SVC(kernel="linear")
    bayes_model = linear_model.BayesianRidge()
    nb_model = GaussianNB()
    lr_model = LogisticRegression()

    print("Begin cutting")
    waves = cut(waves)

    print("Begin fitting")
    print("nb")
    nb_model.fit(waves, labels)
    # print("svm")
    # svm_model.fit(waves, labels)
    print("lr")
    lr_model.fit(waves, labels)
    print("bayes")
    bayes_model.fit(waves, labels)

    verify_data, actual_labels = get_training_data("C:\\Users\\Magnus\\Desktop\\University\\5semester\\SecondHalf\\",
                                                   max_freq=40)

    print("Cut verify data")
    verify_data = cut_to_size(verify_data, 291)

    print("begin get predictions", "svm")
    # svm_predictions = svm_model.predict(verify_data)
    # print("nb")
    nb_predictions = nb_model.predict(verify_data)
    print("lr")
    lr_predictions = lr_model.predict(verify_data)
    print("bayes")
    bayes_predictions = bayes_model.predict(verify_data)

    svm_correct, nb_correct, lr_correct, samples, bayes_correct = 0, 0, 0, 0, 0

    print("begin calculate accuracy")
    for i in range(len(lr_predictions)):
        # print("SVM:", svm_predictions[i], "NB:", nb_predictions[i], "LR:", lr_predictions[i],
        # "actual value:", actual_labels[i])
        # if svm_predictions[i] == actual_labels[i]:
        #    svm_correct += 1
        if nb_predictions[i] == actual_labels[i]:
            nb_correct += 1
        if lr_predictions[i] == actual_labels[i]:
            lr_correct += 1
        if bayes_predictions[i] == actual_labels[i]:
            bayes_correct += 1
        samples += 1

    # print("svm accuracy:", 100 * svm_correct / samples)
    print("NB accuracy:", 100 * nb_correct / samples)
    print("LR accuracy:", 100 * lr_correct / samples)
    print("Bayes accuracy", 100 * bayes_correct / samples)
