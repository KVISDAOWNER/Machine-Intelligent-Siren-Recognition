import sys
import sklearn.svm as svmm
import os
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle
from support_vector_machine2 import cut, get_training_data, cut_to_size, _find_smallest_length


def printing_confusing_matrix_of_models(split=True):
    nb_model = GaussianNB()
    waves, labels = get_training_data("Wav\\", max_freq=40,
                                      training=True, split=split, min_freq=14, divisions=6)
    print("Begin cutting")
    waves = cut(waves)

    nb_model.fit(waves, labels)

    print("Begin Get verify data")
    verify_data, actual_labels = get_training_data("Wav\\",
                                                   max_freq=40, training=False, split=split, min_freq=14, divisions=6)
    print("Cut verify data")
    verify_data = cut_to_size(verify_data, _find_smallest_length(waves))

    print("predicting")
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
    print("Confusing Matrix for: Naive Bayes: ")
    print("true positive", tp, "true negative", tn, "false positive", fp, "false negative", fn)


def printing_size_of_models_with_split():
    print("SPLITTING")
    gau_model = GaussianNB()
    svm_model = svmm.SVC()
    ran_model = RandomForestClassifier()
    lr_model = LogisticRegression()
    tree_model = DecisionTreeClassifier()
    waves, labels = get_training_data("C:\\Users\\Jacob\\Desktop\\MIData\\training_data\\", max_freq=40,
                                      training=True, split=True, min_freq=14, divisions=6)

    print("Begin cutting")
    waves = cut(waves)

    print("Begin fitting")
    gau_model.fit(waves, labels)
    print("Gau done")
    svm_model.fit(waves, labels)
    print("svm done")
    ran_model.fit(waves, labels)
    print("ran done")
    lr_model.fit(waves, labels)
    print("lr done")
    tree_model.fit(waves, labels)
    print("tree done")

    # https://stackoverflow.com/questions/45601897/how-to-calculate-the-actual-size-of-a-fit-trained-model-in-sklearn
    gau = pickle.dumps(gau_model)
    svm = pickle.dumps(svm_model)
    ran = pickle.dumps(ran_model)
    lr = pickle.dumps(lr_model)
    tree = pickle.dumps(tree_model)

    gau_size = sys.getsizeof(gau)
    svm_size = sys.getsizeof(svm)
    ran_size = sys.getsizeof(ran)
    lr_size = sys.getsizeof(lr)
    tree_size = sys.getsizeof(tree)
    print(
        "In terms of pickle.dumps\n The size of: \n" + "gau: " + str(gau_size) + "\n" + "svm: " + str(svm_size) + "\n" +
        "ran: " + str(ran_size) + "\n" + "lr: " + str(lr_size) + "\n" + "tree: " + str(tree_size)
        + "\n\n")

    # https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python
    from pympler import asizeof
    gau_size = asizeof.asizeof(gau_model)
    svm_size = asizeof.asizeof(svm_model)
    ran_size = asizeof.asizeof(ran_model)
    lr_size = asizeof.asizeof(lr_model)
    tree_size = asizeof.asizeof(tree_model)
    print("In terms of Pympler \n The size of: \n" + "gau: " + str(gau_size) + "\n" + "svm: " + str(svm_size) + "\n" +
          "ran: " + str(ran_size) + "\n" + "lr: " + str(lr_size) + "\n" + "tree: " + str(tree_size)
          + "\n\n")

    # https://stackoverflow.com/questions/2104080/how-to-check-file-size-in-python
    pickle.dump(gau_model, open("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\SplittedModels\\JamesGAU.pkl", "wb"))
    pickle.dump(svm_model, open("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\SplittedModels\\JamesSVM.pkl", "wb"))
    pickle.dump(ran_model, open("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\SplittedModels\\JamesRAN.pkl", "wb"))
    pickle.dump(lr_model, open("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\SplittedModels\\JamesLR.pkl", "wb"))
    pickle.dump(tree_model, open("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\SplittedModels\\JamesTREE.pkl", "wb"))

    gau_size = os.path.getsize("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\SplittedModels\\JamesGAU.pkl")
    svm_size = os.path.getsize("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\SplittedModels\\JamesSVM.pkl")
    ran_size = os.path.getsize("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\SplittedModels\\JamesRAN.pkl")
    lr_size = os.path.getsize("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\SplittedModels\\JamesLR.pkl")
    tree_size = os.path.getsize("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\SplittedModels\\JamesTREE.pkl")
    print("In terms of pickle.dump file sizes\n The size of: \n" + "gau: " + str(gau_size) + "\n" + "svm: " + str(
        svm_size) + "\n" +
          "ran: " + str(ran_size) + "\n" + "lr: " + str(lr_size) + "\n" + "tree: " + str(tree_size)
          + "\n")


def printing_size_of_models_with_nosplit():
    print("NO SPLITTING")
    gau_model = GaussianNB()
    svm_model = svmm.SVC()
    ran_model = RandomForestClassifier()
    lr_model = LogisticRegression()
    tree_model = DecisionTreeClassifier()
    waves, labels = get_training_data("C:\\Users\\Jacob\\Desktop\\MIData\\training_data\\", max_freq=40,
                                      training=True, split=False, min_freq=14, divisions=6)

    print("Begin cutting")
    waves = cut(waves)

    print("Begin fitting")
    gau_model.fit(waves, labels)
    print("Gau done")
    svm_model.fit(waves, labels)
    print("svm done")
    ran_model.fit(waves, labels)
    print("ran done")
    lr_model.fit(waves, labels)
    print("lr done")
    tree_model.fit(waves, labels)
    print("tree done")

    # https://stackoverflow.com/questions/45601897/how-to-calculate-the-actual-size-of-a-fit-trained-model-in-sklearn
    gau = pickle.dumps(gau_model)
    svm = pickle.dumps(svm_model)
    ran = pickle.dumps(ran_model)
    lr = pickle.dumps(lr_model)
    tree = pickle.dumps(tree_model)

    gau_size = sys.getsizeof(gau)
    svm_size = sys.getsizeof(svm)
    ran_size = sys.getsizeof(ran)
    lr_size = sys.getsizeof(lr)
    tree_size = sys.getsizeof(tree)
    print(
        "In terms of pickle.dumps\n The size of: \n" + "gau: " + str(gau_size) + "\n" + "svm: " + str(svm_size) + "\n" +
        "ran: " + str(ran_size) + "\n" + "lr: " + str(lr_size) + "\n" + "tree: " + str(tree_size)
        + "\n\n")

    # https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python
    from pympler import asizeof
    gau_size = asizeof.asizeof(gau_model)
    svm_size = asizeof.asizeof(svm_model)
    ran_size = asizeof.asizeof(ran_model)
    lr_size = asizeof.asizeof(lr_model)
    tree_size = asizeof.asizeof(tree_model)
    print("In terms of Pympler \n The size of: \n" + "gau: " + str(gau_size) + "\n" + "svm: " + str(svm_size) + "\n" +
          "ran: " + str(ran_size) + "\n" + "lr: " + str(lr_size) + "\n" + "tree: " + str(tree_size)
          + "\n\n")

    # https://stackoverflow.com/questions/2104080/how-to-check-file-size-in-python
    pickle.dump(gau_model, open("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\NonSplittedModels\\JamesGAU.pkl", "wb"))
    pickle.dump(svm_model, open("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\NonSplittedModels\\JamesSVM.pkl", "wb"))
    pickle.dump(ran_model, open("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\NonSplittedModels\\JamesRAN.pkl", "wb"))
    pickle.dump(lr_model, open("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\NonSplittedModels\\JamesLR.pkl", "wb"))
    pickle.dump(tree_model, open("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\NonSplittedModels\\JamesTREE.pkl", "wb"))

    gau_size = os.path.getsize("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\NonSplittedModels\\JamesGAU.pkl")
    svm_size = os.path.getsize("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\NonSplittedModels\\JamesSVM.pkl")
    ran_size = os.path.getsize("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\NonSplittedModels\\JamesRAN.pkl")
    lr_size = os.path.getsize("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\NonSplittedModels\\JamesLR.pkl")
    tree_size = os.path.getsize("C:\\Users\\Jacob\\Desktop\\MIData\\mi_pickle\\NonSplittedModels\\JamesTREE.pkl")
    print("In terms of pickle.dump file sizes\n The size of: \n" + "gau: " + str(gau_size) + "\n" + "svm: " + str(
        svm_size) + "\n" +
          "ran: " + str(ran_size) + "\n" + "lr: " + str(lr_size) + "\n" + "tree: " + str(tree_size)
          + "\n")


if __name__ == "__main__":
    printing_confusing_matrix_of_models(split=True)
