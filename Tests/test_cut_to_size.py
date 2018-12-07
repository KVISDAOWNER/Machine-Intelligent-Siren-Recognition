from unittest import TestCase
from clip_split import cut_to_size


class TestCut_to_size(TestCase):
    def test_cut_to_size1(self):
        # arrange
        ls = [[1,2,3], [4,5,6], [7,8,9]]
        len = 2

        # act
        result = cut_to_size(ls, len)

        #assert
        assert result == [[1,2], [4,5], [7,8]]

    def test_cut_to_size2(self):
        # arrange
        ls = [[1,2,3], [4,5,6], [7,8,9]]
        len = 1

        # act
        result = cut_to_size(ls, len)

        #assert
        assert result == [[1], [4], [7]]

    def test_cut_to_size3(self):
        # arrange
        ls = [[1,2,3], [4,5,6], [7,8,9]]
        len = 3

        # act
        result = cut_to_size(ls, len)

        #assert
        assert result == [[1,2, 3], [4,5, 6], [7,8, 9]]

    def test_cut_to_size4(self):
        # arrange
        ls = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        len = 0

        # act
        result = cut_to_size(ls, len)

        # assert
        assert result == [[], [], []]
