import numpy as np
import holdem
import UnbiasedNet
import framework as fw
import calling_station

class Raising_station(fw.Auto_player):
    def __init__(self):
        self.net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                                        randomInit=False)
        self.status= fw.Status()
        self.name="RaisingStation"
    def decision(self, player2, debug=0):
        #always call/check
        if debug:
            print "it's the rs's turn!"
        stage=self.status.stage
        if (player2.status.vec_act[stage][0]== 4*fw.basebet(stage)):
            if debug:
                print "Now rs call at stage ", stage
            next=self.status.call()
        else:
            next=self.status.praise()
            if debug:
                print "Now rs bet/raise at stage ", stage
        self.status= next.copy()
        #update the other guy's status vector resulting from your act
        player2.status.vec_act[stage][1]=self.status.vec_act[stage][0]
        player2.status.vec_act[stage][2]=self.status.vec_act[stage][2]
        player2.status.stage= self.status.stage

if __name__== "__main__":
    import pickle
#    auto= pickle.load(open("player.p", "rb"))
#    net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
#                               alpha=0.02, 
#                               lamb=0.9, randomInit=True)
#    auto= fw.Auto_player(net, name="superbot") 
    auto= calling_station.Calling_station()
    rs= Raising_station()
    auto.compete(1,rs, debug=1)
#    pickle.dump(auto, open("player.p", "wb"))
