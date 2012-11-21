
import numpy as np
import UnbiasedNet
import Holdem

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
