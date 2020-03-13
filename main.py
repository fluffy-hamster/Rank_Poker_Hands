from typing import List
import sys

from hand import Hand

# sorted hands
EXAMPLE = ["KS AS TS QS JS",
           "2H 3H 4H 5H 6H",
           "AS AD AC AH JD",
           "JS JD JC JH 3D",
           "2S AH 2H AS AC",
           "AS 3S 4S 8S 2S"]

if __name__ == "__main__":

    hands: List[Hand] = []

    for str_hand in EXAMPLE:
        h = Hand(str_hand)
        hands.append(h)

    reverse_order = sorted(hands, reverse=True)

    assert hands == reverse_order[::-1], "God f****** damnnit."

    sys.exit(0)
