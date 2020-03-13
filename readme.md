# Poker Hand Ranking

Takes a poker hand (or a collection of poker hands) and evalutate how hand rank. 

For the tiebreaker rules used see here:
https://www.adda52.com/poker/poker-rules/cash-game-rules/tie-breaker-rules

Based on "Sortable Poker Hands", a 4th Kyu problem with can be found on codewars.com.
https://www.codewars.com/kata/586423aa39c5abfcec0001e6

The code will parse a poker hand as a space-seperated string where each card is represented as a 2-character string <value, suit>. For example:

Royal Flush: "KS AS TS QS JS"
Straight_Flush: "2H 3H 4H 5H 6H"

## Example useage

### Evaluating a hand

>>> h.Hand("2H 3H 4H 5H 6H") 
>>> h.get_hand_rank()
"straight_flush"
	
### Comparing Hands

>>> Hand("AS AD AC AH JD") < Hand("JS JD JC JH 3D")
False # four of a kind, where ace high beats 4 jacks. 

