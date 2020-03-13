from typing import Tuple, List, Callable
from collections import Counter

from card import Card

class HandRanking:
    
    def __init__(self, rank_sequence: List[int], suit_count: List[int]):
        """
        rank_sequence is simply a list of numerical values for each card
        suit_count is simply a count of times each suit appears. (unordered)

        From these two rules we can derive rank all poker hands, including tiebreakers.

        EXAMPLE 1:

            HAND: 2H 3H 4H 5H 6H"
            
            rank_sequence -> [2, 3, 4, 5, 6]  
            suit_count -> [5]

            since 5 is in suit_count we know the hand is a flush
            and since rank_sequence is ordered sequentially we know its a straight.
            A 'straight flush' occurs when both of the above conditions are met.

        EXAMPLE 2:

            HAND: "JS JD JC JH 3D"

            rank_sequence -> [11, 11, 11, 3]
            suit_count -> [2, 1, 1, 1]           (#1 spades, #2 diamonds, ... )

            from rank count we can derive a 'rank_count', which would be [4, 1]  (#4 Jacks, #1 3)
            And since rank_count contains 4 we know that the hand contains a '4 of a kind'. 

        ----------------------------------------------------------------------------------------------
        Tiebreaker rules: https://www.adda52.com/poker/poker-rules/cash-game-rules/tie-breaker-rules

            As an implementation detail, there are two basic rules for tiebreakers. 
            For hands like a 'straight flush' its simply highest card wins.
            For 'two pair', its highest pair, second highest pair, then highest card wins.

            The first case is simply solved simply by sorting. The 2nd case can be done by
            using a 'stable sort'; that is, we sort first by count and then value.  
        """

        assert len(rank_sequence) == 5, "Error, rank_sequence should be of length 5"
        assert sum(suit_count) == 5, "Error, incorrect number of suits"

        self._rank_sequence = rank_sequence
        self._rank_count = list(Counter(rank_sequence).values())
        self._suit_count = suit_count

        self.__tiebreaker_rule_high_card_wins = sorted(rank_sequence, reverse=True)
        self.__tiebreaker_rule_highest_sequence_wins =  sorted(rank_sequence, key= lambda x: (-rank_sequence.count(x), -x))
        
    
    def high_card(self) -> Tuple[int, List[int]]: 
        return max(self._rank_sequence), self.__tiebreaker_rule_high_card_wins

    def flush(self) -> Tuple[bool, List[int]]: 
        return 5 in self._suit_count, self.__tiebreaker_rule_high_card_wins
    
    def four_of_a_kind(self) -> Tuple[bool, List[int]]:   
        return 4 in self._rank_count, self.__tiebreaker_rule_highest_sequence_wins

    def three_of_a_kind(self) -> Tuple[bool, List[int]]:
        return (3 in self._rank_count, self.__tiebreaker_rule_highest_sequence_wins)

    def two_pair(self) -> Tuple[bool, List[int]]: 
        return (self._rank_count.count(2) == 2, self.__tiebreaker_rule_highest_sequence_wins)

    def pair(self) -> Tuple[bool, List[int]]: 
        # Note that pair looks specifically for a '2' in _rank_count
        # This means that pair will return false if there are three or four copies of the same card.
        return (2 in self._rank_count, self.__tiebreaker_rule_highest_sequence_wins)

    def straight(self) -> Tuple[bool, List[int]]:

        sorted_hand = sorted(self._rank_sequence)
        prev_val = sorted_hand[0]
        for card_rank in sorted_hand[1:]:
            if card_rank - 1 != prev_val:
                return (False, [])
            prev_val = card_rank
            
        return (True, self.__tiebreaker_rule_high_card_wins)
            
    def straight_flush(self) -> Tuple[bool, List[int]]: 
        is_flush, _  = self.flush()
        is_straight, _ = self.straight()

        return is_flush and is_straight, self.__tiebreaker_rule_high_card_wins
        
    def royal_flush(self) -> Tuple[bool, List[int]]: 

        is_straight_flush, _ = self.straight_flush()
        is_ace_high = max(self._rank_sequence) == Card.ACE_HIGH

        return is_straight_flush and is_ace_high, [0] # No Tiebreaker for royal flush
        
    def full_house(self) -> Tuple[bool, List[int]]: 
        
        is_three_of_a_kind, _ = self.three_of_a_kind()
        is_pair, _ = self.pair()

        return is_three_of_a_kind and is_pair, self.__tiebreaker_rule_highest_sequence_wins
        
    @staticmethod
    def texasholdem_hand_rankings() -> List[str]:
        """
        In order of Highest to lowest

        Note that we return function.__name__ rather than using raw strings such as "royal flush".
        This is a deliberate design choice with maintainability in mind (i.e. this will update as functions are renamed, strings would not)
        """
        return [
            HandRanking.royal_flush.__name__,
            HandRanking.straight_flush.__name__,
            HandRanking.four_of_a_kind.__name__,    
            HandRanking.full_house.__name__,
            HandRanking.flush.__name__,
            HandRanking.straight.__name__,
            HandRanking.three_of_a_kind.__name__,   
            HandRanking.two_pair.__name__,          
            HandRanking.pair.__name__,
            HandRanking.high_card.__name__
        ]
