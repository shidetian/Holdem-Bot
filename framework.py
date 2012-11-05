import numpy as np
import holdem
import NeuralNet

#parameters
n_in =  52*4 + 1 + 3*4 +1# num of input nodes=222
n_hidden = 40 # number of hidden nodes
n_out = 1
GAMMA = 0.9 # discount rate
ALPHA = 1.0 / n_in # 1st layer learning rate
BETA = 1.0 / 100 # 2nd layer learning rate
LAMBDA = 0.5 # < GAMMA. The descent rate?

def basebet(stage):
    if stage <=1:
        return 2
    else:
        return 4

class Status:
    #vec_cards for card vector,is of dim 4*52.
    #dealer=0 means not dealer, 
    #vec_act stands for action, is of dim 4*3, row corresponds to stage
    #column i is the bet of player i, 1<=i <=2; column 3 indicates whether 
    #this stage is over
    def __init__(self, vec_cards=np.zeros((4,52)), 
                 dealer=0, vec_act=np.zeros((4,3)), stage=0):
        self.vec_cards= vec_cards
        self.dealer=dealer
        self.vec_act=vec_act
        self.stage=stage;
    def longvec(self):
        #this just concatenate the vectors
        return np.concatenate([self.vec_cards,  self.dealer,
                               self.vec_act, self.stage])
    def copy(self):
        return Status(1*self.vec_cards,
                      1*self.dealer, 1*self.vec_act, 1*self.stage)
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

'''
#v_weights is of dim  n_in * n_hidden, w_weights is of dim n_hidden*n_out
def eval(current_status, v_weights, w_weights):
#evaluate the status
    h=np.zeros(n_hidden)
    for j in range(n_hidden):
        h[j]= np.sum(status.longvec() * w_weights[j])
    for j in range(n_hidden):
        h[j]=np.sign(h[j])
    return np.sum(h* v_weights)
'''

class Auto_player:
   def __init__(self, neural_net, stat= Status()):
       self.net= neural_net
       self.status= stat
   def cum_bet(self):
       #compute the total bet 
       sum=0
       for i in range(4):
           sum = sum+ self.status.vec_act[i][0]
       return sum
   def decision(self, player2):
       #make decision on next move
       possible_next=[]
       current= self.status
       stage=current.stage
       if (stage>0 and current.vec_act[0][0]==0 and current.dealer==0):
               possible_next=[check_first(current), praise(current)]
       elif (current.vec_act[stage][0]<= 2*basebet(stage)):
           possible_next=[check_fold(current), call(current), praise(current)]
       else:
           possible_next=[check_fold(current), call(current)]
       values=[0]*len(possible_next)
       for i in range(len(possible_next)):
           values[i] = self.net.predict(possible_next[i])
       index=values.index(max(values))
       current = possible_next[index]
       player2.status.vec_act[stage][1]=current.vec_act[stage][0]
       player2.status.vec_act[stage][2]=current.vec_act[stage][2]
   def post_blinds(self, player2, dealer=0):
       if dealer==0:
           dealer_player= player2
           nondealer_player= self
       else :
           dealer_player= self
           nondealer_player= player2
       dealer_player.status.vec_act[0]=[2,4,0]
       nondealer_player.status.vec_act[0]=[4,2,0]
   def action(self, player2, dealer=0):
       stage= self.status.stage
       if (dealer==0 and stage==0) or (dealer==1 and stage>0) :
           first= player2
           second= self
       else:
           first= self
           second= player2
       while (1):
           first.decision(second)
           if (first.status.vec_act[stage][2]==1):
               break
           second.decision(first)
           if (second.status.vec_act[stage][2]==1):
               break
   
   def sim_one_hand(self, player2, dealer=0):
       stat_seq=[]
       output=0
       #clear up possible leftover status from last game
       self.status=Status(dealer=dealer)
       player2.status=Status(dealer=1-dealer)
       stat1=self.status
       stat2=self.status
       game= holdem.Holdem(2, 4, 0)
       #post the blind
       self.postblinds(player2, dealer)
       #deal the hands
       game.deal()
       stat1.update_preflop(game.players[0].cards)
       stat2.update_preflop(game.players[1].cards)
       stat_seq.append(stat1)
       #pre-flop action
       self.action(player2, dealer)
       stat_seq.append(stat1)
       if (stat1.vec_act[0][0] < stat2.vec_act[0][0]):
           return [stat_seq, -self.cum_sum()]
       elif (stat1.vec_act[0][0] > stat2.vec_act[0][0]):
           return (stat_seq, player2.cum_sum())
       #deal the flop
       game.deal()
       stat1.update_flop(game.table)
       stat2.update_flop(game.table)
       stat_seq.append(stat1)
       #flop action
       self.action(player2, dealer)
       stat_seq.append(stat1)
       if (stat1.vec_act[1][0]< stat2.vec_act[1][0]):
           return [stat_seq, -self.cum_sum()]
       elif (stat1.vec_act[0][0] > stat2.vec_act[0][0]):
           return (stat_seq, player2.cum_sum())
       #deal the turn 
       game.deal()
       stat1.update_turn(game.table)
       stat2.update_turn(game.table)
       stat_seq.append(stat1)
       #turn action
       self.action(player2, dealer)
       stat_seq.append(stat1)
       if (stat1.vec_act[1][0]< stat2.vec_act[1][0]):
           return [stat_seq, -self.cum_sum()]
       elif (stat1.vec_act[0][0] > stat2.vec_act[0][0]):
           return (stat_seq, player2.cum_sum())
       #deal the river
       game.deal()
       stat1.update_river(game.table)
       stat2.update_river(game.table)
       stat.seq.append(stat1)
       #river action
       self.action(player2, dealer)
       stat_seq.append(stat1)
       if (stat1.vec_act[1][0]< stat2.vec_act[1][0]):
           return [stat_seq, -self.cum_sum()]
       elif (stat1.vec_act[0][0] > stat2.vec_act[0][0]):
           return (stat_seq, player2.cum_sum())
       #now show down, implement some time later
       return (stat_seq, 0)
   def learn_one(self, stat_seq, output):
       #update all the weights
       #no matter which way we take to encode infomation,
       #this function should be virtually identical
       self.net.learnTD( stat_seq, output)
       return 
   
   def train(self,num_of_train, opponent):
       for i in range(num_of_train):
           result=self.sim_one_hand(opponent, dealer=i%2)
           self.learn_one(result[0], result[1])
           return 
       
