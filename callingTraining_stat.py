import numpy as np
import holdem
import UnbiasedNet
import HandStat as fw

class Calling_station(fw.MyAutoPlayer):
    def __init__(self):
        self.net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                                        randomInit=False)
        self.status= fw.StatStatus()
        self.name="CallingStation"
    def decision(self, player2, debug=0):
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
if 1:
# auto= pickle.load(open("player.p", "rb"))
    net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                               alpha=0.02,
                               lamb=0.9, randomInit=True)
    auto= fw.MyAutoPlayer(net, name="superbot")
    cs= Calling_station()
    auto.train(50000, cs, debug=0)
    pickle.dump(auto, open("player2.p", "wb"))
if 1:
    cs= Calling_station()
    auto = pickle.load(open("player2.p", "rb"))
    result = []
    for i in range(40):
        result.append( auto.compete(cs, 5000, debug=0) )
    print result
