import random
from random import shuffle
from copy import deepcopy
import itertools
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
        self.checkWinnerM(self.players[0], self.players[1], self.table)
        self.__endRound__()
    #returns 0 if playerA won, or 1 if playerB, [or -1 if tie (currently not implemented)]
    def checkWinnerM(self, playerA, playerB, table):
        cardA = deepcopy(table)
        cardA.append(playerA.cards[0])
        cardA.append(playerA.cards[1])
        
        cardB = deepcopy( table )
        cardB.append(playerB.cards[0])
        cardB.append(playerB.cards[1])
        
        flushStraightA = self.checkFlushStraight(cardA)
        flushStraightB = self.checkFlushStraight(cardB)
        
        fourKindA = self.checkFourOfAKind(cardA)
        fourKindB = self.checkFourOfAKind(cardB)
        
        fullHouseA = self.checkFullHouse(cardA)
        fullHouseB = self.checkFullHouse(cardB)
        
        flushA = self.checkFlush(cardA)
        flushB = self.checkFlush(cardB)
        
        straightA = self.checkStraight(cardA)
        straightB = self.checkStraight(cardB)
        
        threeA = self.checkThreeOfKind(cardA)
        threeB = self.checkThreeOfKind(cardB)
        
        pairA = self.checkPair(cardA)
        pairB = self.checkPair(cardB)
        
        highA = self.checkHighCard(cardA)
        highB = self.checkHighCard(cardB)
        
        if (flushStraightA!=False or flushStraightB!=False):
            valA = valB = -1
            if flushStraightA!=False:
                valA = self.checkHighCard(flushStraightA)
            if flushStraightB!=False:
                valB = self.checkHighCard(flushStraightB)
            print "Player %d won with straight flush %d high" % (int(valA<valB), max(valA, valB))
            return valA<valB
        elif (fourKindA!=False or fourKindB!=False):
            print "Player %d won with 4 of a kind of %d" % (int(fourKindA<fourKindB), max(fourKindA, fourKindB))
            return fourKindA<fourKindB
        elif (fullHouseA!=False or fullHouseB!=False):
            valA = valB = -1
            if fullHouseA!=False:
                valA = fullHouseA[0]*100 + fullHouseA[1] #ensures we make the triple worth more
            if fullHouseB!=False:
                valB = fullHouseB[0]*100 + fullHouseB[1]
            print "Player %d won with full house" % (int(valA<valB), )
            return valA<valB
        elif (flushA!= False or flushB!=False):
            valA = valB = -1
            if (flushA!=False):
                valA = self.checkHighCard(flushA)
            if (flushB!=False):
                valB = self.checkHighCard(flushB)
            print "Player %d won with flush %d high" % (int(valA<valB), max(valA, valB))
            return valA<valB
        elif (straightA!=False or straightB!=False):
            valA = valB = -1
            if (straightA!=False):
                valA = self.checkHighCard(straightA)
            if (straightB!=False):
                valB = self.checkHighCard(straightB)
            print "Player %d won with straight %d high" % (int(valA<valB), max(valA, valB))
            return valA<valB
        elif (threeA!=False or threeB!=False):
            print "Player %d won with 3 of a kind of %d" % (int(threeA<threeB), max(threeA, threeB))
            return threeA<threeB
        elif (pairA!=[] or pairB!=[]): #TODO check kicker
            if len(pairA) == len(pairB):
                valA = max(pairA[0:2])*100 + min(pairA[0:2])
                valB = max(pairB[0:2])*100 + min(pairB[0:2])
                if valA==valB:
                    print "Tie, check kicker"
                print "Player %d won with %d pair with total value %d" % (int(valA<valB), max(len(pairA), len(pairB)), max(valA,valB))
            else:
                print "Player %d won with %d pair" % (int(len(pairA)<len(pairB)), max(len(pairA), len(pairB)))
                return len(pairA)<len(pairB)
        else:
            print "Player %d won with high card %d" % (int(highA<highB), max(highA, highB))
    #returns an array of cards in the straight flush in descending order
    def checkFlushStraight(self, cards):
        flush = self.checkFlush(cards)
        if flush:
            return self.checkStraight(flush)
        else:
            return False
    #returns an array of cards that composes the flush (could be more than 5) in descending order (except ace last b/c value is 1) or False otherwise
    def checkFlush(self, cards):
        handSorted = sorted(cards, key=lambda card: card.num)
        totals = [0,0,0,0]
        for card in cards:
            totals[card.suit]+=1
        maxnum = max(totals)
        if maxnum>=5:
            return filter(lambda card: card.suit==totals.index(maxnum, ), handSorted)[-1::-1] #this should be stable
        else:
            return False
    #cards = [Card(0,0), Card(1,0), Card(2,0), Card(3,0), Card(4,0), Card(5,0), Card(6,0)]
    #returns the array of cards in the straight in descending order (ace first though, different from checkFlush) or False if none
    def checkStraight(self, cards):
        handSorted = sorted(cards, key=lambda card: card.num, reverse=True)
        numStreak = 1
        straight = []
        if handSorted[0].num==0:
            print "DEBUG: ERROR, card with value 0"
        #handle ace case
        if handSorted[-1].num==1 and handSorted[0].num==13:
            numStreak+=1
            straight.append(handSorted[-1])
        
        straight.append(handSorted[0])
        for i in range(1, len(cards)):
            if handSorted[i].num==handSorted[i-1].num-1:
                numStreak+=1
                straight.append(handSorted[i])
            elif handSorted[i].num==handSorted[i-1].num:
                pass
            else:
                numStreak=1
                straight = []
            if numStreak==5:
                return straight
        return False    
    #returns the VALUE of 4 of a kind or False if none
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
            return False
    #returns the value of the 3 of a kind or False otherwise
    def checkThreeOfKind(self, cards):
        handSorted = sorted(cards, key=lambda card: card.num, reverse=True)
        currentLength = 1
        for i in range (1,len(cards)):
            if handSorted[i].num==handSorted[i-1].num:
                currentLength+=1
                if currentLength==3:
                    return handSorted[i].num
            else:
                currentLength=1
        return False
    #returns all VALUES of pairs in an array (ascending order) or [] if none
    def checkPair(self, cards):
        if len(cards)<=1:
            return []
        pairs = []
        handSorted = sorted(cards, key=lambda card: card.num, reverse=True)
        for i in range (0,len(cards)-1):
            if handSorted[i].num==handSorted[i+1].num:
                pairs.append(handSorted[i].num)
        return list(set(pairs))
    #returns the VALUE in a tuple of the 3ofakind, 2ofakind; False otherwise
    def checkFullHouse(self, cards):
        num = self.checkThreeOfKind(cards)
        if num==False:
            return False
        cards = filter(lambda card: card.num!=num, cards)
        pairs = self.checkPair(cards)
        if len(pairs)!=0:
            return (num, pairs[-1])
        else:
            return False
    #returns the VALUE of the high card
    def checkHighCard(self, cards):
        handSorted = sorted(cards, key=lambda card: card.num, reverse=True)
        if handSorted[-1].num == 1:
            return 14
        else:
            return handSorted[0].num
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

def replace_to_num(h):
    royals = 'TJQKA'
    result = []
    for card in h:
        if card[0] in royals:
            num = 10 + royals.index(card[0])
        else:
            num = int(card[0])
        result.append(num)
    return result

def is_flush(h):
    if h[0][1] == h[1][1] == h[2][1] == h[3][1] == h[4][1]:
        return True
    return False
    
def is_straight(h):
    values = sorted(replace_to_num(h))
    for i in range(min(values)+1, min(values)+5):
        if i not in values:
            return False
    return True
    
def Royal_Flush(h1, h2):
    if is_flush(h1):
        if set([h1[x][0] for x in range(5)]) == {'A', 'K', 'Q', 'J', 'T'}:
            return 1        
    if is_flush(h2):
        if set([h2[x][0] for x in range(5)]) == {'A', 'K', 'Q', 'J', 'T'}:
            return 2
    return
        
def Straight_Flush(h1, h2):
    check = [0,0]
    if is_flush(h1) and is_straight(h1):
        check[0] = 1        
    if is_flush(h2) and is_straight(h2):
        check[1] = 1
    if check == [1,1]:
        if max(replace_to_num(h1)) > max(replace_to_num(h2)):
            return 1
        else:
            return 2
    if check == [1,0]:
        return 1
    if check == [0,1]:
        return 2
    return
    
def Four_of_a_Kind(h1, h2):
    check = [0,0]
    num1 = sorted(replace_to_num(h1))
    num2 = sorted(replace_to_num(h2))
    if num1.count(num1[0]) == 4:
        check[0] = 1
        four1 = num1[0]
        one1 = num1[4]
    if num1.count(num1[4]) == 4:
        check[0] = 1
        four1 = num1[4]
        one1 = num1[0]
    if num2.count(num2[0]) == 4:
        check[1] = 1
        four2 = num2[0]
        one2 = num2[4]
    if num2.count(num2[1]) == 4:
        check[1] = 1
        four2 = num2[4]
        one2 = num2[0]
    if check == [1,1]:
        if four1 > four2:
            return 1
        elif four1 < four2:
            return 2
        elif one1 > one2:
            return 1
        else:
            return 2
    if check == [1,0]:
        return 1
    if check == [0,1]:
        return 2
    return

def Full_House(h1, h2):
    check = [0,0]
    num1 = sorted(replace_to_num(h1))
    num2 = sorted(replace_to_num(h2))
    if num1.count(num1[0]) == 3 and num1.count(num1[4]) == 2:
        check[0] = 1
        triple1 = num1[0]
        pair1 = num1[4]
    if num1.count(num1[0]) == 2 and num1.count(num1[4]) == 3:
        check[0] = 1
        triple1 = num1[4]
        pair1 = num1[0]
    if num2.count(num2[0]) == 3 and num2.count(num2[4]) == 2:
        check[1] = 1
        triple2 = num2[0]
        pair2 = num2[4]
    if num2.count(num2[0]) == 2 and num2.count(num2[4]) == 3:
        check[1] = 1
        triple2 = num2[4]
        pair2 = num2[0]
    if check == [1,1]:
        if triple1 > triple2:
            return 1
        elif triple1 < triple2:
            return 2
        elif pair1 > pair2:
            return 1
        else:
            return 2
    if check == [1,0]:
        return 1
    if check == [0,1]:
        return 2
    return

def Flush(h1, h2):
    check = [0,0]
    if is_flush(h1):
        check[0] = 1
    if is_flush(h2):
        check[1] = 1
    if check == [1,1]:
        return High_Card(replace_to_num(h1), replace_to_num(h2))
    if check == [1,0]:
        return 1
    if check == [0,1]:
        return 2
    return

def Straight(h1, h2):
    check = [0,0]
    if is_straight(h1):
        check[0] = 1
    if is_straight(h2):
        check[1] = 1
    if check == [1,1]:
        if max(replace_to_num(h1)) > max(replace_to_num(h2)):
            return 1
        else:
            return 2
    if check == [1,0]:
        return 1
    if check == [0,1]:
        return 2
    return

def Three_of_a_Kind(h1, h2):
    check = [0,0]
    num1 = sorted(replace_to_num(h1))
    num2 = sorted(replace_to_num(h2))
    for i in num1:
        if num1.count(i) == 3:
            check[0] = 1
            triple1 = i
            break
    for i in num2:
        if num2.count(i) == 3:
            check[1] = 1
            triple2 = i
            break
    if check == [1,1]:
        if triple1 > triple2:
            return 1
        elif triple1 < triple2:
            return 2
        else:
            return High_Card([x for x in num1 if x != triple1], [x for x in num2 if x != triple2])
    if check == [1,0]:
        return 1
    if check == [0,1]:
        return 2
    return

def Two_Pairs(h1, h2):
    check = [0,0]
    num1 = replace_to_num(h1)
    num2 = replace_to_num(h2)
    pairs1 = []
    for i in num1:
        if num1.count(i) == 2:
            if i not in pairs1:
                pairs1.append(i)
    if len(pairs1) == 2:
        check[0] = 1
    pairs2 = []
    for i in num2:
        if num2.count(i) == 2:
            if i not in pairs2:
                pairs2.append(i)
    if len(pairs2) == 2:
        check[1] = 1
    if check == [1,1]:
        tiebreak = High_Card(pairs1, pairs2)
        if tiebreak != None:
            return tiebreak
        else:
            one1 = list(set(num1)-set(pairs1))
            one2 = list(set(num2)-set(pairs2))
            if one1[0] > one2[0]:
                return 1
            else:
                return 2
    if check == [1,0]:
        return 1
    if check == [0,1]:
        return 2
    return
    
def One_Pair(h1, h2):
    check = [0,0]
    num1 = sorted(replace_to_num(h1))
    num2 = sorted(replace_to_num(h2))
    for i in num1:
        if num1.count(i) == 2:
            check[0] = 1
            pair1 = i
            break
    for i in num2:
        if num2.count(i) == 2:
            check[1] = 1
            pair2 = i
            break
    if check == [1,1]:
        if pair1 > pair2:
            return 1
        elif pair1 < pair2:
            return 2
        else:
            return High_Card([x for x in num1 if x != pair1], [x for x in num2 if x != pair2])
    if check == [1,0]:
        return 1
    if check == [0,1]:
        return 2
    return

def High_Card(num1, num2):
    num1 = sorted(num1)
    num2 = sorted(num2)
    for i in range(len(num1)-1, -1, -1):
        if num1[i] > num2[i]:
            return 1
        if num1[i] < num2[i]:
            return 2
    return

def winner(h1, h2):
    w = Royal_Flush(h1, h2)
    if w != None:
        return w
    w = Straight_Flush(h1, h2)
    if w != None:
        return w
    w = Four_of_a_Kind(h1, h2)
    if w != None:
        return w
    w = Full_House(h1, h2)
    if w != None:
        return w
    w = Flush(h1, h2)
    if w != None:
        return w
    w = Straight(h1, h2)
    if w != None:
        return w
    w = Three_of_a_Kind(h1, h2)
    if w != None:
        return w
    w = Two_Pairs(h1, h2)
    if w != None:
        return w
    w = One_Pair(h1, h2)
    if w != None:
        return w
    return High_Card(replace_to_num(h1), replace_to_num(h2))
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