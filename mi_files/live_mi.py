import pickle
from mic_recorder import MicRecorder
import specgram_maker
import matplotlib.pyplot as plot
import winsound
# import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library


if __name__ == "__main__":
    f = open("Log.txt", "wb")
    # GPIO.setwarnings(False)  # Ignore warning for now
    # GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    # GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)  # Set the light to off as default
    is_recording = True  # A boolean value that runs the while loop below.
    gau = pickle.load(open("Jamesnb.pkl", "rb"))
    lr = pickle.load(open("Jameslr.pkl", "rb"))
    ran = pickle.load(open("JamesrandomForest.pkl", "rb"))
    # svm = pickle.load(open("Jamessvm.pkl", "rb"))
    tree = pickle.load(open("Jamestree.pkl", "rb"))
    models = [[gau, "gaussian network"], [lr, "logistic regression"], [tree, "decision tree"],
              [ran, "random forest"]]
    mic = MicRecorder(4.0)
    stream = mic.get_stream()
    sgm = specgram_maker.SpecgramMaker()

    while is_recording:  # Vi bør finde en måde at gøre den False på
        rows = []
        predictions = []
        print("Begin recording")
        matrix, freq, t = sgm.make_specgram_from_mic_matrix(mic, stream)
        print("End recording")
        for col in range(len(matrix[1])):  # iterating over coloums.
            max_dB = 0
            max_row = 0
            for row in range(14, 32):  # Finding the row with highest frequency.
                if matrix[row][col] > max_dB:
                    max_dB = matrix[row][col]
                    max_row = row
            rows.append(50 * max_row)
        rows = rows[0:230]

        # plot.scatter(t[0:230], rows)
        # plot.show()
        number_of_true, number_of_false = 0, 0
        for i in range(len(models)):
            pred = models[i][0].predict(rows)
            if pred:
                number_of_true += 1
                print(models[i][1], "says TRUE!")
            else:
                number_of_false += 1
                print(models[i][1], "says false...")

        if number_of_true >= 4:
            # GPIO.output(8, GPIO.HIGH) # This line should be run when the on the Pi
            print("There is a siren!", number_of_true)  # This line should be run when the on the PC
            winsound.PlaySound("C:\\Windows\\media\\Ring01.wav", 1)
        else:
            # GPIO.output(8, GPIO.LOW)  # This line should be run when the on the Pi
            print("There is not a siren...", number_of_true)  # This line should be run when the on the PC

    stream.close()
    f.close()
