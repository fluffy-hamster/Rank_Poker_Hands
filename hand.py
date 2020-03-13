from typing import List, Tuple
from itertools import product
from collections import Counter

from hand_rank import HandRanking
from card import Card

class Hand:

    def __init__(self, hand: str):
        self._hand_interpretations: List[Tuple[Card]] = self.__parse_hand(hand)

        self._hand_rank: int
        self._tiebreaker: List[int]
        self._hand: Tuple[Card]

        self._hand_rank, self._tiebreaker, self.hand = self.__best_hand(self._hand_interpretations)

    def __parse_hand(self, hand: str) -> List[Tuple[Card]]: 
        hand_lst = []
        for c in hand.split(" "):
            card = Card(c, ace_high=True)

            if card.is_ace():
                card_low_ace = Card(c, ace_high=False)
                tup = (card, card_low_ace)
            else:
                tup = (card,)
                
            hand_lst.append(tup)

        # The idea here is that when we have an Ace in the hand
        # We evaluate it as 2 hands (one where Ace is High, the other where Ace is low) e.g "AC KD" -> (AC(low) KD),  (AC(high), KD)
        # Note that (in general) using 'product' could be computationally very expensive.
        # However, we expect at most 4 Aces in any given hand, thus the max possible hands should be about 2^4. 
        hand_interpretations = list(product(*hand_lst))
        return hand_interpretations


    def __best_hand(self, interpretations: List[Tuple[Card]]) -> Tuple[int, List[int], Tuple[Card]]:
                
        for rank, func in enumerate(HandRanking.texasholdem_hand_rankings()):
            for hand in interpretations:

                sequence: List[int] = [card._value for card in hand]
                suits_counts = list(Counter(card._suit for card in hand).values())

                tiebreaker: List[int]

                h = HandRanking(sequence, suits_counts)
                is_rank, tiebreaker = getattr(h, func)()
                
                if is_rank:
                    return rank, tiebreaker, hand
                   
        # should never reach here
        raise Exception("Failed to rank hand")

    def get_hand_rank(self) -> str:
        return HandRanking.texasholdem_hand_rankings()[self._hand_rank]

    def __lt__(self, other):
        if self._hand_rank == other._hand_rank:
            # Note that tiebreakers are implemented as numbers
            # thus this comparision takes advantage of default python behaviour
            # e.g [1,2,3] < [1,2,4] = True
            return self._tiebreaker > other._tiebreaker
        
        return self._hand_rank < other._hand_rank # Low rank = good.
        
    def __str__(self):
        return " ".join(str(card) for card in self.hand)
        
    def __repr__(self):
        return str(self)
