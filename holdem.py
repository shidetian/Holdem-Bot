import random
from random import shuffle
from copy import deepcopy
import itertools
class Card:
    #0=Spades (b), 1=heart (r), 2=diamond (r), 3=club (b)
    def __init__(self, num, suit):
        self.num = num;
        self.suit = suit;
    def card_to_number(self):
    #so that one card correspnd to the index in the one-dim array of length 52
        return self.num + self.suit * 13 -1
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
    
    def getCharOfSuit(self, suit):
        if suit==0:
            return "S"
        elif suit==1:
            return "H"
        elif suit==2:
            return "D"
        elif suit==3:
            return "C"
        else:
            return "Bad suit"
    
    def getCardOfNum(self, num):
        if num==14:
            return 'A'
        elif num==11:
            return 'J'
        elif num==12:
            return 'Q'
        elif num==13:
            return 'K'
        elif num==14:
            return 'A'
        elif num==10:
            return 'T'
        else:
            return str(num)
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
                deck.append(Card(num+2, suit))
        shuffle(deck)
        return deck
    def drawCard(self):
        nextCard = random.choice(self.deck)
        self.deck.remove(nextCard)
        return nextCard
    def deal(self):
        if self.hasDelt:
            print "DEBUG: Deal called twice in a round"
            return
        if self.stage==0: #preflop
            for player in self.players:
                player.cards = (self.drawCard(), self.drawCard())
            print "Player zereo's hand: "
            print self.players[0].cards
            print "Player one's hand: "
            print self.players[1].cards
        elif self.stage==1: #flop
            self.table.append(self.drawCard())
            self.table.append(self.drawCard())
            self.table.append(self.drawCard())
            print "Flop: "
            print self.table
        elif self.stage==2: #turn
            self.table.append(self.drawCard())
            print "Turn: "
            print self.table
        elif self.stage==3: #turn
            self.table.append(self.drawCard())
            print "River: "
            print self.table
        self.hasDelt = True
    def checkWinner(self):
        #self.checkWinnerM(self.players[0], self.players[1], self.table)
        self.__endRound__()
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
    def performOneRound(self):
        #Deals player hands
        self.deal()
        self.__endStage__()
        #Deals flop
        self.deal()
        self.__endStage__()
        #Deals turn
        self.deal()
        self.__endStage__()
        #Deals river
        self.deal()
        self.checkWinner()
        
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

def adaptCards(cards):
    out = []
    for card in cards:
        out.append(card.getCardOfNum(card.num)+card.getCharOfSuit(card.suit))
    return out
def emulateRound(game):
    #Deals player hands
    game.deal()
    game.__endStage__()
    #Deals flop
    game.deal()
    game.__endStage__()
    #Deals turn
    game.deal()
    game.__endStage__()
    #Deals river
    game.deal()
    cardA = deepcopy(game.table)
    cardA.append(game.players[0].cards[0])
    cardA.append(game.players[0].cards[1])
    
    cardB = deepcopy(game.table)
    cardB.append(game.players[1].cards[0])
    cardB.append(game.players[1].cards[1])
    maxA = ()
    maxB = ()
    for handA in itertools.combinations(cardA, 5):
        #print handA
        temp = Hand(handA).convert().ranking()
        if temp > maxA:
           maxA = temp
    for handB in itertools.combinations(cardB, 5):
        temp = Hand(handB).convert().ranking()
        if temp > maxB:
           maxB = temp     
    print maxA>maxB
    print maxA
    print maxB
    game.__endRound__()

class Hand():
    def __init__(self, listOfCards):
        self.listOfCards = listOfCards
        self.ranks = []
        self.suits = []
        
    def convert(self):
        #self.listOfCards = ((5, 0), (9, 2), (14, 3), (12, 3), (8, 1))
        self.ranks = sorted([r.num for r in self.listOfCards])
        self.ranks.reverse()
        self.suits = [r.suit for r in self.listOfCards]
        return self

    def kind(self, n, biggest=1):
        count = 0
        prevRank = 0
        for r in self.ranks:
            if self.ranks.count(r) == n:
                if prevRank != r:
                    count += 1
                if count == biggest:
                    return (True, r)
            prevRank = r
        return (False,)

    def ranking(self):
        
        flush = len(set(self.suits)) == 1
        straight = (max(self.ranks)-min(self.ranks))==4 and len(set(self.ranks))==5


        if straight and flush:
            return 9, self.ranks
        if self.kind(4)[0]:
            
            return 8, self.kind(4)[1], self.kind(1)[1]
        if self.kind(3)[0] and self.kind(2)[0]:
            return 7, self.kind(3)[1], self.kind(2)[1]
        if flush:
            return 6, self.ranks
        if straight:
            return 5, self.ranks
        if self.kind(3)[0]:
            return 4, self.kind(3)[1], self.kind(1)[1], self.kind(1, 2)[1]
        if self.kind(2)[0] and self.kind(2, 2)[0]:
            return 3, self.kind(2)[1], self.kind(2, 2)[1], self.kind(1)[1]
        if self.kind(2)[0]:
            return 2, self.kind(2)[1], self.kind(1,1)[1], self.kind(1,2)[1], self.kind(1,3)[1]
        return 1, self.ranks
'''
for line in file("poker.txt"):
    print Hand(line[0:14]).convert().ranks, Hand(line[15:29]).convert().ranks
    print Hand(line[0:14]).convert().ranking(), Hand(line[15:29]).convert().ranking()
'''
