#PE 14 - implement card and deck class and implement a card game - I choose blackjack..
#special cases - aces (1/ 11), splitting hands, naturals, dealer one card face down
import random 

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        
    @property
    def is_picture(self):
        if self.number in ['J', 'Q', 'K']:
            return True
        
    def __repr__(self):
        return f"{self.number} of {self.suit}"

    
class Deck:
    def __init__(self, include_jokers=False, shuffled=False):
        #deck characteristics
        self.suits = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
        self.numbers = [str(n) for n in range(2, 11)]
        self.pictures = ['J', 'Q', 'K', 'A']
        self.include_jokers = include_jokers
        self.shuffled = shuffled

        #initialize deck
        self.cards = []
        self.init_deck()
        if self.shuffled:
            self.shuffle_deck()
        
    def init_deck(self):
        for s in self.suits:
            for num in self.numbers + self.pictures:
                self.cards.append(Card(s, num))
        if self.include_jokers:
            self.cards += [Card(None, 'Joker'), Card(None, 'Joker')]

    def shuffle_deck(self):
        random.shuffle(self.cards)
        
    def deal_cards(self, n):
        cards = self.cards[:n]
        self.cards = self.cards[n:]
        return cards


class BlackJackHand:
    def __init__(self, cards=None, is_dealer=False):
        self.cards = cards
        self.bust = False 
        self.active = True
        self.is_dealer = is_dealer
        self.reveal = False
        self.points_1 = None
        self.points_2 = None
        self.is_natural = False

        if cards is not None:
            self.calc_points()
            self.natural_check()
        
        if self.is_dealer:
            self.dealer_points_check()

    
    def hit(self, card):
        self.cards.append(card[0])
        self.calc_points()
        player_name = 'Player' if not self.is_dealer else 'Dealer'

        if self.is_dealer:
            self.dealer_points_check()

        if not self.points_2:
            if self.points_1 == 21:
                print(f"{player_name} has 21 points!")
                self.active = False 
            elif self.points_1 > 21:
                print(f"{player_name} has {self.points_1} points! ***BUSTED***")
                self.bust = True
                self.active = False
            else:
                print(f"{player_name} now has {self.points_1} points.")
        else:
            if self.points_1 == 21 or self.points_2 == 21:
                print(f"{player_name} has 21 points!")
                self.active = False 

            elif self.points_1 > 21:
                print(f"{player_name} has {self.points_1} points! ***BUSTED***")
                self.bust = True
                self.active = False
            else:
                points = [str(p) for p in (self.points_1, self.points_2) if p <= 21]
                points = " OR ".join(points)
                print(f"{player_name} now has {points} points.")
        
    def stand(self):
        if self.is_dealer:
            if self.points_1 < 17:
                print("You're a dealer! You can not stand below 17")
                return
        self.active = False

    def split(self, new_cards):
        #expect 2 new cards
        if self.is_dealer:
            print("You're a dealer! You cannot split!")
            return

        if len(self.cards) == 2:
            if len(set([c.number for c in self.cards])) == 1:
                new_hand = BlackJackHand(cards=[self.cards[1], new_cards[0]])
                self.cards = [self.cards[0], new_cards[1]]
                print(f'Your new hands are {self} and {new_hand}')
                return new_hand
            else:
                print("You do not have a pair!")
                return
        else:
            print("You cannot split hands after initial round!")
            return


    def calc_points(self):
        #Need to deal with Ace cases - 
        rest_of_hand = [c for c in self.cards if c.number != 'A']
        points = 0 
        for card in rest_of_hand:
            val = 10 if card.is_picture else int(card.number)
            points += val
        if len(rest_of_hand) == len(self.cards):
            self.points_1 = points
            self.points_2 = 0
        elif len(rest_of_hand) == len(self.cards) - 1:
            #there is one ace...
            self.points_1 = points + 1
            self.points_2 = points + 11
        elif len(rest_of_hand) < len(self.cards) - 1:
            n_aces = len([c for c in self.cards if c.number == 'A'])
            self.points_1 = points + n_aces
            self.points_2 = points + (n_aces - 1) + 11
        else:
            raise Exception('Something went wrong?')

    def natural_check(self):
        if self.points_2 == 21:
            if not self.is_dealer:
                print("You have a natural!")
            self.active = False
            self.is_natural = True

    def dealer_points_check(self):
        assert self.is_dealer
        valid_points = [p for p in (self.points_1, self.points_2)]
        if max(valid_points) >= 17:
            self.active = False
            print('*** stand ***')


    def __repr__(self):
        return f"BlackJackHand({[card.number for card in self.cards]})"

    def __str__(self):
        if self.is_dealer and self.reveal == False:
            return f"(FACEDOWN) {[c.number for c in self.cards[1:]]}"
        else:
            return f"{[card.number for card in self.cards]}"

        
#special cases - splitting hands, blackjack 
class Player:
    def __init__(self, is_dealer=False, game=None):
        self.wins = 0
        self.losses = 0
        self.hands = []
        self.game = game
        self.is_dealer = is_dealer
        
    def reset(self):
        self.hands = []

    def get_next_action(self):
        valid_actions = ['hit', 'stand', 'split']
        if self.hands:
            for hand in self.hands:
                while hand.active:
                    action = input(f"Your current hand is {hand}, what would you like to do? [hit, stand, split]")
                    if action in valid_actions:
                        print('***', action, '***')
                        #do something with hand
                        if action == 'hit':
                            new_card = self.game.deck.deal_cards(1)
                            hand.hit(new_card)
                        elif action == 'stand':
                            hand.stand()
                        elif action == 'split':
                            new_cards = self.game.deck.deal_cards(2)
                            new_hand = hand.split(new_cards)
                            if new_hand:
                                self.hands.append(new_hand)
                    else:
                        pass
                
        else:
            print("You don't have any active hands!")
            return


class BlackJack:
    def __init__(self):
        self.deck = Deck(shuffled=True)
        self.dealer = Player(is_dealer=True, game=self)
        self.player = Player(is_dealer=False, game=self)
        self.round = 1
    
    def play(self):
        #initial round dealer and player gets 2 cards each 
        print(f"Round {self.round}...")
        print(f"Dealing...")
        self.player.hands.append(BlackJackHand(self.deck.deal_cards(2)))
        self.dealer.hands.append(BlackJackHand(self.deck.deal_cards(2), is_dealer=True))
        assert len(self.player.hands) == 1
        assert len(self.dealer.hands) == 1


        print(f"Dealer hand: {self.dealer.hands[0]}")
        print(f"Player hand: {self.player.hands[0]}")
        print("Player Round...")
        while self.check_active_player_hands():
            self.player.get_next_action()
            #if current hand is bust then dealer wins automatically
            self.player_bust_check()
        
        print("Dealer Round...")
        self.dealer.hands[0].reveal = True
        while self.check_active_dealer_hands():
            print('*** hit ***')
            self.dealer.hands[0].hit(self.deck.deal_cards(1))

        print("Results...")
        dealer_natural = self.dealer.hands[0].is_natural
        dealer_bust = self.dealer.hands[0].bust
        dealer_hand = self.dealer.hands[0]
        for hand in self.player.hands:
            player_points = self.get_hand_final_points(hand)
            if hand.bust:
                #Just print busted hands
                print(f"{hand} went bust ({hand.points_1} points) :( - YOU LOSE")
                continue

            if dealer_bust:
                #automatic player win
                print(f"{hand} ({player_points} points) won! Dealer went bust {dealer_hand}. - YOU WIN")
                self.player.wins += 1
                self.dealer.losses += 1
                continue

            hand_natural = hand.is_natural
            if dealer_natural or hand_natural:
                if hand_natural and dealer_natural:
                    print(f"{hand} is a natural! But dealer also has a natural... {dealer_hand}- TIE GAME")

                elif dealer_natural and not hand_natural:
                    print(f"{hand} has {player_points} points! But dealer had a natural {dealer_hand}... - YOU LOSE")
                    self.player.losses += 1
                    self.dealer.wins += 1

                elif hand_natural and not dealer_natural:
                    print(f"{hand} was a natural! Dealer didn't have a natural {dealer_hand}... - YOU WIN")
                    self.player.wins += 1
                    self.dealer.losses += 1
                continue                                
            
            #no one has a natural or bust - compare points 
            dealer_points = self.get_hand_final_points(self.dealer.hands[0])
            if dealer_points > player_points:
                print(f"Player had {hand} ({player_points} points) and dealer had {dealer_hand} ({dealer_points} points)... - YOU LOSE")
                self.dealer.wins += 1
                self.player.losses += 1
            elif player_points > dealer_points:
                print(f"Player had {hand} ({player_points} points) and dealer had {dealer_hand} ({dealer_points} points)... - YOU WIN")
                self.player.wins += 1
                self.dealer.losses += 1
            elif player_points == dealer_points:
                print(f"Player had {hand} ({player_points} points) and dealer had {dealer_hand} ({dealer_points} points)... - TIE GAME")

        self.outcomes_check()
        self.player.reset()
        self.dealer.reset()
        self.deck.init_deck()
        self.round += 1


    def check_active_player_hands(self):
        return sum([hand.active for hand in self.player.hands])

    def check_active_dealer_hands(self):
        active_dealer = sum([hand.active for hand in self.dealer.hands])
        all_bust = len(self.player.hands) == sum([hand.bust for hand in self.player.hands])
        return active_dealer and not all_bust

    @staticmethod
    def get_hand_final_points(hand):
        valid_points = [p for p in (hand.points_1, hand.points_2) if p <= 21]
        if valid_points:
            return max(valid_points)
        else:
            return 0

    def player_bust_check(self):
        for hand in self.player.hands:
            if hand.bust:
                self.player.losses += 1
                self.dealer.wins += 1

    def outcomes_check(self):
        assert self.player.losses == self.dealer.wins
        assert self.player.wins == self.dealer.losses
                
        

if __name__ == "__main__":
    import pytest
    from test_blackjack import *
    #run test first 
    fail = pytest.main()
    if not fail:
        playing = True
        game = BlackJack()
        while playing:
            n_rounds = int(input("Hi!, how many rounds of blackjack would you like to play?"))
            for _ in range(n_rounds):
                game.play()
            cont = input("Would you like to keep playing? [Yes, No]")
            if cont == 'Yes':
                continue
            elif cont == 'No':
                playing = False 
        print(f"Wins: {game.player.wins}, losses: {game.player.losses}")

        