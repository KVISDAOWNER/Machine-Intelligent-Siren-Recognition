from unittest import TestCase
from clip_split import cut


class TestCut(TestCase):
    def test_cut1(self):  # fail
        # arrange
        trainls = [[1,2,3], [1,2], [1]]
        testls = [[1,2,3], [1,2,3], [1,2]]
        # act
        resulttrain, resulttest = cut(trainls, testls)

        # assert
        assert resulttrain == [[1], [1], [1]] and resulttest == [[1], [1], [1]]

    def test_cut2(self):  # fail
        # arrange
        trainls = [[1,2,3], [1,2], [1,2]]
        testls = [[1,2,3], [1,2], [1]]
        # act
        resulttrain, resulttest = cut(trainls, testls)

        # assert
        assert resulttrain == [[1], [1], [1]] and resulttest == [[1], [1], [1]]

    def test_cut3(self):  # fail
        # arrange
        trainls = [[1,2,3], [1,2,3], [1,2,3]]
        testls = [[1,2,3], [1,2,3], [1,2,3]]
        # act
        resulttrain, resulttest = cut(trainls, testls)

        # assert
        assert resulttrain == [[1,2,3], [1,2,3], [1,2,3]] and resulttest == [[1,2,3], [1,2,3], [1,2,3]]