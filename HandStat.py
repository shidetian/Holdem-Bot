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
        if self.num != 14:
            return self.num + self.suit * 13 -1
        if self.num == 14:
            return 1+ self.suit*13 -1
        
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
    #stage: 0=preflop, 1=flop, 2=turn, 3=river, 4=end
    def __init__(self, lowLimit, highLimit, numRaisesAllows = 4, debug=False):
        self.debug = debug;
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        self.numRaisesAllowed = 4;
        self.raisesCurrentRound = 0;
        self.raisesCalled = [0,0]
        self.roundNum = 0
        self.stage = 0
        self.players = [Player(0, 0), Player(1, 0)]
        self.deck = self.genDeck()
        self.hasDelt = False
        self.turn = True #true for player A and false for player B
        self.table=[]
        self.pot = 0;
        self.actionRequired = 2
        self.deal();
    def genDeck(self):
        deck = []
        for num in range(13):
            for suit in range (4):
                deck.append(Card(num+2, suit))
        shuffle(deck) #this is actually not necessary
        return deck
    def drawCard(self):
        nextCard = random.choice(self.deck)
        self.deck.remove(nextCard)
        return nextCard
    def deal(self, debug=False):
        if self.hasDelt:
            print "DEBUG: Deal called twice in a round"
            return
        if self.stage==0: #preflop
            for player in self.players:
                player.cards = (self.drawCard(), self.drawCard())
            if debug:
                print "Player zereo's hand: "
                print self.players[0].cards
                print "Player one's hand: "
                print self.players[1].cards
        elif self.stage==1: #flop
            self.table.append(self.drawCard())
            self.table.append(self.drawCard())
            self.table.append(self.drawCard())
            if debug:
                print "Flop: "
                print self.table
        elif self.stage==2: #turn
            self.table.append(self.drawCard())
            if debug:
                print "Turn: "
                print self.table
        elif self.stage==3: #turn
            self.table.append(self.drawCard())
            if debug:
                print "River: "
                print self.table
        self.hasDelt = True
    #input: pocket cards for A, B, and table cards
    #outputs: tuple of scores (A wins if A>B)
    def checkWinnerM(self, pocketA, pocketB, table):
        maxA = 0;
        maxB = 0;
        cardA = [pocketA[0], pocketA[1]]+table #concat array
        cardB = [pocketB[0], pocketB[1]]+table
        for handA in itertools.combinations(cardA, 5):
            #print handA
            temp = Hand(handA).convert().ranking()
            if temp > maxA:
                maxA = temp
        for handB in itertools.combinations(cardB, 5):
            temp = Hand(handB).convert().ranking()
            if temp > maxB:
                maxB = temp
        return (maxA, maxB)
    #calls checkWinnerM for current game
    #returns a tuple of the hand values for a finished game
    def checkWinner(self):
        if self.stage!=4:
            print "Round not over or folded halfway"
            return
        return self.checkWinnerM(self.players[0].cards, self.players[1].cards, self.table)
    def playerCheckCall(self, playerNum):
        if self.stage==4:
            print "DEBUG: Round already over, no more actions allowed"
            return
        if self.turn!=playerNum:
            print "DEBUG: Not this player's turn"
            return
        if self.actionRequired <= 1:
            if self.stage ==3:
                print "Game finished"
                self.stage+=1
                print self.checkWinner()
            else:
                if self.stage>=2: #ie turn or river, use big bet
                    self.pot += self.raisesCurrentRound * self.highLimit
                else:
                    self.pot += self.raisesCurrentRound * self.lowLimit
                self.turn = not self.turn
                self._endStage_()
        else:
            self.actionRequired -= 1
            self.turn = not self.turn
    def playerRaise(self, playerNum):
        if self.stage==4:
            print "DEBUG: Round already over, no more actions allowed"
            return
        if self.turn!=playerNum:
            print "DEBUG: Not this player's turn"
            return
        if self.raisesCurrentRound==self.numRaisesAllowed:
            print "DEBUG: Max raises for this stage has been reached"
            return
        #assuming infinite cash
        #if self.players[playerNum].cash < self.highLimit:
        #    print "DEBUG: Not enough cash!"
        #    return
        #self.players[playerNum].cash -= self.highLimit
        if self.raisesCurrentRound!=0:
            self.raisesCalled[playerNum]+=1
        self.raisesCurrentRound+=1
        self.actionRequired-=1
        #self.actionRequired += 1
        self.turn = not self.turn
    def playerFold(self, playerNum):
        if self.stage==4:
            print "DEBUG: Round already over, no more actions allowed"
            return
        if self.turn!=playerNum:
            print "DEBUG: Not this player's turn"
            return
        if stage>=2:
            print "Player %d won %d"%(not self.turn, self.pot + (self.raisesCalled[not self.turn] * self.highLimit))
            self.players[not self.turn].cash += self.pot + (self.raisesCalled[not self.turn] * self.highLimit)
        else:
            print "Player %d won %d"%(not self.turn, self.pot + (self.raisesCalled[not self.turn] * self.lowLimit))
            self.players[not self.turn].cash += self.pot + (self.raisesCalled[not self.turn] * self.lowLimit)
        self.stage=4;
        self.actionRequired = -1;
        self.raisesCurrentRound = self.numRaisesAllowed;
        self.turn = not self.turn
    def allowableActions(self,playerNum):
        if self.turn!=playerNum or self.stage==4:
            return (False,False,False,False)
        foldAllowed = True #allow fold?
        checkAllowed = (self.raisesCalled[playerNum]==self.raisesCalled[not playerNum])
        callAllowed = (self.raisesCalled[playerNum]!=self.raisesCalled[not playerNum])
        raiseAllowed = (self.raisesCurrentRound<self.numRaisesAllowed)
        return (checkAllowed, callAllowed, raiseAllowed, foldAllowed)
    def performOneRound(self):
        #Deals player hands
        self.playerCheckCall(1)
        self.playerCheckCall(0)
        #Deals flop
        self.playerCheckCall(1)
        self.playerCheckCall(0)
        #Deals turn
        self.playerCheckCall(1)
        self.playerCheckCall(0)
        #Deals river
        self.playerCheckCall(1)
        self.playerCheckCall(0)
        #self.checkWinner()
        
    #you should now call these functions to progress the game state
    def endRound(self):
        self.hasDelt = False
        self.actionRequired = 2
        self.stage = 0
        self.pot = 0
        self.raisesCurrentRound = 0
        self.raisesCalled = [0,0]
        self.table = []
        self.deck = self.genDeck()
        self.deal(self.debug)
    def _endStage_(self):
        self.hasDelt = False
        self.actionRequired = 2
        self.raisesCurrentRound=0
        self.raisesCalled = [0,0]
        self.stage+=1
        self.stage%=4;
        self.deal(self.debug)

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

import numpy as np
import UnbiasedNet

class HandStat:
    '''
    Given a list of Card objects, analyze features like
    number of high cards, number of pairs,
    connected and suited
    '''
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards
        self.board = []

    def rank_list(self, cards=None):
        if cards is None:
            cards = self.cards
        return [card.num for card in cards]

    def suit_list(self, cards=None):
        if cards is None:
            cards = self.cards
        return [card.suit for card in cards]

    def update_board(self, cards=None, card=None):
        if card is None:
            self.board.extend(cards)
        else:
            self.board.append(card)

    def stat(self, cards=None, features=None):
        if cards is None:
            cards = self.cards
        stats = {}
        suits = self.suit_list(cards)
        ranks = self.rank_list(cards)
        if 14 in ranks:
            ranks.append( 1 ) # ace can be 1 in a wheel straight
        ranks = sorted( ranks )
        distances = [ ranks[i+1] - ranks[i] for i in range(len(ranks)-1) ]
        #------------Preflop's hand------------------------
        if len(cards) >= 2:
            stats['pair'] = int( distances.count(0) > 0 )    
            stats['2-connected'] = distances.count(1) + distances.count(2)
            suitCount = [suits.count(i) for i in range(4)]
            stats['2-suited'] = int( max(suitCount) >= 2 )
            stats['1-high'] = int( ranks[-1] > 12 )
            stats['2-high'] = int( ranks[-2] > 8 )

        #------------Flop's board------------------
        if len(cards) >= 3:
            stats['pairs'] = int( distances.count(0) > 1 ) # 3-of-a-kind too
            stats['3-suited'] = int( max(suitCount) >= 3 )
            # Find sum of consecutive distances for nonpair
            distanceSum = []
            stats['3-of-a-kind'] = 0 # or 4-of-a-kind
            for i in range(len(distances) - 1):
                if distances[i]>0 and distances[i+1]>0:
                    distanceSum.append( distances[i+1] + distances[i] )
                elif distances[i]==0 and distances[i+1]==0:
                    stats['3-of-a-kind'] = 1
            if distanceSum == []:
                distanceSum = [0] # to prevent min from raising error
            stats['3-connected'] = int( min(distanceSum) < 5 )
            stats['3-high'] = int( ranks[-3] > 7 )
        #-----------Turn's board--------------------
        if len(cards) >= 4:
            stats['4-suited'] = int( max(suitCount) >= 4 )
            distanceSum = [ distances[i+2] + distances[i+1] +
                            distances[i] for i in
                            range(len(distances) - 2) if
                            (distances[i]>0 and distances[i+1]>0
                             and distances[i+2]>0) ]
            if distanceSum == []:
                distanceSum = [0]
            stats['4-connected'] = int( min(distanceSum) < 5 )
        #----------River's board------------------------
        if len(cards) >= 5:
            stats['5-suited'] = int( max(suitCount) >= 5 )
            distanceSum = [ sum(distances[i+k] for k in range(4))
                            for i in range(len(distances) - 3) if
                            (distances[i]>0 and distances[i+1]>0
                             and distances[i+2]>0 and
                             distances[i+3]>0) ]
            if distanceSum == []:
                distanceSum = [0]
            stats['5-connected'] = int( min(distanceSum) < 5 )

        if features is None:
            return stats
        else:
            return [stats[key] for key in features]

    # 5 preflop features
    #
two_features = ['pair', '1-high', '2-high', '2-connected', '2-suited']
three_features = two_features.extend( ['pairs', '3-high', '3-connected',
                            '3-suited', '3-of-a-kind'] )
four_features = three_features.extend( ['4-suited',
                            '4-connected'] )
five_features = four_features.extend( ['5-suited', '5-connected'] )
final_features = ['pair', '1-high', '2-high', 'pairs', '3-of-a-kind',
                  '5-suited', '5-connected']

vec_keys = {'my preflop': np.zeros(len(two_features)),
            'flop': np.zeros(len(three_features)),
            'my flop': np.zeros(len(five_features)),
            'turn': np.zeros(len(four_features)),
            'my turn': np.zeros(len(five_features)),
            'river': np.zeros(len(five_features)),
            'my river': : np.zeros(len(final_features))}


class StatStatus:
    '''
    vec_cards for vector of the cards' statistics 1 row for each stage
    At stage 0, only features in two_features are updated for all 4 rows
    At stage 1, more_features, 2 of them (1 for all 5 cards and 1 for
    the 3 table cards only), are updated for last 3 rows.
    #dealer=0 means not dealer, 
    #vec_act stands for action, is of dim 4*3, row corresponds to stage
    #column i is the bet of player i, 1<=i <=2; column 3 indicates whether 
    #this stage is over
    '''
    def __init__(self, dealer=0):
        self.vec_cards = {'my preflop': np.zeros(len(two_features)),
                        'flop': np.zeros(len(three_features)),
                        'my flop': np.zeros(len(five_features)),
                        'turn': np.zeros(len(four_features)),
                        'my turn': np.zeros(len(five_features)),
                        'river': np.zeros(len(five_features)),
                        'my river': : np.zeros(len(final_features))}
        self.d=dealer
        self.vec_act=np.zeros((4,3))
        self.stage=0;
        self.cards = None
    def longvec(self):
        #this just concatenate the vectors
        return np.concatenate([ self.vec_cards['my preflop'],
                    self.vec_cards['flop'], self.vec_cards['my flop'],
                    self.vec_cards['turn'], self.vec_cards['my_turn'],
                    self.vec_cards['river'], self.vec_cards['my_river'],
                               np.array([self.dealer]),
                               self.vec_act[0], self.vec_act[1],
                               self.vec_act[2], self.vec_act[3],
                               np.array([self.stage])])
    def copy(self):
        new_one= Status()
        new_one.vec_cards=1*self.vec_cards
        new_one.dealer=1*self.dealer
        new_one.vec_act=1*self.vec_act
        new_one.stage=1*self.stage
        return new_one
    
    def update_preflop(self, cards):
        self.cards = cards # needed later
        hand = HandStat( cards=cards )
        self.vec_cards['my preflop'] = hand.stat( features=two_features )
        
    def update_flop(self, table):
        #table is a list of Cards
        board = HandStat(table)
        self.vec_cards['flop'] = board.stat( features=three_features )
        my = HandStat( self.cards.extend(table) )
        self.vec_cards['my flop'] = my.stat( features=five_features )        
        self.stage=1
        
    def update_turn(self, table):
        board = HandStat(table)
        self.vec_cards['turn'] = board.stat( features=four_features )
        my = HandStat( self.cards.extend(table) )
        self.vec_cards['my turn'] = my.stat( features=five_features )
        self.stage=2
        
    def update_river(self, table):
        board = HandStat(table)
        self.vec_cards['river'] = board.stat( features=five_features )
        my = HandStat( self.cards.extend(table) )
        self.vec_cards['my river'] = my.stat( features=final_features )
        self.stage=3
        
    def check_fold(self):
        #go fraom one status to another status throught check/fold
        new_stat=self.copy()
        stage=self.stage
        new_stat.vec_act[stage]=(1*np.array([self.vec_act[stage][0], 
                                           self.vec_act[stage][1], 1]))
        new_stat.stage=stage+1
        return new_stat
    
    def check_first(self):
        #this happens when you are the first one to act and you check
        new_stat=self.copy()
        stage=self.stage
        new_stat.vec_act[stage]=(1*np.array([self.vec_act[stage][0], 
                                           self.vec_act[stage][1], 0])) 
        return new_stat
    def call(self):
        #calls
        new_stat=self.copy()
        stage=self.stage
        if stage==0 and self.vec_act[0][0]==1:
            new_stat.vec_act[stage]=1*np.array([2,2,0])
        else:
            new_stat.vec_act[stage]=(1*np.array([self.vec_act[stage][1], 
                                               self.vec_act[stage][1], 1]))
            new_stat.stage=stage+1
        return new_stat
    def praise(self):
        #raise
        new_stat=self.copy()
        stage=self.stage
        newbet=self.vec_act[stage][1]+basebet(stage)
        new_stat.vec_act[stage]=(1*np.array([newbet,
                                          self.vec_act[stage][1], 0]))
        return new_stat
