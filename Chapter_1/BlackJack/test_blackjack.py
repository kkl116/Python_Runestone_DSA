import pytest
from blackjack import Card, BlackJackHand

def test_player_point_calculation():
    hand = BlackJackHand()
    #test 3 hands, no ace, one ace, multi ace
    hand_1 = [Card(None, 10), Card(None, 5), Card(None, 5)]
    hand_2 = [Card(None, 'A'), Card(None, 6)]
    hand_3 = [Card(None, 'A'), Card(None, 'A'), Card(None, 7)]

    ans = [(20, 0), (7,17), (9, 19)]

    for h,ans in zip([hand_1, hand_2, hand_3], ans):
        hand.cards = h
        hand.calc_points()
        assert (hand.points_1, hand.points_2) == ans

