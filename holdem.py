from random import shuffle
from copy import deepcopy
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
            print "Player zereo's hand: "
            print self.players[0].cards
            print "Player one's hand: "
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
        
def evalHand(hand):
    values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

    flush = 1
    suit = hand[0][1]
    for card in hand:
        if card[1] &lt;&gt; suit:
            flush = 0
            break

    indices = []
    royal = 1
    straight = 1
    for card in hand:
        indices.append(values.index(card[0]))
    indices.sort()
    if indices[4] - indices[0] &lt;&gt; 4 \
       or indices.count(indices[0]) &gt; 1 \
       or indices.count(indices[1]) &gt; 1 \
       or indices.count(indices[2]) &gt; 1 \
       or indices.count(indices[3]) &gt; 1 \
       or indices.count(indices[4]) &gt; 1:
        straight = 0
    if indices[0] &lt;&gt; 8:
        royal = 0

    kinds = []
    for value in indices:
        count = indices.count(value)
        if count &gt; 1:
            kind = [value, count]
            if kind not in kinds:
                kinds.append(kind)

    if royal and flush:
#        return "royal flush"
        return [9, 0]
    if straight and flush:
#        return "straight flush"
        return [8, indices[4]]
    if len(kinds) == 1 and kinds[0][1] == 4:
#        return "four of a kind"
        return [7, kinds[0][0]]
    if len(kinds) == 2 and (kinds[0][1] + kinds[1][1] == 5):
#        return "full house"
        return [6, kinds[0][0]]
    if flush:
#        return "flush"
        return [5, indices[4]]
    if straight:
#        return "straight"
        return [4, indices[4]]
    if len(kinds) == 1 and kinds[0][1] == 3:
#        return "three of a kind"
        return [3, kinds[0][0]]
    if len(kinds) == 2 and (kinds[0][1] + kinds[1][1] == 4):
#        return "two pair"
        return [2, max(kinds[0][0], kinds[1][0])]
    if len(kinds) == 1 and kinds[0][1] == 2:
#        return "one pair"
        return [1, kinds[0][0]]
#    return "high card"
    return [0, max(indices)]

rounds = []
f = file('poker.txt','r')
for l in f.readlines():
    rounds.append(l[:-1].split(' '))

count = 0
for r in rounds:
    p1 = evalHand(r[0:5])
    p2 = evalHand(r[5:10])
    if p1[0] &gt; p2[0] or (p1[0] == p2[0] and p1[1] &gt; p2[1]):
        count = count + 1

print count