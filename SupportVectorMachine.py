import clip_split
import matplotlib.pyplot as plot
import specgram_maker as sm


if __name__ == "__main__":
    spec = sm.SpecgramMaker()
    matrix, freq, t = spec.get_specgram_data_from_wav("Wav\\", "Sample_33_Chatting_Doorbells_WWIISiren_MusicWithSiren2_Rain.wav")
    min_freq = 14
    max_freq = 32
    rows = []
    for col in range(len(matrix[1])):  # iterating over coloums.
        max_dB = 0
        max_row = 0
        for row in range(min_freq, max_freq):  # Finding the row with highest frequency.
            if matrix[row][col] > max_dB:
                max_dB = matrix[row][col]
                max_row = row
        rows.append(50 * max_row)
    plot.scatter(t, rows)
    plot.xlabel("time / seconds")
    plot.ylabel("Frequency / Hz")
    plot.show()
