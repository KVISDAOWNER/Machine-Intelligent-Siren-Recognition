import os
import clip_split as cs
from unittest import TestCase


class TestExtract(TestCase):
    def test_extract(self):
        # Arrange
        path = os.getcwd()+"\\Ressources\\for_test_extract\\"

        # Act
        split_waves, time, label = cs.extract(path, split=True)

        freq, time1, = cs.extract(path, split=False)

        # Assert
        # These are the expected values.
        # This approach is used, since its the only
        # way I can think of to test the correctness of the outputs.
        exp_split_waves_len = 3
        exp_split_waves_0_len = 293
        exp_split_waves_1_len = 292
        exp_split_waves_2_len = 293
        exp_time_len = 1
        exp_time_0_shape = (1861,)
        exp_time_0_size = 1861
        exp_label_0 = False
        exp_label_1 = False
        exp_label_2 = True

        exp_freq_len = 1
        exp_freq_0_len = 1861

        exp_time1_len = 1
        exp_time1_0_size = 1861
        exp_time1_0_shape = (1861,)

        self.assertEqual(len(split_waves), exp_split_waves_len)
        self.assertEqual(len(split_waves[0]), exp_split_waves_0_len)
        self.assertEqual(len(split_waves[1]), exp_split_waves_1_len)
        self.assertEqual(len(split_waves[2]), exp_split_waves_2_len)
        self.assertEqual(len(time), exp_time_len)
        self.assertEqual(time[0].shape, exp_time_0_shape)
        self.assertEqual(time[0].size, exp_time_0_size)
        self.assertEqual(label[0], exp_label_0)
        self.assertEqual(label[1], exp_label_1)
        self.assertEqual(label[2], exp_label_2)
        self.assertEqual(len(freq), exp_freq_len)
        self.assertEqual(len(freq[0]), exp_freq_0_len)
        self.assertEqual(len(time1), exp_time1_len)
        self.assertEqual(time1[0].size, exp_time1_0_size)
        self.assertEqual(time1[0].shape, exp_time1_0_shape)
