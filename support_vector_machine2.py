import sklearn.svm as svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
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
    tree_model = tree.DecisionTreeClassifier()
    ran_model = RandomForestClassifier()
    svm_model = svm.SVC()
    lr_model = LogisticRegression()
    models = [[nb_model, "nb"], [tree_model, "tree"], [ran_model, "randomForest"], [svm_model, "svm"], [lr_model, "lr"]]

    waves, labels = get_training_data("C:\\Users\\kristoffer\\Desktop\\low_bgn_data\\", max_freq=1600,
                                     training=True, split=True, min_freq=700, divisions=6)

    print("Begin cutting")
    waves = cut(waves)

    print("Begin fitting")
    for i in range(len(models)):
        print("fitting", models[i][1])
        models[i][0].fit(waves, labels)
        pickle.dump(models[i][0], open("James" + models[i][1] + ".v.1.pkl", "wb"))

