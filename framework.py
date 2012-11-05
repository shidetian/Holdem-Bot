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

class status:
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
        return status(1*self.vec_cards,
                      1*self.dealer, 1*self.vec_act, 1*self.stage)
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
   def __init__(self, neural_net):
       self.net= neural_net
   def decision(self, current):
       #takes in a current status, and make decision on next move
       possible_next=[]
       stage=current.stage
       if (stage>0 and current.vec_act[0][0]==0 and current.dealer==0):
               possible_next=[check_first(current), praise(current)]
       elif (current.vec_act[stage][0]<= 2*basebet(stage)):
           possible_next=[check_fold(current), call(current), praise(current)]
       else:
           possible_next=[check_fold(current), call(current)]
       values=[0]*len(possible_next)
       for i in range(len(possible_next)):
           values[i]=NeuralNet.predict(self.net, possible_next[i])
       index=values.index(max(values))
       return possible_next[index]
   def sim_one_hand(self, player2, dealer=0):
       stat_seq=[]
       output=0
       #to be implemented
       return [stat_seq, output]

   def learn_one(self, stat_seq, output):
       #update all the weights
       #no matter which way we take to encode infomation,
       #this function should be virtually identical
       NeuralNet.learnTD(self.net, stat_seq, output)
       return 
   
   def train(self,num_of_train, opponent):
       for i in range(num_of_train):
           result=self.sim_one_hand(opponent, dealer=i%2)
           self.learn_one(result[0], result[1])
           return 
       
