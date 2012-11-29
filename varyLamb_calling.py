import numpy as np
import holdem
import UnbiasedNet
import anotherStatus as fw
from cheater_bot import Cheater_player
import calling_station
class Calling_station(fw.AnotherAutoPlayer):
    def __init__(self):
        self.net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                                        randomInit=False)
        self.status= fw.AnotherStatus()
        self.name="CallingStation"
    def decision(self, player2, gameO=None, playerNum=-1,debug=0):
        #always call/check
        if debug:
            print "it's the cs's turn!"
        stage=self.status.stage
        if (self.status.vec_act[stage][0]< self.status.vec_act[stage][1]):
            if debug:
                print "Now cs call at stage ", stage
            next=self.status.call()
            action= "Call"
        elif (stage>0 and self.status.vec_act[stage][0]==0
              and self.status.dealer==0):
            if debug:
                print "Now cs check_fist"
            next=self.status.check_first()
            action= "Check"
        else:
            if debug:
                print "Now cs check_fold", stage
            next=self.status.check_fold()
            action= "CheckFold"
        self.status= next.copy()
        #update the other guy's status vector resulting from your act
        player2.status.vec_act[stage][1]=self.status.vec_act[stage][0]
        player2.status.vec_act[stage][2]=self.status.vec_act[stage][2]
        player2.status.stage= self.status.stage
        return action

import pickle
#    auto= pickle.load(open("player.p", "rb"))
#    net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
#                               alpha=0.001, 
#                               lamb=0.5, randomInit=False)
auto= calling_station.Calling_station()
n_train = 50000
for LAMB in [0.7, 0.8, 0.9, 1.0]:
    #net=UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden,
    #                          fw.n_out, alpha=0.001, lamb=LAMB,
    #                          randomInit=True)
    
    #auto2= fw.AnotherAutoPlayer(net, name="against_TA")
    #for i in range(3):
    #    auto2.train(n_train, auto, debug=0, frenzy=1)
    #    pickle.dump( auto2, open(str(i) + str(LAMB) +
    #                             'another_vs_TA.p', 'wb') )
    print "LAMB "+ str(LAMB)
    auto2 = pickle.load(open(str(2) + str(LAMB) + 'another_vs_TA.p', 'rb') )
    win=[]
    for i in range(10):
        win.append(auto2.compete(auto,1000, debug=0))
    #print win
    print "Mean: "+str(np.mean(win))
    print "Var: "+str(np.std(win))
