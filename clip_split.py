import specgram_maker as sm
import os


def extract(path, max_freq=442):
    specmaker = sm.SpecgramMaker()
    directory = os.listdir(path)
    time = []
    rows = []
    files_frequencies_array = []
    labels = []

    for filename in directory:
        if not filename.endswith(".wav"):
            continue

        labels.append("sirenAt" in filename or "siren" in filename or "SPCSiren" in filename)

        spec, freq, t = specmaker.get_specgram_data_from_wav(path, filename)
        for i in range(len(spec[1])):  # iterating over coloums.
            max_dB = 0
            row = 0
            for j in range(max_freq):  # Finding the row with highest frequency.
                if spec[j][i] > max_dB:
                    max_dB = spec[j][i]
                    row = j
            rows.append(50 * row)
        files_frequencies_array.append(rows.copy())
        rows.clear()
        time.append(t)
        os.system("cls")
        print("Done importing " + filename + ".", labels[len(time) - 1], str(len(time) * 100 / len(directory)) + " %")

    split_waves, labels = split_clips(files_frequencies_array, labels, directory, time)

    return split_waves, time, labels


def find_subset_of_clip(clip, start, end, time):
    index_one = -1
    index_two = -1
    for i in range(len(time)):
        t = time[i]
        if (t >= start) and (index_one == -1):
            index_one = i
        if (t >= end) and (index_two == -1):
            index_two = i

    return clip[index_one:index_two]


def split_clips(files_frequencies_array, labels, file_names, time):
    split_waves = []
    new_labels = []
    for i in range(len(labels)):  # Assuming labels and files_frequencies_array are of equal length
        if labels[i]:
            siren_start = int(file_names[i].split("_")[3])
            for j in range(-3, 4):
                new_start = j * 5 + siren_start
                if 0 <= new_start <= 15:
                    split_waves.append(find_subset_of_clip(files_frequencies_array[i], new_start, new_start + 5, time[i]))
                    new_labels.append(new_start >= siren_start)
        else:
            for j in range(4):
                split_waves.append(find_subset_of_clip(files_frequencies_array[i], 5 * j, 5 * j + 5, time[i]))
                new_labels.append(False)

    return split_waves, new_labels

def regression_extract(self, path, max_freq=442):
    labels = []
    rows = []
    FilesFrequenciesAr = []
    time = []
    specmaker = sm.SpecgramMaker()

    directory = os.listdir(path)
    for filename in directory:
        if not filename.endswith(".wav"):
            continue

        if "SPCSiren" in filename or "siren" in filename or "sirenAt" in filename:
            labels.append(True)
        else:
            labels.append(False)

        spec, freq, t = specmaker.get_specgram_data_from_wav(path, filename)
        for i in range(len(spec[1])):  # iterating over coloums.
            MaxFrequencyValue = 0
            row = 0
            for j in range(max_freq):  # Finding the row with highest frequency.
                if spec[j][i] > MaxFrequencyValue:
                    MaxFrequencyValue = spec[j][i]
                    row = j
            rows.append(50 * row)
        FilesFrequenciesAr.append(rows.copy())
        rows.clear()
        time.append(t)
        print("Done importing " + filename + ".", labels[len(time) - 1], str(len(time) * 100 / len(directory)) + " %")
    return FilesFrequenciesAr, time

