import numpy as np
import UnbiasedNet
import holdem
import framework

def basebet(stage):
    if stage <=1:
        return 2
    else:
        return 4

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

    def stat(self, hole_cards=None, features=None):
        cards = self.cards
        stats = {}
        suits = self.suit_list(cards)
        ranks = self.rank_list(cards)
        if 14 in ranks:
            ranks.append( 1 ) # ace can be 1 in a wheel straight
        ranks = sorted( ranks )
        reverse_rank = sorted( ranks, reverse=True )
        distances = [ ranks[i+1] - ranks[i] for i in range(len(ranks)-1) ]
        #------------Preflop's hand------------------------
        if len(cards) >= 2:
            for i in range(2, 17):
                # 11 to 13 means J to K
                # 14 means pair of A
                # 15 means pair of 2 to 7
                # 16 means pair of 8 to 10
                stats['pair ' + str(i)] = 0
            for i in range(len(ranks) - 1):
                if ranks[i] == ranks[i+1]:
                    stats['pair ' + str(ranks[i])] = 1
                    if i in range(2, 8):
                        stats['pair 15'] = 1
                    elif i in range(8, 11):
                        stats['pair 16'] = 1
            stats['pair'] = int( distances.count(0) > 0 )   
            stats['2-connected'] = distances.count(1) + distances.count(2)
            suitCount = [suits.count(i) for i in range(4)]
            stats['2-suited'] = int( max(suitCount) >= 2 )
            stats['1-high'] = int( ranks[-1] > 12 )
            stats['2-high'] = int( ranks[-2] > 8 )

        #------------Flop's board--------------------------
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
            #---------Comparing to my hole cards---------------
            if not hole_cards is None:
                hole_ranks = self.rank_list(hole_cards)
                all_ranks = hole_ranks + ranks
                all_ranks = sorted( all_ranks )
                for j in range(5):
                    # '0-highest' is true if we have the highest card
                    # '1-highest' is true if we have the second highest card, etc.
                    stats[str(j)+'-highest'] = all_ranks[-j] in hole_ranks
                stats['1-higher'] = not all_ranks[-1] in hole_ranks
                stats['2-higher'] = not all_ranks[-2] in hole_ranks
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
three_features = two_features + ['pairs', '3-high', '3-connected',
                            '3-suited', '3-of-a-kind']
four_features = three_features + ['4-suited', '4-connected']
five_features = four_features + ['5-suited', '5-connected']
final_features = ['pair', '1-high', '2-high', 'pairs', '3-of-a-kind',
                  '5-suited', '5-connected']
    
class StatStatus(framework.Status):
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
                        'my river': np.zeros(len(final_features))}
        self.dealer=dealer
        self.vec_act=np.zeros((4,3))
        self.stage=0;
        self.cards = None
    def longvec(self):
        #this just concatenate the vectors
        return np.concatenate([ self.vec_cards['my preflop'],
                    self.vec_cards['flop'], self.vec_cards['my flop'],
                    self.vec_cards['turn'], self.vec_cards['my turn'],
                    self.vec_cards['river'], self.vec_cards['my river'],
                               np.array([self.dealer]),
                               self.vec_act[0], self.vec_act[1],
                               self.vec_act[2], self.vec_act[3],
                               np.array([self.stage])])
    def copy(self):
        new_one= StatStatus()
        new_one.vec_cards={key:self.vec_cards[key] for key in self.vec_cards}
        new_one.dealer=1*self.dealer
        new_one.vec_act=1*self.vec_act
        new_one.stage=1*self.stage
        new_one.cards = self.cards
        return new_one
    
    def update_preflop(self, cards):
        self.cards = list(cards) # needed later
        hand = HandStat( cards=cards )
        self.vec_cards['my preflop'] = hand.stat( features=two_features )
        
    def update_flop(self, table):
        #table is a list of Cards
        board = HandStat(table)
        self.vec_cards['flop'] = board.stat( features=three_features )
        my = HandStat( self.cards + table )
        self.vec_cards['my flop'] = my.stat( features=five_features )        
        self.stage=1
        
    def update_turn(self, table):
        board = HandStat(table)
        self.vec_cards['turn'] = board.stat( features=four_features )
        my = HandStat( self.cards + table )
        self.vec_cards['my turn'] = my.stat( features=five_features )
        self.stage=2
        
    def update_river(self, table):
        board = HandStat(table)
        self.vec_cards['river'] = board.stat( features=five_features )
        my = HandStat( self.cards + table )
        self.vec_cards['my river'] = my.stat( features=final_features )
        self.stage=3
   
class MyAutoPlayer(framework.Auto_player):
   def __init__(self, neural_net, name= "anonymous", frenzy=False):
       framework.Auto_player.__init__(self, neural_net, name= "anonymous",
                                      frenzy=frenzy, Check_prob=0.25,
                                      Call_prob=0.25, Raise_prob=0.25,
                                      CheckFold_prob=0.25)
       self.status=StatStatus()
   
   def sim_one_hand(self, player2, game, dealer=0, debug=0):
       stat_seq=[]
       output=0
       #clear up possible leftover status from last game
       self.status=StatStatus(dealer=dealer)
       player2.status=StatStatus(dealer=1-dealer)
       #initialize the game and deal the pocket cards.
       #game= holdem.Holdem(2, 4, 4, debug);
       game.setName(player2.name, self.name)
       #post the blind
       self.post_blinds(player2, dealer)
       #deal the hands
       self.status.update_preflop(game.players[0].cards)
       player2.status.update_preflop(game.players[1].cards)
       stat_seq.append(self.status.longvec())
       if debug:
           print "blinds:"
           print self.status.vec_act[0][0], self.status.vec_act[0][1]
       #pre-flop action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.longvec())
       if debug:
           print "preflop:", self.status.vec_act[0]
           print "preflop:", player2.status.vec_act[0]
       if (self.status.vec_act[0][0] < player2.status.vec_act[0][0]):
           return [stat_seq, -self.cum_bet()]
       elif (self.status.vec_act[0][0] > player2.status.vec_act[0][0]):
           return (stat_seq, player2.cum_bet())
       #deal the flop
       #game._endStage_();
       self.status.update_flop(game.table)
       player2.status.update_flop(game.table)
       stat_seq.append(self.status.longvec())
       #flop action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.longvec())
       if debug:
           print "on the flop:"
           print self.status.vec_act[1][0], self.status.vec_act[1][1]
       if (self.status.vec_act[1][0]< player2.status.vec_act[1][0]):
           return [stat_seq, -self.cum_bet()]
       elif (self.status.vec_act[1][0] > player2.status.vec_act[1][0]):
           return (stat_seq, player2.cum_bet())
       #deal the turn 
       #game._endStage_();
       self.status.update_turn(game.table)
       player2.status.update_turn(game.table)
       stat_seq.append(self.status.longvec())
       #turn action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.longvec())
       if debug:
           print "on the turn:" 
           print self.status.vec_act[2][0], self.status.vec_act[2][1]
       if (self.status.vec_act[2][0]< player2.status.vec_act[2][0]):
           return [stat_seq, -self.cum_bet()]
       elif (self.status.vec_act[2][0] > player2.status.vec_act[2][0]):
           return (stat_seq, player2.cum_bet())
       #deal the river
       #game._endStage_()
       self.status.update_river(game.table)
       player2.status.update_river(game.table)
       stat_seq.append(self.status.longvec())
       #river action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.longvec())
       if debug:
           print "on the river:"
           print self.status.vec_act[3][0], self.status.vec_act[3][1]
       if (self.status.vec_act[3][0]< player2.status.vec_act[3][0]):
           return [stat_seq, -self.cum_bet()]
       elif (self.status.vec_act[3][0] > player2.status.vec_act[3][0]):
           return (stat_seq, player2.cum_bet())
       #show down
       #game.stage=4
       res= game.checkWinner()
       #game.endRound()
       if (res[0]>res[1]):
           return (stat_seq, self.cum_bet())
       elif (res[0]< res[1]):
           return (stat_seq, -self.cum_bet())
       else:
           if debug:
               print "it's a tie"
           return (stat_seq, 0)

   def learn_one(self, stat_seq, output):
       #update all the weights
       #no matter which way we take to encode infomation,
       #this function should be virtually identical
       self.net.learnTD( stat_seq, output)
       return 
   def train(self,num_of_train, opponent, debug=0, frenzy=0):
       self.frenzy= frenzy
       game= holdem.Holdem(2, 4, 4, debug);
       for i in range(num_of_train):
           result=self.sim_one_hand(opponent, game, dealer=i%2, debug=debug)
           game.endRound()
           # print result[1]
           self.learn_one(result[0], result[1])
           self.status = StatStatus()
           opponent.status= StatStatus()
       self.frenzy= 0

stat_rep = StatStatus()
n_in = len(stat_rep.longvec())
n_hidden = 40
n_out = 1
