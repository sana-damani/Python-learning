# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck = 0
player_hand = 0
dealer_hand = 0
player_pos = [0, 0]
dealer_pos = [0, 100]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self, hide = False):
        self.cardList = []
        self.hasAce = False
        self.hide = hide

    def __str__(self):
        string = "Hand contains"
        for card in self.cardList:
            string += " "
            string += str(card)
        return string

    def hide_card(self):
        self.hide = True

    def reveal_card(self):
        self.hide = False

    def add_card(self, card):
        self.cardList.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        handValue = 0
        for card in self.cardList:
            if card.get_rank() == 'A':
                self.hasAce = True
            handValue += VALUES[card.get_rank()]
        if self.hasAce and handValue + 10 < 21:
            handValue += 10
        return handValue
   
    def draw(self, canvas, pos):
        i = 0
        for card in self.cardList:
            if self.hide and i == 0:
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
            else:    
                card.draw(canvas, pos)
            pos[0] += 15
            i += 1

    
# define deck class 
class Deck:
    def __init__(self):
        self.cardList = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cardList.append(card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cardList)

    def deal_card(self):
        return self.cardList.pop()

    def __str__(self):
        string = "Deck contains"
        for card in self.cardList:
            string += " "
            string += str(card)
        return string


#define event handlers for buttons
def deal():
    global score, outcome, in_play, deck, player_hand, dealer_hand

    if in_play:
        score -= 1
        outcome = "You lose!"
        
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    deck.shuffle()
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    outcome = "Hit or Stand?"

    dealer_hand.hide_card()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    in_play = True

def hit():
    global score, in_play, outcome
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted!"
            score -= 1
            in_play = False
        else:
            outcome = "Hit or Stand?"
            
def stand():
    global in_play, score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        dealer_hand.reveal_card()
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21 or dealer_hand.get_value() < player_hand.get_value():
            outcome = "You win!"
            score += 1
        else:
            outcome = "You lose!"
            score -= 1
        in_play = False


# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACKJACK", [200, 50], 40, "Black")
    canvas.draw_text(outcome, [200, 300], 40, "Red")
    canvas.draw_text("Score:" + str(score), [500, 50], 20, "Black")

    player_hand.draw(canvas, [200, 400])
    dealer_hand.draw(canvas, [200, 100])    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
