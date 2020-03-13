import unittest
from hand import Hand



class test_get_rank(unittest.TestCase):

    def test_returns_royal_flush(self):
        royal_flush = "KS AS TS QS JS"

        h = Hand(royal_flush)

        expected = "royal_flush"
        actual = h.get_hand_rank()

        self.assertEquals(actual, expected)

    def test_returns_flush(self):
        flush = "AS 3S 4S 8S 2S"

        h = Hand(flush)

        expected = "flush"
        actual = h.get_hand_rank()
        
        self.assertEquals(actual, expected)


    def test_returns_fullhouse(self):
        full_house = "2S AH 2H AS AC"

        h = Hand(full_house)

        expected = "full_house"
        actual = h.get_hand_rank()
        
        self.assertEquals(actual, expected)


class test_compare(unittest.TestCase):

    def test_flush_less_than_fullhouse(self):

        flush = "AS 3S 4S 8S 2S"
        full_house = "2S AH 2H AS AC"
        
        h_flush = Hand(flush)
        h_house = Hand(full_house)

        self.assertTrue(h_flush < h_house)
        self.assertFalse(h_house < h_flush)

    def test_four_of_a_kind_ace_wins_on_tiebreakers(self):

        four_ace  = "AS AD AC AH 3D"
        four_jack = "JS JD JC JH 3D"

        h_ace = Hand(four_ace)
        h_jack = Hand(four_jack)

        self.assertTrue(h_jack < h_ace)
        self.assertFalse(h_ace < h_jack)


if __name__ == "__main__":
    unittest.main()