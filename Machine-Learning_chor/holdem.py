from random import shuffle
class Card:
    #0=Spades (b), 1=heart (r), 2=diamond (r), 3=club (b)
    def __init__(self, num, suit):
        self.num = num;
        self.suit = suit;
    def getStringOfSuit(self, suit):
        if suit==0:
            return "Spades"
        elif suit==1:
            return "Hearts"
        elif suit==2:
            return "Diamond"
        elif suit==3:
            return "Club"
        else:
            return "Bad suit"
    def binary(self):
        return self.num*4 + self.suit
    def __eq__(self, other):
        return (self.num==other.num and self.suit==other.suit)
    def __str__(self):
        return str(self.num) + " of " + self.getStringOfSuit(self.suit)
    def __repr__(self):
        return repr((self.num, self.suit))
class Player:
    def __init__(self, playerNum, cash):
        self.playerNum = playerNum
        self.cards = ()
        self.cash = cash
        
class Holdem:
    #stage: 0=preflop, 1=flop, 2=turn, 3=river
    def __init__(self, lowLimit, highLimit, startCash):
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        self.roundNum = 0
        self.stage = 0
        self.players = [Player(0, startCash), Player(1, startCash)]
        self.deck = self.genDeck()
        self.hasDelt = False
        self.turn = True #true for player A and false for player B
        self.table=[]
        self.pot = 0;
    def genDeck(self):
        deck = []
        for num in range(13):
            for suit in range (4):
                deck.append(Card(num+1, suit))
        shuffle(deck)
        return deck
    def deal(self):
        if self.hasDelt:
            print "DEBUG: Deal called twice in a round"
            return
        if self.stage==0: #preflop
            for player in self.players:
                player.cards = (self.deck.pop(), self.deck.pop())
            print "Player one's hand: "
            print self.players[0].cards
            print "Player two's hand: "
            print self.players[1].cards
        elif self.stage==1: #flop
            self.table.append(self.deck.pop())
            self.table.append(self.deck.pop())
            self.table.append(self.deck.pop())
            print "Flop: "
            print self.table
        elif self.stage==2: #turn
            self.table.append(self.deck.pop())
            print "Turn: "
            print self.table
        elif self.stage==3: #turn
            self.table.append(self.deck.pop())
            print "River: "
            print self.table
        self.hasDelt = True
    def checkWinner(self):
        #Do checks
        self.__endRound__()
        pass
    def checkFlush(self, cards):
        totals = [0,0,0,0]
        for card in cards:
            totals[card.suit]+=1
        for num in totals:
            if num>=5:
                return True
        return False
    #cards = [Card(0,0), Card(1,0), Card(2,0), Card(3,0), Card(4,0), Card(5,0), Card(6,0)]
    #returns the highest card in the straight (14 if ace), or -1 if none
    def checkStraight(self, cards):
        handSorted = sorted(cards, key=lambda card: card.num)
        found = True
        #handle ace case
        if handSorted[0].num==0 and handSorted[3].num==10:
            for i in range (4, 7):
                if handSorted[i].num != handSorted[i-1].num+1:
                    found = False
                    break
            if found:
                return 14
        #straight can only start in only 3 positions in the sorted list
        for i in range (3, 7):
            if handSorted[i].num != handSorted[i-1].num+1:
                found = False
                break
        if found:
            return handSorted[6].num
        
        found = True
        for i in range(2, 6):
            if handSorted[i].num != handSorted[i-1].num+1:
                found = False
                break
        if found:
            return handSorted[5].num
        
        found = True
        for i in range (1, 5):
            if handSorted[i].num != handSorted[i-1].num+1:
                found = False
                break
        if found:
            return handSorted[4].num
        else:
            return -1
    #returns the 4 of a kind or -1 if none
    def checkFourOfAKind(self, cards):
        handSorted = sorted(cards, key=lambda card: card.num)
        longestSame = 0
        sameCard = -1
        currentLength = 0
        for i in range (1,7):
            if handSorted[i].num==handSorted[i-1].num:
                currentLength+=1
                if currentLength>longestSame:
                    sameCard = handSorted[i].num
                    longestSame = currentLength
            else:
                currentLength=1
        if longestSame>=4:
            if longestSame>4:
                print "5+ of a kind!!?"
            return sameCard
        else:
            return -1
    def playerCheck(self, playerNum):
        if self.turn!=playerNum:
            print "DEBUG: Not this player's turn"
            return
        if self.stage ==4:
            self.checkWinner()
        self.__endStage__()
    def playerRaise(self, playerNum):
        if self.turn!=playerNum:
            print "DEBUG: Not this player's turn"
            return
        if self.players[playerNum].cash < self.highLimit:
            print "DEBUG: Not enough cash!"
            return
        self.players[playerNum].cash -= self.highLimit
        self.pot = self.highLimit
        self.turn = not self.turn
    def playerFold(self, playerNum):
        if self.turn!=playerNum:
            print "DEBUG: Not this player's turn"
            return
        self.players[not self.turn].cash += self.pot
        self.__endRound__()
    #you should not call these functions
    def __endRound__(self):
        self.hasDelt = False
        self.stage = 0
        self.pot = 0
        self.table = []
        self.deck = self.genDeck()
    def __endStage__(self):
        self.hasDelt = False
        self.stage+=1
        self.stage%=4;
        
import numpy as np

#parameters
n_in = 4*52 + 4 + 48 # num of input nodes
n_hidden = 100 # number of hidden nodes
n_out = 1
steps = 8 # max number of times we need to act
GAMMA = 0.9 # discount rate
ALPHA = 1.0 / n_in # 1st layer learning rate
BETA = 1.0 / 100 # 2nd layer learning rate
LAMBDA = 0.5 # < GAMMA. The descent rate?
card_dim = 52

'''
data is formatted as row matrix with first 4*52 entries being card data,
the next four indicates the stage and the rest is the actions
'''
x = np.zeros( (steps, n_in) ) # Keep track of inputs in all steps 

# randomly initialize weights of first and second layer
v = np.random.uniform( -0.5, 0.5, (n_hidden, n_in) )
w = np.random.uniform( -0.5, 0.5, (n_out, n_hidden) )

# I guess we should wait til we have automated the game before proceeding
# ...
game = Holdem(1, 2, 100)
game.deal()
for i in [0,1]:
    game.players[0].cards[i].binary()
cur_step = 0
cur_x = x[ cur_step, : ]
# Update hand data
for i in [0,1]:
    cur_x[ game.players[0].cards[i].binary() ] = 1.0
if not game.turn:
    game.playerCheck(1) # opponent is always check-calling
# update cur_x
pass
# Forward phase of the perceptron
h = np.dot( v, np.transpose(x[ cur_step, : ]) )
h_bool = 1 / (1 + np.exp( - 1*h ))
y = np.dot( w, transpose(h_bool) )