import HandStat as fw
import anotherStatus
import numpy as np
import holdem
import UnbiasedNet
from framework import *


class Big_small_blind(fw.MyAutoPlayer):
    def __init__(self, small_blind_bot, big_blind_bot, 
                 stat=None, name= "anonymous", frenzy=False):
        self.sbb=small_blind_bot
        self.bbb=big_blind_bot
        self.frenzy=frenzy
        self.name=name
        if stat==None:
            self.status=anotherStatus.AnotherStatus()
        else:
            self.status=stat

#    def post_blinds(self, player2, dealer=0):
#        if dealer==0:
#            dealer_player= player2
#            nondealer_player= self.bbb
#        else:
#            dealer_player= self.sbb
#            nondealer_player= player2
#        nondealer_player.status.vec_act[0]=[2,1,0]
#        dealer_player.status.vec_act[0]=[1,2,0]
#        if dealer==0:
#            self.status=self.bbb.copy()
#        else:
#            self.status=self.sbb.copy()

#    def decision(self, player2, gameO, playerNum, debug=0):
#        if self.status.dealer==1:
#            self.sbb.status.dealer=1
#            result=self.sbb.decision(player2, gameO, playerNum, debug=0)
#            self.status=self.sbb.status.copy()
#            return result
#        else:
#            self.bbb.status.dealer=0
#            result=self.bbb.decision(player2, gameO, playerNum, debug=0)
#            self.status=self.bbb.status.copy()
#            return result

    def learn_one(self, stat_seq, output, dealer):
       #update all the weights
       #no matter which way we take to encode infomation,
       #this function should be virtually identical
        if dealer==1:
            self.sbb.net.learnTD( stat_seq, output)
        else:
            self.bbb.net.learnTD( stat_seq, output)
        return

    def train(self,num_of_train, opponent, debug=0, frenzy=0, 
              recover_rate=0):
       #recover_rate=1 means recovers from frenzy immediately
       #recover_rate=0 means it never recovers
        rate=1-recover_rate
        frenzy_degree=frenzy
        self.frenzy= frenzy
        self.sbb.frenzy=frenzy
        self.bbb.frenzy=frenzy
        game= holdem.Holdem(2, 4, 4, debug);
        for i in range(num_of_train):
            if np.random.rand() < frenzy_degree:
                self.frenzy=frenzy
                self.sbb.frenzy=frenzy
                self.bbb.frenzy=frenzy
            else:
                self.frenzy=0
                self.sbb.frenzy=frenzy
                self.bbb.frenzy=frenzy
            frenzy_degree *=rate
            if i%2==1:
                result=self.sbb.sim_one_hand(opponent, game, 1, debug=debug)
            else:
                result=self.bbb.sim_one_hand(opponent, game, 0, debug=debug)
            game.endRound()
           # print result[1]
            self.learn_one(result[0], result[1], self.status.dealer)
        self.frenzy= 0
        self.sbb.frenzy=0
        self.bbb.frenzy=0
        return
    
    def compete(self, opponent, num_of_games=100, debug=0):
        start_cash=0
        game=holdem.Holdem(2,4,4,debug)
        for i in range(num_of_games):
            if i%2==1:
                result=self.sbb.sim_one_hand(opponent, 
                                             game, dealer=1, debug=debug)
            else:
                result=self.bbb.sim_one_hand(opponent, 
                                             game, dealer=0, debug=debug)
            game.endRound()
            if debug:
                print "End of one hand. The winning is", result[1], "\n"
            start_cash += result[1]
        return start_cash

if __name__=="__main__":
    ALPHA=0.0005
    LAMB=0.6
    n_train=10
    net1=UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out, randomInit=True,
                               alpha=ALPHA, lamb=LAMB)
    auto1=fw.MyAutoPlayer(net1, name="auto1", frenzy=True)
    net2=UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out, randomInit=True,
                               alpha=ALPHA, lamb=LAMB)
    auto2=fw.MyAutoPlayer(net2, name="auto2", frenzy=True)
    big_small= Big_small_blind(auto1, auto2, frenzy=True)
    import calling_station
    csbot=calling_station.Calling_station()
    big_small.train(n_train, csbot, frenzy=True, debug=1)
    big_small.compete(csbot)
