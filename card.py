from typing import Union

class Card:

    ACE_HIGH = 14
    ACE_LOW = 1

    def __init__(self, card: str, ace_high = True):
        """
        Input:
             Takes a 2-character string representation of a card.
             Where first character denotes the value and second character denotes the suit.
             e.g: 'Ace of Spades' => 'AS', 'Two of Hearts' => '2H'     

             Note also that if the card is an Ace, the ace_high optional param denotes if card is high/low

        Output:
              Card object
        """
                
        assert len(card) == 2, "Expecting cards to be string of length 2"
        
        self._ace_high = ace_high
            
        self._value: int = self._parse_numerical_rank(card[0])
        self._suit: str  = self._parse_suit(card[1])
        
        assert self._value is not None, "Error parsing rank"
        assert self._suit is not None, "Error parsing suit"
        
    def is_ace(self) -> bool:
        return self._value in [Card.ACE_HIGH, Card.ACE_LOW]
    
    def __lt__(self, other) -> bool:
        return self._value < other._value
    
    def __eq__(self, other) -> bool:
        # In Texas holdem', suits have no value, 
        # thus for equality we only need to check for numerical values. 
        return self._value == other._value
        
    def __str__(self):
        return "<CardObj:({},{})>".format(self._value, self._suit)
        
    def _parse_suit(self, character : str) -> Union[str, None]:
        suits = ["S", "C", "H", "D"]
        return character if character.upper() in suits else None
        
    def _parse_numerical_rank(self, character: str) -> Union[int, None]:
        
        if character == "A":
            return Card.ACE_HIGH if self._ace_high else Card.ACE_LOW
        
        face_card_to_int = {"T": 10, "J": 11, 
                            "Q": 12, "K": 13}
        
        if character in face_card_to_int:
            return face_card_to_int[character]
        
        try:
            return int(character)
        except:
            return None
