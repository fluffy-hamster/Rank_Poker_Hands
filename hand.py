from typing import List, Tuple
from itertools import product
from collections import Counter

from hand_rank import HandRanking
from card import Card

class Hand:

    def __init__(self, hand: str):
        self._hand_interpretations: List[Tuple[Card]] = self._parse_hand(hand)

        self._hand_rank: int
        self._tiebreaker: List[int]
        self._hand: Tuple[Card]

        self._hand_rank, self._tiebreaker, self.hand = self._best_hand(self._hand_interpretations)

    def get_hand_rank(self) -> str:
        ranks = HandRanking.texasholdem_hand_rankings()
        return ranks[len(ranks) - self._hand_rank]

    def _parse_hand(self, hand: str) -> List[Tuple[Card]]: 
        """
        Finds all the possible ways to interpret a hand. In the cases where there are no aces, there is only one interpretation.
        However, when there is one (or several) aces in the hand there are a number of ways to intrepret the hand. 

        e.g "AC KD" -> (AC(low) KD)
                       (AC(high), KD)

        So we return all possible combinations, and let __best_hand figure out the most favourable combination
        """
        hand_lst = []
        for c in hand.split(" "):
            card = Card(c, ace_high=True)

            if card.is_ace():
                card_low_ace = Card(c, ace_high=False)
                tup = (card, card_low_ace)
            else:
                tup = (card,)
                
            hand_lst.append(tup)

        # Note that (in general) using 'product' could be computationally very expensive.
        # However, we expect at most 4 Aces in any given hand, thus the max possible hands should be about 2^4. 
        hand_interpretations = list(product(*hand_lst))
        return hand_interpretations


    def _best_hand(self, interpretations: List[Tuple[Card]]) -> Tuple[int, List[int], Tuple[Card]]:
        """
            For hands without aces, the 'best hand' is just the hand. We assign it a rank and calculate tiebreakers

            For hands with aces, we evaluate all possible scenarios (e.g when the ace is high, when the ace is low)
            and we break the moment we calculate a hand rank (HandRanking.texasholdem_hand_rankings() is ordered best first).
        """

        for rank, func in enumerate(HandRanking.texasholdem_hand_rankings()):
            for hand in interpretations: 

                sequence: List[int] = [card._value for card in hand]
                suits_counts = list(Counter(card._suit for card in hand).values())

                h = HandRanking(sequence, suits_counts)
                is_rank, tiebreaker = getattr(h, func)()
                
                if is_rank:
                    rank = len(HandRanking.texasholdem_hand_rankings()) - rank  # flip logic such that large numbers = good hands.
                    return rank, tiebreaker, hand
                   
        # should never reach here
        raise Exception("Failed to rank hand")

    def __lt__(self, other):
        if self._hand_rank == other._hand_rank:
            # Note that tiebreakers are implemented as lists of numbers
            # thus this comparision takes advantage of default python behavior
            # e.g [1,2,3] < [1,2,4] = True
            return self._tiebreaker < other._tiebreaker
        
        return self._hand_rank < other._hand_rank
        
    def __str__(self):
        return " ".join(str(card) for card in self.hand)
        
    def __repr__(self):
        return str(self)
