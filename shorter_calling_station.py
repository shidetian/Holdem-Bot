import numpy as np
import holdem
import UnbiasedNet
import shorter_framework as fw

class Calling_station(fw.Auto_player):
    def __init__(self):
        self.net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                                        randomInit=False)
        self.status= fw.Status()
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

if __name__== "__main__":
    import pickle
#    auto= pickle.load(open("player.p", "rb"))
    net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                               alpha=0.02, 
                               lamb=0.9, randomInit=True)
    auto= fw.Auto_player(net, name="superbot") 
    cs= Calling_station()
    auto.train(20,cs, debug=0)
    pickle.dump(auto, open("player.p", "wb"))
