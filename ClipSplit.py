import specgram_maker as SM
import os


def extract(path, max_freq=442, length=20):
    sm = SM.SpecgramMaker()
    directory = os.listdir(path)
    time = []
    rows = []
    files_frequencies_array = []
    labels = []

    # This for loop is the same as in regression

    for filename in directory:
        if not filename.endswith(".wav"):
            continue

        labels.append("sirenAt" in filename or "siren" in filename or "SPCSiren" in filename)

        spec, freq, t = sm.get_specgram_data_from_wav(path, filename)
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
        print("Done importing " + filename + ".", labels[len(time) - 1], str(len(time) * 100 / len(directory)) + " %")

    # if length is 20, we split them with the _split_clips function
    if length == 20:
        split_waves, labels = _split_clips(files_frequencies_array, labels, directory, time)
    # otherwise we do nothing
    else:
        split_waves = files_frequencies_array

    return split_waves, time, labels


def _find_subset_of_clip(clip, start, end, time):
    index_one = -1
    index_two = -1
    # index_one and index_two show on which index the clip begins and on which index the clip ends
    for i in range(len(time)):
        t = time[i]
        # if we cross the timestamp given by start, we set index_one to i
        if (t >= start) and (index_one == -1):
            index_one = i
        # if we cross the timestamp given by end, we set index_two to i
        if (t >= end) and (index_two == -1):
            index_two = i
    # finally, we can return the part of the array that is between the indices of index_one and index_two
    return clip[index_one:index_two]


def _split_clips(files_frequencies_array, labels, file_names, time):
    split_waves = []
    new_labels = []
    for i in range(len(labels)):
        # Assuming labels and files_frequencies_array are of equal length
        if labels[i]:
            # If the i'th clip has a siren at some point
            siren_start = int(file_names[i].split("_")[3])
            # The file names say when the sirens start. One filename could be Sample_2_sirenAt_13_Dogs_WWIISiren
            # which would mean that the sirens start at the 13th second.
            for j in range(-3, 4):
                # The idea is to find as many sub-clips in files_frequencies_array[i] as possible. To do this, we have
                # to find out how many 5-second clips we can extract out of the 20 second clip. We only want clips that
                # are 100 % sirens or 0 % sirens.
                new_start = j * 5 + siren_start
                # new_start is a potential starting second for a sub-clip.
                if 0 <= new_start <= 15:
                    # If new_start < 0 or new_start > 15, we skip it, because we only want 5-second clips.
                    # Otherwise, we append a new clip to split_waves. The new clip is a five second clip between
                    # new_start and new_start + 5.
                    split_waves.append(_find_subset_of_clip(files_frequencies_array[i], new_start, new_start + 5,
                                                            time[i]))
                    # Then we append the new_labels with whether or not the siren has begun yet, or in other words,
                    # whether the siren start is earlier than new_start
                    new_labels.append(new_start >= siren_start)
        else:
            # If the clip does not have a siren in it at all, we split the 20-second clip into four 5-second clips
            for j in range(4):
                split_waves.append(_find_subset_of_clip(files_frequencies_array[i], 5 * j, 5 * j + 5, time[i]))
                new_labels.append(False)
    # split_waves are the frequencies split into 5-second clips.
    # new_labels are the labels of the 5-second clips. The two lists should have equal length.
    return split_waves, new_labels
