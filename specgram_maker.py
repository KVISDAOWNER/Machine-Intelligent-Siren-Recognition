import os
import math
import time
import matplotlib.pyplot as plt
from matplotlib.mlab import specgram
import scipy.io.wavfile as wavefile
from mic_recorder import MicRecorder


class SpecgramMaker:

    # Take all the variables common for the functions.
    def __init__(self, resolution=50):
        self.rez_in_hz = resolution

    # Returns the data corresponding to the spectrogram made from the wav file at location: "path".
    def get_specgram_data_from_wav(self, path):
        # getting the data from the .wav file.
        sample_rate, data = wavefile.read(path)

        # the resolution of specgram (how big one "pixel" is, measured in hz according y-axis)
        res_in_hz = 50

        # making spectrogram using mlab, and thereby only generating the data corresponding to the specgram.
        spectro, freq, t, = specgram(data, Fs=sample_rate, NFFT=math.ceil(sample_rate / res_in_hz))

        return spectro, freq, t

    # private method used for getting a specfic colormap.
    def _get_cmap(self, nameofcmap="inferno"):

        cmap = plt.get_cmap(nameofcmap)

        # this simply says, that is the dB goes below what the
        # cmap can represent show it as the color k (a dark color)
        cmap.set_under(color="k", alpha=None)

        return cmap

    # makes a spectrogram from a wav-file, with the option to include colorbar
    def make_specgram_from_wav(self, path, filename, outputpath=None, make_cbar=True, grid=False,
                               ylim=None, xlim=None, figx=20,
                               figy=12, fontsize=20, labels=True, ticks=True):

        # if the outputpath is not specfied output it at the same location as the .wav file.
        if outputpath is None:
            outputpath = path

        # getting the cmap
        cmap = self._get_cmap("inferno")

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

        self._finish_plot(axes, xlim, ylim, fontsize, pic,
                          fig, make_cbar, grid, labels, ticks)

        self._save_and_close_fig(outputpath, filename, fig)

    # makes spectrogram for all wav-files in a directory
    def make_specgram_for_dir(self, dirpath, make_cbar=True, grid=False,
                              outputpath=None, ylim=None, xlim=None, figx=20,
                              figy=12, fontsize=20):
        directory = dirpath
        for filename in os.listdir(directory):
            if filename.endswith(".wav"):
                # splitting in order to get name of file
                args = filename.split(".")
                name_of_file = args[0]
                self.make_specgram_from_wav(directory+filename, name_of_file, make_cbar, grid,
                                            outputpath, ylim, xlim, figx, figy, fontsize)

    def _save_and_close_fig(self, outputpath, filename, fig):
        # saves the file in this folder.
        plt.savefig(outputpath + filename + ".png", bbox_inches="tight", pad_inches=-0.1)

        # This clears the memory used by the figure.
        # Otherwise memory usage becomes too high if this function is called inside a loop.
        plt.close(fig)

    # private functions which perform cosmetic actions on the given plot.
    def _finish_plot(self, axes, xlim, ylim, fontsize, pic,
                     fig, make_cbar, grid, labels=True, ticks=True):

        # sets the limits for the y-axis and x-axis
        if xlim is not None:
            axes.set_xlim(0, xlim)
        if ylim is not None:
            axes.set_ylim(0, ylim)

        # if grid is desired, it is made
        if grid:
            # b=True indicates that grid is desired.
            axes.grid(b=True, axis="both", color="w", linewidth=1.2, linestyle="--")

        if labels:
            # sets labels and sizes of labels
            axes.set_xlabel("Time[sec]", fontsize=fontsize)
            axes.set_ylabel("Frequency [Hz]", fontsize=fontsize)
        else:
            axes.tick_params(axis="both", which="both", labelbottom=False, labelleft=False)

        if ticks:
            axes.tick_params(labelsize=fontsize)
        else:
            axes.tick_params(axis="both", which="both", bottom=False,
                             top=False, right=False, left=False)

        # plots the colorbar
        if make_cbar:
            cbar = fig.colorbar(pic)
            cbar.set_label("Intensity dB", fontsize=fontsize)

    # makes a spectrogram from a wav-file, with the option to include colorbar
    def make_specgram_from_mic(self, outputpath, filename, viewable, make_cbar=True, grid=False,
                               ylim=None, xlim=None, figx=20,
                               figy=12, fontsize=20, total_length=10, sample_length=1):

        # otherwise it is a bit tricky to determine how much to shift.
        if viewable % sample_length != 0:
            raise AttributeError("viewable must be dividable by sample_length")

        if total_length % viewable != 0:
            raise AttributeError("total_length must be dividable by viewable")

        # getting the cmap
        cmap = self._get_cmap("inferno")

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

        # getting the amount of samples.
        x = 0

        while x < totaltime:

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
            self._finish_plot(axes, xlim, ylim, fontsize, pic,
                         fig, make_cbar, grid)

            self._save_and_close_fig(outputpath, filename+str(x), fig)

            x += sample_length

        t1 = time.time()

        print("Done.")
        # print("Total time span: " + t1-t0)

        # closing the stream to the microphone.
        stream.close()

    def make_clean_specgram(self, path, filename, outputpath=None):
        self.make_specgram_from_wav(path, filename, outputpath, make_cbar=False,
                                    grid=False, labels=False, ticks=False)


if __name__ == "__main__":
    specmaker = SpecgramMaker()
    specmaker.make_clean_specgram("C:\\Users\\Jacob\\Music\\Samples\\Alle\\Sirene56.wav", "Sirene56")

