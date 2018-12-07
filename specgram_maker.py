import os
import math
import time
import matplotlib.pyplot as plt
from matplotlib.mlab import specgram
import scipy.io.wavfile as wavefile
from mic_recorder import MicRecorder


class SpecgramMaker:

    # Returns the data corresponding to the spectrogram made from the wav file at location: "path".
    def get_specgram_data_from_wav(self, pathtofile, filename, resolution=50):
        # getting the data from the .wav file.
        sample_rate, data = wavefile.read(pathtofile+filename)

        # making spectrogram using mlab, and thereby only generating the data corresponding to the specgram.
        if data.shape.__len__()==2:
            data = data[:,0]
        spectro, freq, t, = specgram(data, Fs=sample_rate, NFFT=math.ceil(sample_rate / resolution))

        return spectro, freq, t

    # private method used for getting a specific colormap.
    def _get_cmap(self, cmap_name):

        cmap = plt.get_cmap(cmap_name)

        # this simply says, that is the dB goes below what the
        # cmap can represent show it as the color k (a dark color)
        cmap.set_under(color="k", alpha=None)

        return cmap

    # makes a spectrogram from a wav-file,
    # path could be C:\\...\\Music\\ and filename could be Sirene56.wav
    def make_specgram_from_wav(self, pathtofile, filename, outputpath=None,
                               resolution=50, cmap_name="inferno",
                               make_cbar=True, grid=False,
                               ylim=None, xlim=None, figx=20,
                               figy=12, fontsize=20, onlyspecgram=False):

        # if no output path is given, output at the same location as the .wav file.
        if outputpath is None:
            outputpath = pathtofile

        # getting the cmap
        cmap = self._get_cmap(cmap_name)

        # reads the wave file and gets the framerate and the frames(info)
        sample_rate, data = wavefile.read(pathtofile+filename)

        # figsize is additional parameters, indicating the size of the figure
        # used instead of plt.figure, since we here get a Axesobject .
        fig, axes = plt.subplots(figsize=(figx, figy))

        # making the spectrogram, see doc for return values.
        # can also make stereo to mono by saying data[:,0], which takes the first channel
        spectro, freq, t, pic = axes.specgram(data, Fs=sample_rate, cmap=cmap,
                                              NFFT=math.ceil(sample_rate/resolution))

        self._finish_plot(axes, xlim, ylim, fontsize, pic,
                          fig, make_cbar, grid, onlyspecgram)

        self._save_and_close_fig(outputpath, filename, fig, onlyspecgram)

    def _save_and_close_fig(self, outputpath, wav_file_name, fig, onlyspecgram, optional=""):
        # Removes the .wav in the end of the wav file's name
        filename = wav_file_name[::-1].split("vaw.", 1)[1][::-1]
        # saves the file in this folder.
        if onlyspecgram:
            plt.savefig(outputpath + filename + optional + ".png",
                        bbox_inches="tight", pad_inches=-0.1)
        else:
            plt.savefig(outputpath + filename + optional + ".png")

        # This clears the memory used by the figure.
        # Otherwise memory usage becomes too high if this function is called inside a loop.
        plt.close(fig)

    def _save_and_close_fig1(self, outputpath,filename, fig, onlyspecgram, optional=""):
        # Removes the .wav in the end of the wav file's name
        #filename = wav_file_name[::-1].split("vaw.", 1)[1][::-1]
        # saves the file in this folder.
        if onlyspecgram:
            plt.savefig(outputpath + filename + optional + ".png",
                        bbox_inches="tight", pad_inches=-0.1)
        else:
            plt.savefig(outputpath + filename + optional + ".png")

        # This clears the memory used by the figure.
        # Otherwise memory usage becomes too high if this function is called inside a loop.
        plt.close(fig)

    # private functions which perform cosmetic actions on the given plot.
    def _finish_plot(self, axes, xlim, ylim, fontsize, pic,
                     fig, make_cbar, grid, onlyspecgram):
        # sets the limits for the y-axis and x-axis
        if xlim is not None:
            axes.set_xlim(0, xlim)
        if ylim is not None:
            axes.set_ylim(0, ylim)

        # if onlyspecgram, we only want the specgram.
        if onlyspecgram:
            axes.tick_params(axis="both", which="both", labelbottom=False, labelleft=False,
                             bottom=False, top=False, right=False, left=False)
        else:
            axes.set_ylabel("Frequency [Hz]", fontsize=fontsize)

            # sets labels and sizes of labels
            axes.set_xlabel("Time[sec]", fontsize=fontsize)

            axes.tick_params(labelsize=fontsize)

        # if grid is desired, it is made
        if grid and not onlyspecgram:
            # b=True indicates that grid is desired.
            axes.grid(b=True, axis="both", color="w", linewidth=1.2, linestyle="--")

        # plots the colorbar
        if make_cbar and not onlyspecgram:
            cbar = fig.colorbar(pic)
            cbar.set_label("Intensity dB", fontsize=fontsize)

    def make_specgram_from_mic_matrix(self, micrecorder, stream):
            
        # getting the data from the sound recorded from the mic in the given span.
        data = micrecorder.get_data_from_mic(stream)

        data = data.ravel()

        # making spectrogram using mlab, and thereby only generating the data corresponding to the specgram.
        spectro, freq, t, = specgram(data, Fs=micrecorder.rate, NFFT=math.ceil(micrecorder.rate / 50))

        return spectro, freq, t

    # makes a spectrogram from a wav-file, with the option to include colorbar
    def make_specgram_from_mic(self, outputpath, filename, viewablespan, total_length, sample_length,
                               resolution=50, cmap_name="inferno", make_cbar=True, grid=False,
                               ylim=None, xlim=None, figx=20, figy=12,
                               fontsize=20, onlyspecgram=False):

        # otherwise it is a bit tricky to determine how much to shift.
        if viewablespan % sample_length != 0:
            raise AttributeError("viewable must be dividable by sample_length")

        if total_length % viewablespan != 0:
            raise AttributeError("total_length must be dividable by viewable")

        # getting the cmap
        cmap = self._get_cmap(cmap_name)

        # instantiating a micrecorder indicating the span of a recording.
        micrecorder = MicRecorder(sample_length)

        # getting the stream to read from
        stream = micrecorder.get_stream()

        totaltime = total_length
        viewable = viewablespan

        # the accumulated data used for the spectrogram.
        a_data = []

        print("Recording.")
        t0 = time.time()


        timerecorded = 0

        while timerecorded < totaltime:

            # figsize is additional parameters, indicating the size of the figure.
            # This is used instead of plt.figure, since we here get a Axesobject .
            fig, axes = plt.subplots(figsize=(figx, figy))

            # getting the data from the sound recorded from the mic in the given span.
            data = micrecorder.get_data_from_mic(stream)

            # if the spectrogram is showing the viewable amount of seconds
            # we begin to shift out the start of the spectrogram.
            if timerecorded >= viewable:
                # Shifts out the amount of samples recorded each time.
                del a_data[0:(micrecorder.rate * sample_length)]

            # converting a ndarray to an array/list otherwise we cant extend it to a_data.
            # Then adding the newly read sound.
            a_data.extend(data.ravel())

            # making the spectrogram, see doc for return values.
            # can also make stereo to mono by saying data[:,0], which takes the first channel
            spectro, freq, t, pic = axes.specgram(a_data, Fs=micrecorder.rate, cmap=cmap,
                                                  NFFT=math.ceil(micrecorder.rate/resolution))

            # perform the final cosmetic actions on the plot.
            self._finish_plot(axes, xlim, ylim, fontsize, pic,
                              fig, make_cbar, grid, onlyspecgram)

            self._save_and_close_fig1(outputpath, filename, fig, onlyspecgram, str(timerecorded))

            timerecorded += sample_length

        t1 = time.time()

        print("Done.")
        # print("Total time span: " + t1-t0)

        # closing the stream to the microphone.
        stream.close()

    # makes spectrogram for all wav-files in a directory
    # to indicate the folder with the file, just give the path
    # to one of the files in the constructor and then do anything else as usual
    def make_specgram_for_dir(self, dirpath, outputpath=None, resolution=50,
                              cmap_name="inferno", make_cbar=True, grid=False,
                              ylim=None, xlim=None, figx=20, onlyspecgram=False,
                              figy=12, fontsize=20):
        directory = dirpath
        if outputpath is None:
            outputpath = directory
        else:
            outputpath = outputpath
        for filename in os.listdir(directory):
            if filename.endswith(".wav"):
                self.make_specgram_from_wav(directory, filename, outputpath, resolution,
                                            cmap_name, make_cbar,
                                            grid, ylim, xlim, figx, figy,
                                            fontsize, onlyspecgram)

if __name__ == "__main__":
    sm = SpecgramMaker()
    sm.make_specgram_from_mic("C:\\Users\\Magnus\\Desktop\\GetPatterns\\", "test", 10, 30, 5)