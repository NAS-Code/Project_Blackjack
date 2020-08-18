import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__ (self):
        return self.rank + ' of ' + self.suit

class Deck:

    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.deck.append(created_card)

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has: ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        # card passed in
        # from Deck.deal() --> single Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]

        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        # IF TOTAL VALUE > 21 AND I STILL HAVE AN ACE
        # THEN CHANGE MY ACE TO BE A 1 INSTEAD OF AN 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet?: "))
        except:
            print ("Sorry, please provide an integer")
        else:
            if chips.bet > chips.total:
                print("Sorry you dont have enough chips. You only have: {}".format(chips.total))
            else:
                break

def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Hit or Sand? Enter H or S: " )
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() =="s":
            playing = False
            print ('Player Stands, Dealer turn')
        else:
            print ("Sorry that is an incompatible command, please enter H or S")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(player,dealer,chips):
    print ("Player busted!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print ("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Player wins! Dealer busted!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()

def push(player,dealer):
    print ("dealer and player tie! Push!")

def play_again():
    new_game = input("Would you like to play another hand? Yes or No: ")
    if new_game[0].lower() == 'y':
        playing = True
        return playing
    elif new_game[0].lower() == 'n':
        playing = False
        return playing
    else:
        return play_again()

# PROGRAM LOGIC

while True:
    print ("Welcome to blackjack")
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()

    take_bet(player_chips)

    show_some(player_hand, dealer_hand)
    playing = True
    while playing:
        hit_or_stand(deck,player_hand)
        show_some(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(deck,dealer_hand)
            show_all(player_hand, dealer_hand)
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
            else:
                push(player_hand, dealer_hand)
    print("\n Player total chips are at: {}".format(player_chips.total))
    if play_again() == False:
            break