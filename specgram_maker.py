import os
import math
import time
import matplotlib.pyplot as plt
from matplotlib.mlab import specgram
import scipy.io.wavfile as wavefile
from mic_recorder import MicRecorder


# Returns the data corresponding to the spectrogram made from the wav file at location: "path".
def get_specgram_data_from_wav(path):
    # getting the data from the .wav file.
    sample_rate, data = wavefile.read(path)

    # the resolution of specgram (how big one "pixel" is, measured in hz according y-axis)
    res_in_hz = 50

    # making spectrogram using mlab, and thereby only generating the data corresponding to the specgram.
    spectro, freq, t, = specgram(data, Fs=sample_rate, NFFT=math.ceil(sample_rate / res_in_hz))

    return spectro, freq, t


# private method used for getting a specfic colormap.
def _get_cmap(nameofcmap="inferno"):

    cmap = plt.get_cmap(nameofcmap)

    # this simply says, that is the dB goes below what the
    # cmap can represent show it as the color k (a dark color)
    cmap.set_under(color="k", alpha=None)

    return cmap


# makes a spectrogram from a wav-file, with the option to include colorbar
def make_specgram_from_wav(path, filename, make_cbar=True, grid=False,
                           outputpath=None, ylim=None, xlim=None, figx=20,
                           figy=12, fontsize=20):

    # if the outputpath is not specfied output it at the same location as the .wav file.
    if outputpath is None:
        outputpath = path

    # getting the cmap
    cmap = _get_cmap("inferno")

    # reads the wave file and gets the framerate and the frames(info)
    sample_rate, data = wavefile.read(path)

    # figsize is additional parameters, indicating the size of the figure
    # used instead of plt.figure, since we here get a Axesobject .
    fig, axes = plt.subplots(figsize=(figx, figy))

    # the resolution of specgram (how big one "pixel" is, measured in hz according y-axis)
    res_in_hz = 50

    # making the spectrogram, see doc for return values.
    # can also make stereo to mono by saying data[:,0], which takes the first channel
    spectro, freq, t, pic = axes.specgram(data, Fs=sample_rate, cmap=cmap,
                                          NFFT=math.ceil(sample_rate/res_in_hz))

    _finish_plot(axes, xlim, ylim, fontsize, pic,
                 fig, make_cbar, grid)

    # saves the file in this folder.
    # for quick view, call this: plt.show()
    plt.savefig(outputpath+filename+".png")

    # This clears the memory used by the figure.
    # Otherwise memory usage becomes too high if this function is called inside a loop.
    plt.close(fig)


# makes spectrogram for all wav-files in a directory
def make_specgram_for_dir(dirpath, make_cbar=True, grid=False,
                          outputpath=None, ylim=None, xlim=None, figx=20,
                          figy=12, fontsize=20):
    directory = dirpath
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            # splitting in order to get name of file
            args = filename.split(".")
            name_of_file = args[0]
            make_specgram_from_wav(directory+filename, name_of_file, make_cbar, grid,
                                   outputpath, ylim, xlim, figx, figy, fontsize)


# private functions which perform cosmetic actions on the given plot.
def _finish_plot(axes, xlim, ylim, fontsize, pic,
                 fig, make_cbar, grid):

    # sets the limits for the y-axis and x-axis
    if xlim is not None:
        axes.set_xlim(0, xlim)
    if ylim is not None:
        axes.set_ylim(0, ylim)

    # if grid is desired, it is made
    if grid:
        # b=True indicates that grid is desired.
        axes.grid(b=True, axis="both", color="w", linewidth=1.2, linestyle="--")

    # sets labels and sizes of labels
    axes.set_xlabel("Time[sec]", fontsize=fontsize)
    axes.set_ylabel("Frequency [Hz]", fontsize=fontsize)
    axes.tick_params(labelsize=fontsize)

    # plots the colorbar
    if make_cbar:
        cbar = fig.colorbar(pic)
        cbar.set_label("Intensity dB", fontsize=fontsize)


# makes a spectrogram from a wav-file, with the option to include colorbar
def make_specgram_from_mic(outputpath, filename, viewable, make_cbar=True, grid=False,
                           ylim=None, xlim=None, figx=20,
                           figy=12, fontsize=20, total_length=10, sample_length=1):

    # otherwise it is a bit tricky to determine how much to shift.
    if viewable % sample_length != 0:
        raise AttributeError("viewable must be dividable by sample_length")

    # getting the cmap
    cmap = _get_cmap("inferno")

    # the resolution of specgram (how big one "pixel" is, measured in hz according y-axis)
    res_in_hz = 50

    # instantiating a micrecorder indicating the span of a recording.
    micrecorder = MicRecorder(sample_length)

    # getting the stream to read from
    stream = micrecorder.get_stream()

    totaltime = total_length
    viewable = 5

    # the accumulated data used for the spectrogram.
    a_data = []

    print("Recording.")
    t0 = time.time()
    for x in range(0, totaltime):

        # figsize is additional parameters, indicating the size of the figure.
        # This is used instead of plt.figure, since we here get a Axesobject .
        fig, axes = plt.subplots(figsize=(figx, figy))

        # getting the data from the sound recorded from the mic in the given span.
        data = micrecorder.get_data_from_mic(stream)

        # if the spectrogram is showing the viewable amount of seconds
        # we begin to shift out the start of the spectrogram.
        if x >= viewable:
            del a_data[0:micrecorder.rate]

        # converting a ndarray to an array/list otherwise we cant extend it to a_data.
        a_data.extend(data.ravel())

        # making the spectrogram, see doc for return values.
        # can also make stereo to mono by saying data[:,0], which takes the first channel
        spectro, freq, t, pic = axes.specgram(a_data, Fs=micrecorder.rate, cmap=cmap,
                                              NFFT=math.ceil(micrecorder.rate/res_in_hz))

        # perform the final cosmetic actions on the plot.
        _finish_plot(axes, xlim, ylim, fontsize, pic,
                     fig, make_cbar, grid)

        # saves the file in the given folder.
        plt.savefig(outputpath+filename+str(x)+".png")

        # This clears the memory used by the figure.
        # Otherwise memory usage becomes too high if plt.subplots is called inside a loop.
        plt.close(fig)

    t1 = time.time()

    print("Done.")
    print("Total time span: " + t1-t0)

    # closing the stream to the microphone.
    stream.close()


if __name__ == "__main__":
    make_specgram_from_mic("C:\\Users\\Jacob\\Music\\Samples\\Alle\\Specgrams\\", "live", 5)
