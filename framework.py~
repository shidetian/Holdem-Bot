import numpy as np
import holdem
#import NeuralNet
import UnbiasedNet

#parameters
n_in =  52*4 + 1 + 3*4 +1# num of input nodes=222
n_hidden = 40 # number of hidden nodes
n_out = 1

def basebet(stage):
    if stage <=1:
        return 2
    else:
        return 4

class Status:
    #vec_cards for card vector,is of dim 4*52.
    #dealer=0 means not dealer, 
    #vec_act stands for action, is of dim 4*3, row corresponds to stage            #column i is the bet of player i, 1<=i <=2; column 3 indicates whether 
    #this stage is over
    def __init__(self, dealer=0):
        self.vec_cards= np.zeros((4,52))
        self.dealer=dealer
        self.vec_act=np.zeros((4,3))
        self.stage=0;
    def longvec(self):
        #this just concatenate the vectors
        return np.concatenate([self.vec_cards[0], self.vec_cards[1],
                               self.vec_cards[2], self.vec_cards[3],
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
        for i in range(2):
            self.vec_cards[0][cards[i].card_to_number()]=1
    def update_flop(self, table):
        #table is a list of Cards
        for i in range(3):
            self.vec_cards[1][table[i].card_to_number()]=1
        self.stage=1
    def update_turn(self, table):
        self.vec_cards[2][table[3].card_to_number()]=1
        self.stage=2
    def update_river(self, table):
        self.vec_cards[3][table[4].card_to_number()]=1
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

class Auto_player:
   def __init__(self, neural_net, stat= None, name= "anonymous", 
                frenzy= False):
       self.name= name
       self.net= neural_net
       if stat==None:
           self.status=Status()
       else:
           self.status=stat
       self.frenzy= frenzy
   def reset_status(self):
       self.status=Status()
   def cum_bet(self):
       #compute the total bet 
       sum=0
       for i in range(4):
           sum = sum+ self.status.vec_act[i][0]
       return sum
   def allowed_actions(self, player2, debug=0):
       current= self.status
       stage=current.stage
       if (stage>0 and current.vec_act[stage][0]==0 and 
           current.dealer==0 and player2.status.vec_act[stage][0]==0):
           #this is the case when you are the first to act in a post-flop round
           game_actions = ["Check", "Raise"]
       elif (current.vec_act[stage][1]< 4*basebet(stage)):
           #this is the case when you are not in first case, and you may still
           #raise
           game_actions = ["CheckFold", "Call", "Raise"]
       else:
           #all other cases
           game_actions = ["CheckFold", "Call"]
       return game_actions
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
               values[i] = self.net.predict(possible_next[i].longvec())[0]
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
   def post_blinds(self, player2, dealer=0):
       if dealer==0:
           dealer_player= player2
           nondealer_player= self
       else:
           dealer_player= self
           nondealer_player= player2
       nondealer_player.status.vec_act[0]=[2,1,0]
       dealer_player.status.vec_act[0]=[1,2,0]
   def action(self, player2, dealer=0, debug=0, game = None):
       stage= self.status.stage
       if (dealer==0 and stage==0) or (dealer==1 and stage>0) :
           first= player2
           second= self
       else:
           first= self
           second= player2
       while (1):
           game.performAction(first.decision(second, debug), 
                              (dealer==0 and stage==0) 
                              or (dealer==1 and stage>0))
           if debug:
               print "stage moved to ", first.status.stage, second.status.stage
               print first.status.vec_act[stage]
               print second.status.vec_act[stage]
           if (first.status.vec_act[stage][2]==1):
               break
           game.performAction(second.decision(first, debug), 
                              not ((dealer==0 and stage==0) 
                                   or (dealer==1 and stage>0)))
           if debug:
               print "stage moved to", first.status.stage,second.status.stage
               print first.status.vec_act[stage]
               print second.status.vec_act[stage]
           if (second.status.vec_act[stage][2]==1):
               break
   
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
   def train(self,num_of_train, opponent, debug=0, frenzy=0):
       game=holdem.Holdem(2, 4, 4, debug)
       self.frenzy= frenzy
       for i in range(num_of_train):
           result=self.sim_one_hand(opponent, game, dealer=i%2, debug=debug)
           game.endRound()
           print result[1]
           self.learn_one(result[0], result[1])
#           self.status= Status()
#           opponent.status= Status()
           print "End\n\n"
       self.frenzy= 0
   def compete(self, opponent, num_of_games=100, debug=1):
       start_cash=0
       game=holdem.Holdem(2, 4, 4, debug)
       for i in range(num_of_games):
           result=self.sim_one_hand(opponent, game, dealer=i%2, debug=debug)
           game.endRound()
           if debug:
               print "End of one hand. The winning is", result[1], "\n"
           start_cash= start_cash+ result[1]
       return start_cash

if __name__ == "__main__":
    net= UnbiasedNet.NeuralNet(n_in, n_hidden, n_out, alpha=0.1,
                               lamb=0.9, randomInit=True)
    auto= Auto_player(net, name="auto", frenzy=True)
    net2= UnbiasedNet.NeuralNet(n_in, n_hidden, n_out, randomInit=True)
    auto2= Auto_player(net2, name="auto2", frenzy=True)
    import pickle
    #from human_player import Human_player
    #auto = pickle.load(open("player.p", "rb"))
    auto.train(2, auto2, debug=1, frenzy=True)
#    pickle.dump(auto, open("player.p","wb"))
#    xyz=auto.sim_one_hand(auto2)
#    print xyz
