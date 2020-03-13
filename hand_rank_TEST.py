import unittest
from hand import HandRanking

# ACE_HIGH = 14
# ACE_LOW = 1
# face_card_to_int = {"T": 10, "J": 11, "Q": 12, "K": 13}

class test_handRanking(unittest.TestCase):
    
    def test_royal_flush_returns_true(self):

        # "KS AS TS QS JS"
        rank_sequence = [13, 14, 10, 12, 11]
        suit_count = [5]

        h = HandRanking(rank_sequence, suit_count)

        is_royal_flush, _ = h.royal_flush()

        self.assertTrue(is_royal_flush)

    def test_royal_flush_returns_false(self):

        # "JS JD JC JH 3D"
        rank_sequence = [11, 11, 11, 11, 3]
        suit_count =    [2, 1, 1, 1]

        h = HandRanking(rank_sequence, suit_count)

        is_royal_flush, _ = h.royal_flush()

        self.assertFalse(is_royal_flush)

    def test_four_of_a_kind_returns_true(self):
        
        # "JS JD JC JH 3D"
        rank_sequence = [11, 11, 11, 11, 3]
        suit_count =    [2, 1, 1, 1]

        h = HandRanking(rank_sequence, suit_count)
        is_four_of_a_kind, _ = h.four_of_a_kind()

        self.assertTrue(is_four_of_a_kind)

    def test_four_of_a_kind_returns_false(self):
        
        # "KS AS TS QS JS"
        rank_sequence = [13, 14, 10, 12, 11]
        suit_count = [5]

        h = HandRanking(rank_sequence, suit_count)
        is_four_of_a_kind, _ = h.four_of_a_kind()

        self.assertFalse(is_four_of_a_kind)


if __name__ == "__main__":
    unittest.main()