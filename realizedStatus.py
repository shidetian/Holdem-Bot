from HandStat import *
import numpy as np
import UnbiasedNet
import holdem

pair_features = ['pair ' + str(i) for i in range(2, 15)]
my_preflop_features = pair_features + ['1-high', '2-high',
                                       '2-connected', '2-suited']
my_postflop_features = pair_features + ['pairs', '5-connected',
                                        '5-suited']
my_river_features = my_postflop_features 
flop_features = ['1-higher', '2-higher', 'pair']
turn_features = flop_features + ['4-suited', '4-connected']
river_features = turn_features

class AnotherStatus(StatStatus):
    def __init__(self, dealer=0):
        self.vec_cards = {'my preflop': np.zeros(len(my_preflop_features)),
                        'flop': np.zeros(len(flop_features)),
                        'my flop': np.zeros(len(my_postflop_features)),
                        'turn': np.zeros(len(turn_features)),
                        'my turn': np.zeros(len(my_postflop_features)),
                        'river': np.zeros(len(river_features)),
                        'my river': np.zeros(len(my_river_features))}
        self.dealer=dealer
        self.vec_act=np.zeros((4,3))
        self.stage=0;
        self.cards = None
    
    def copy(self):
        new_one= AnotherStatus()
        new_one.vec_cards={key:self.vec_cards[key] for key in self.vec_cards}
        new_one.dealer=1*self.dealer
        new_one.vec_act=1*self.vec_act
        new_one.stage=1*self.stage
        new_one.cards = self.cards
        return new_one

    def update_preflop(self, cards):
        self.cards = list(cards) # needed later
        hand = HandStat( cards=cards )
        self.vec_cards['my preflop'] = hand.stat( features=my_preflop_features )

    def update_flop(self, table):
        #table is a list of Cards
        board = HandStat(table)
        self.vec_cards['flop'] = board.stat( features=flop_features,
                                             hole_cards=self.cards )
        my = HandStat( self.cards + table )
        self.vec_cards['my flop'] = my.stat( features=my_postflop_features )        
        self.stage=1

    def update_turn(self, table):
        board = HandStat(table)
        self.vec_cards['turn'] = board.stat( features=turn_features,
                                             hole_cards=self.cards )
        my = HandStat( self.cards + table )
        self.vec_cards['my turn'] = my.stat( features=my_postflop_features )
        self.stage=2

    def update_river(self, table):
        board = HandStat(table)
        self.vec_cards['river'] = board.stat( features=river_features,
                                              hole_cards=self.cards )
        my = HandStat( self.cards + table )
        self.vec_cards['my river'] = my.stat( features=my_river_features )
        self.stage=3

class AnotherAutoPlayer(MyAutoPlayer):
   def __init__(self, neural_net, name= "anonymous", frenzy=False):
       MyAutoPlayer.__init__(self, neural_net, name= "anonymous", frenzy=frenzy)
       self.status=AnotherStatus()
   def reset_status(self):
       self.status=AnotherStatus()
   def sim_one_hand(self, player2, game, dealer=0, debug=0):
       stat_seq=[]
       output=0
       #clear up possible leftover status from last game
       self.reset_status()
       player2.reset_status()
       self.status.dealer=dealer
       player2.status.dealer=1-dealer
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
   def train(self,num_of_train, opponent, debug=0, frenzy=0, 
             recover_rate=0):
       #recover_rate=1 means recovers from frenzy immediately
       #recover_rate=0 means it never recovers
       rate=1-recover_rate
       frenzy_degree=frenzy
       self.frenzy= frenzy
       game= holdem.Holdem(2, 4, 4, debug);
       for i in range(num_of_train):
           if np.random.rand() < frenzy_degree:
               self.frenzy=frenzy
           else:
               self.frenzy=0
           frenzy_degree *=rate
           result=self.sim_one_hand(opponent, game, dealer=i%2, debug=debug)
           game.endRound()
           # print result[1]
           self.learn_one(result[0], result[1])
           self.status = AnotherStatus()
           opponent.status= AnotherStatus()
       self.frenzy= 0

stat_rep = AnotherStatus()
n_in = len(stat_rep.longvec())
n_hidden = 50
n_out = 1
