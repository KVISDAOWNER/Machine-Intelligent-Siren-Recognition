from unittest import TestCase
import vector as v


class TestVector(TestCase):
    def test_should_create_growth_vector(self):
        # Arrange
        vect = [1, 2, 3, 3, 2, 1]
        expected_growth_vect = [1, 1, 0, -1, -1]

        # Act
        vect = v.get_growth_vector(vect)

        # Assert
        self.assertEqual(vect, expected_growth_vect)

    def test_should_zero_pad_list(self):
        # Arrange
        list = [1]
        expected_pad_list = [0, 1, 0]

        # Act
        list = v.get_zero_padded(list)

        # Assert
        self.assertEqual(expected_pad_list[0], list[0])
        self.assertEqual(expected_pad_list[2], list[2])
