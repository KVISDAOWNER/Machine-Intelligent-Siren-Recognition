from unittest import TestCase
from clip_split import _find_subset_of_clip


class Test_find_subset_of_clip(TestCase):
    def test__find_subset_of_clip1(self):
        #arrange
        clip = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
        start = 2
        end = 8
        time = [0,1,2,3,4,5,6,7,8,9,10]

        #act
        ls = _find_subset_of_clip(clip, start, end, time)

        #assert
        assert ls == [2, 3, 4, 5, 6, 7]

    def test__find_subset_of_clip2(self):
        # arrange
        clip = [1,2,2,2,2,1,2,2,1,0]
        start = 0
        end = 0
        time = [1,2,3,4,5,6,7,8,9]

        #act
        ls = _find_subset_of_clip(clip, start, end, time)

        #assert
        assert ls == []

    def test__find_subset_of_clip3(self):
        # arrange
        clip = [10,5,3,20,34,5,2,3,98,1]
        start = 3
        end = 4
        time = [0,1,2,2.5,3,3.5,4,5,6]

        # act
        ls = _find_subset_of_clip(clip, start, end, time)

        assert ls == [34,5]

    def test__find_subset_of_clips4(self):
        clip = [1,2,3,4,5,6,7,8,9]
        start = 5
        end = 4
        time = [1,2,3,4,5,7,9,8,6]

        ls = _find_subset_of_clip(clip, start, end, time)

        assert ls == []