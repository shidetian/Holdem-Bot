import numpy as np

#parameters
n_in =  52*4 + 1 + 3*4 # num of input nodes=221
n_hidden = 40 # number of hidden nodes
n_out = 1
GAMMA = 0.9 # discount rate
ALPHA = 1.0 / n_in # 1st layer learning rate
BETA = 1.0 / 100 # 2nd layer learning rate
LAMBDA = 0.5 # < GAMMA. The descent rate?


class status:
    #v_p for preflop, dealer=0 means not dealer, v_pa stands for preflop action
    def __init__(self, v_p=zeros(52), v_f=zeros(52), v_t=zeros(52),
                 v_r=zeros(52), dealer=0, v_pa=zeros(3), v_fa=zeros(3),
                 v_ta=zeros(3), v_ra=zeros(3)):
        self.v_p=v_p
        self.v_f=v_f
        self.v_t=v_t
        self.v_r=v_r
        self.dealer=dealer
        self.v_pa=v_pa
        self.v_fa=v_fa
        self.v_ta=v_ta
        self.v_ra=v_ra;

#v_weights is of dim  n_in * n_hidden, w_weights is of dim n_hidden*n_out
def eval(current_status, v_weights, w_weights):
    #to be implemented, returns the expected gain of status under current strategy
    #status is a vector of dim n_in
    return 0

class Auto_player:
   def __init__(self, v, w):
       self.v= v
       self.w= w;
   def decision(self, current_status):
       next_status=current_status
       #to be implemented
       return next_status
   def sim_one_hand(self, player2, dealer=0):
       stat_seq=[]
       output=0
       #to be implemented
       return [stat_seq, output]
   def learn_one(self, stat_seq, output):
       #update all the weights
       return
   def train(self,num_of_train, opponent):
       for i in range(num_of_train):
           result=self.sim_one_hand(opponent, dealer=i%2)
           self.learn_one(result[0], result[1])
       return 
