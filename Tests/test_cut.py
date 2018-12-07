from unittest import TestCase
from clip_split import cut


class TestCut(TestCase):
    def test_cut1(self):  # fail
        # arrange
        ls = [[1,2,3], [1,2], [1]]

        # act
        result = cut(ls)

        # assert
        assert result == [[1], [1], [1]]

    def test_cut2(self):
        # arrange
        ls = [[1, 2, 3], [1, 2], []]

        # act
        result = cut(ls)

        # assert
        assert result == [[], [], []]

    def test_cut3(self):  # fail
        # arrange
        ls = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]

        # act
        result = cut(ls)

        # assert
        assert result == [[1, 2, 3], [1, 2, 3], [1, 2, 3]]

    def test_cut4(self):  # fail
        # arrange
        ls = [[1, 2], [1, 2, 3, 4], [1, 2, 3], [1, 2, 3, 4]]

        # act
        result = cut(ls)

        # assert
        assert result == [[1, 2], [1, 2], [1, 2], [1, 2]]
