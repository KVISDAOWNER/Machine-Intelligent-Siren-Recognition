import sklearn.svm as svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import clip_split as ClipSplit
import pickle


def get_training_data(training_directory, testing_directory, max_freq=2000, split=True, divisions=5, min_freq=750):
    training_waves, training_time, training_labels, testing_waves, testing_time, testing_labels = ClipSplit.extract(
        training_directory, testing_directory, max_freq=max_freq, min_freq=min_freq, divisions=divisions, split=split)

    return training_waves, training_labels, testing_waves, testing_labels


if __name__ == "__main__":
    nb_model = GaussianNB()
    tree_model = tree.DecisionTreeClassifier()
    ran_model = RandomForestClassifier()
    svm_model = svm.SVC()
    lr_model = LogisticRegression()
    models = [[nb_model, "nb"], [tree_model, "tree"], [ran_model, "randomForest"], [svm_model, "svm"], [lr_model, "lr"]]
    print("Begin get data")
    training_waves, training_labels, testing_waves, actual_labels = get_training_data(
        "C:\\Users\\Magnus\\Downloads\\LowBGNData\\",
        "C:\\Users\\Magnus\\Desktop\\University\\5semester\\UCN\\")

    print("Begin fitting")
    for i in range(len(models)):
        print("fitting", models[i][1])
        models[i][0].fit(training_waves, training_labels)
        pickle.dump(models[i][0], open("James" + models[i][1] + ".pkl", "wb"))


