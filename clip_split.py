import specgram_maker as sm
import os


# This method turns .wav-files into matrices that correspond to the spectrograms made in specmaker. It also splits the
# matrices into roughly equal sized bits.
# Parameters:
# path(string):         The path to the folder that contains the .wav-files to be converted to matrices.
# max_freq (number):    The maximum frequency (in Hz) that is considered relevant for vertical maxima. Only the highest
#                       frequency less than or equal to max_freq will be included.
# min_freq (number):    The minimum frequency (in Hz) that is considered relevant for vertical maxima. Only the highest
#                       frequency greater than or equal to max_freq will be included.
# training (bool):      Should be true if the matrices are used for training and should be false otherwise. It changes
#                       which method is called in the end.
# split (bool):         True if the clips should be split and false otherwise.
# divisions (number):   The number of clips that the original clips should be split into. Cannot be 0. split=1
#                       corresponds to split=false
#
# Returns:
# split_waves (list of list of numbers):    One list of the highest frequencies for each file for each division.
# time (list of numbers):                   A list that ties the index in the split_waves list to actual time in
#                                           seconds.
# labels (list of bool):                    index i is True iff the i'th clip contains a siren.
#
# split_waves, time and labels have the same length
def extract(path, max_freq=1600, training=True, split=True, divisions=4, min_freq=750):
    specmaker = sm.SpecgramMaker()
    directory = os.listdir(path)
    filenames = []
    time = []
    rows = []
    files_frequencies_array = []
    labels = []

    for filename in directory:
        # We only consider .wav-files
        if not filename.endswith(".wav"):
            continue
        filenames.append(filename)
        # We append whether or not the filename says there is a siren in the clip. There have been many ways to
        # indicate this, so this line is kind of long. :(
        labels.append("sirenAt" in filename or "siren" in filename or "SPCSiren" in filename)

        # We convert the .wav-file into a matrix with specmaker.
        spec, freq, t = specmaker.get_specgram_data_from_wav(path, filename)

        # For each column:
        for col in range(len(spec[1])):
            max_dB = 0
            max_row = 0
            # For each row:
            for row in range(int(min_freq / 50), int(max_freq / 50)):   # We divide with 50, because the frequencies
                                                                        # are in multiples of 50.
                # We find the highest value in the column.
                if spec[row][col] > max_dB:
                    max_dB = spec[row][col]
                    max_row = row
            # When we have found the highest column, we append that number times 50.
            # This is because the y-axis works in multiples of 50.
            rows.append([50 * max_row, max_dB])
        # files_frequencies_array now contains rows, which is a list of the highest values in each column.
        # I'm not sure, why the rows are copied and then cleared.
        files_frequencies_array.append(rows.copy())
        rows.clear()
        # We would like to keep track of the times for future use.
        time.append(t)
        # Here we print, to keep track of how long we are in importing.
        print("Done importing " + filename + ".", labels[len(time) - 1], str(len(time) * 100 / len(directory)) + " %")
    # This is where we split,, if split is true
    if split:
        # We call different methods dependant on whether it is used for training or not.
        if training:
            split_waves, labels = _split_training(files_frequencies_array, labels, filenames, time, divisions)
        else:
            split_waves, labels = _split_testing(files_frequencies_array, labels, filenames, time, divisions)
    # If we don't split, we simply copy it into split_waves.
    else:
        split_waves = files_frequencies_array

    new_waves  = []
    for feature_set in split_waves:
        new_feature_set = []
        for tubel_element in feature_set:
            new_feature_set.append(tubel_element[0])
            new_feature_set.append(tubel_element[1])
        new_waves.append(new_feature_set)

    return new_waves, time, labels


# Finds and returns a sub-clip of a given sound clip between start-time and end-time.
# Parameters:
# clip (list of numbers):   A clip that has been extracted by the extract method.
# start (number):           The second where the sub clip begins.
# end (number):             The second where the sub clip ends.
# time (list numbers):      translates from indices to real time.
#
# Returns (list of numbers): The sub clip of clip that runs between start and end.
def _find_subset_of_clip(clip, start, end, time):
    index_one = -1
    index_two = -1
    for i in range(len(time)):
        t = time[i]
        if (t >= start) and (index_one == -1):
            # The first time we see a time that is greater than start, we set the index.
            index_one = i
        if (t >= end) and (index_two == -1):
            # The first time we see a time that is greater than end, we set the index.
            index_two = i
            break
            # Assuming that end > start, we can break out of the for loop at this point.
    # When we are done, we can return the clip between the two indices.
    return clip[index_one:index_two]


# Splits lists of lists of training data into smaller divisions.
# Parameters:
# files_frequencies_array (list of lists of numbers):   The extracted vertical maxima arrays.
# labels (list of bool):                                Shows which arrays are sirens and which are not.
# file_names (list of strings):                         The file_names which could say whether or not there is a siren.
# times (list of numbers):                              A list of times corresponding to an array entry.
# divisions (number):                                   Number of divisions to split into. Cannot be 0.
# files_frequencies_array, labels, file_names have equal length.
#
# Returns:
# split_waves (list of lists of numbers):   files_frequencies_array but split into sub-clips.
# new_labels (list of bool):                entry i is true iff split_waves[i] contains a siren.
def _split_training(files_frequencies_array, labels, file_names, times, divisions=4):
    split_waves = []
    new_labels = []
    seconds_per_division = times[0][-1] / float(divisions)
    for i in range(len(labels)):
        # If the i'th clip contains a siren.
        if labels[i]:
            siren_start = int(file_names[i].split("_")[3])
            # Due to the naming scheme of the training data, we know that this number is the second at which the siren
            # starts.
            for j in range(divisions):
                # For each wanted sub-clip:
                new_start = j * seconds_per_division
                # If there is room for another split:
                t = times[0][-1]
                if new_start <= t - seconds_per_division:
                    # We find a sub-clip starting at new_start that lasts for seconds_per_division seconds.
                    split_waves.append(_find_subset_of_clip(files_frequencies_array[i], new_start,
                                                            new_start + seconds_per_division, times[i]))

                    # In new_labels, we add whether or not the siren has begun before the end of the clip.
                    new_labels.append(new_start + seconds_per_division >= siren_start)
        else:  # If the i'th clip does not contain a siren:
            # We split the clip into divisions, and mark that there is not a siren.
            for j in range(divisions):
                split_waves.append(_find_subset_of_clip(files_frequencies_array[i], seconds_per_division * j,
                                                        seconds_per_division * j + seconds_per_division, times[i]))
                new_labels.append(False)
    return split_waves, new_labels


# Splits lists of lists of test data into smaller divisions. When testing, we are not allowed to split differently based
# on whether or not there is a siren.
# Parameters: Copy-paste from _split_training
# files_frequencies_array (list of lists of numbers):   The extracted vertical maxima arrays.
# labels (list of bool):                                Shows which arrays are sirens and which are not.
# file_names (list of strings):                         The file_names which could say whether or not there is a siren.
# times (list of numbers):                              A list of times corresponding to an array entry.
# divisions (number):                                   Number of divisions to split into. Cannot be 0.
# files_frequencies_array, labels, file_names have equal length.
#
# Returns:
# split_waves (list of lists of numbers):   files_frequencies_array but split into sub-clips.
# new_labels (list of bool):                entry i is true iff split_waves[i] contains a siren. They are used for the
#                                           confusion matrix.
def _split_testing(files_frequencies_array, labels, file_names, times, divisions=4):
    split_waves = []
    new_labels = []

    for i in range(len(labels)):
        # We calculate the number of seconds for each division based on the length of the i'th clip, and the number of
        # divisions
        seconds_per_division = times[i][-1] / divisions
        for j in range(divisions):
            split_waves.append(_find_subset_of_clip(files_frequencies_array[i], seconds_per_division * j,
                                                    seconds_per_division * j + seconds_per_division, times[i]))
            # If we know where the sirens begin in the sub-clip, we can make new_labels more correct, since we can
            # append True if the siren's start time is before the end of the sub-clip, and False otherwise
            if "sirenAt" in file_names[i]:
                siren_times = int(file_names[i].split('_')[3])
                new_labels.append(siren_times - seconds_per_division < seconds_per_division * j)
            # If we don't know, we can just append whatever was in the old labels.
            else:
                new_labels.append(labels[i])

    return split_waves, new_labels



