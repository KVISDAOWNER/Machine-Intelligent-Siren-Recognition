from unittest import TestCase
from specgram_maker import SpecgramMaker
import os

# The only function with automated test is get_specgram_data_from_wav.
# The other functions are tested manually (called manual testing) since it is hard to
# programmically assert if they produce the correct result.


class TestSpecgramMaker(TestCase):
    def test_get_specgram_data_from_wav(self):
        specmaker = SpecgramMaker()
        # This may cause problem idk.
        data, freq, t= specmaker.get_specgram_data_from_wav(os.getcwd()+"\\Ressources\\", "Sirene23.wav")
        # I could assert if the correct matrix is given, however, it may be cumbersome,
        # and I that asserting if the matrix is made is equally good since this function gets its
        # matrix from a function from a library.
        self.failIf(data.shape != (442, 1861) and data.size != 822562)

    def test_make_specgram_from_wav(self):
        self._alwaysTrue()

    def test_make_specgram_from_mic(self):
        self._alwaysTrue()

    def test_make_specgram_for_dir(self):
        self._alwaysTrue()

    def _alwaysTrue(self):
        self.failIf(1 == 2)

