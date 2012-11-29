import numpy as np
import holdem
#import NeuralNet
import UnbiasedNet
import framework
from framework import *


#parameters
n_in=208
n_hidden = 150 # number of hidden nodes
n_out = 1

class shorter_Auto_player(framework.Auto_player):
   def __init__(self, neural_net, stat= None, name= "anonymous", 
                frenzy= False):
       self.name= name
       self.net= neural_net
       if stat==None:
           self.status=Status()
       else:
           self.status=stat
       self.frenzy= frenzy

   def decision(self, player2, debug=0):
       #make decision on next move
       if debug:
           print "it's "+self.name+" 's turn!"
       possible_next=[]
       current= self.status
       stage=current.stage
       if (stage>0 and current.vec_act[stage][0]==0 and 
           current.dealer==0 and player2.status.vec_act[stage][0]==0):
           #this is the case when you are the first to act in a post-flop round
           possible_next=[current.check_first(), current.praise()]
           game_actions = ["Check", "Raise"]
       elif (current.vec_act[stage][1]< 4*basebet(stage)):
           #this is the case when you are not in first case, and you may still
           #raise
           possible_next=[current.check_fold(), 
                          current.call(), current.praise()]
           game_actions = ["CheckFold", "Call", "Raise"]
       else:
           #all other cases
           possible_next=[current.check_fold(), current.call()]
           game_actions = ["CheckFold", "Call"]
       values=[0]*len(possible_next)
       if self.frenzy==False:
           for i in range(len(possible_next)):
               values[i] = self.net.predict(possible_next[i].shorter_longvec())[0]
               index=values.index(max(values))
       else:
           index= np.random.randint(0, len(possible_next))
       self.status = possible_next[index].copy()
       #update the other guy's status vector resulting from your act
       player2.status.vec_act[stage][1]=self.status.vec_act[stage][0]
       player2.status.vec_act[stage][2]=self.status.vec_act[stage][2]
       player2.status.stage= self.status.stage
       if debug:
           #print "after the decision is made at stage:", stage
           #print self.status.vec_act[stage]
           #print player2.status.vec_act[stage]
           print self.name+" decided to ", game_actions[index]
       return game_actions[index]
   
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
       stat_seq.append(self.status.shorter_longvec())
       if debug:
           print "blinds:"
           print self.status.vec_act[0][0], self.status.vec_act[0][1]
       #pre-flop action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.shorter_longvec())
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
       stat_seq.append(self.status.shorter_longvec())
       #flop action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.shorter_longvec())
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
       stat_seq.append(self.status.shorter_longvec())
       #turn action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.shorter_longvec())
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
       stat_seq.append(self.status.shorter_longvec())
       #river action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.shorter_longvec())
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
