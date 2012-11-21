import numpy as np
import holdem
import UnbiasedNet
import framework as fw
import calling_station

class Call_defeater(fw.Auto_player):
    def __init__(self):
        self.net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                                        randomInit=False)
        self.status= fw.Status()
        self.name="CallDefeater"
    def decision(self, player2, debug=0):
        #always call/check
        if debug:
            print "it's the defeater's turn!"
        stage= self.status.stage
        if (self.status.vec_cards[0][0]==1
            or self.status.vec_cards[0][13]==1 
            or self.status.vec_cards[0][26]==1
            or self.status.vec_cards[0][39]==1):
            if (self.status.vec_act[stage][0]<= self.status.vec_act[stage][1]
                if debug:
                    print "Now defeater bet/raise at stage", stage
                next=self.status.praise()
        elif (stage>0 and self.status.vec_act[stage][0]==0 
              and self.status.dealer==0):
            if debug:
                print "Now cs check_fist"
            next=self.status.check_first()
        else:
            if debug:
                print "Now cs check_fold", stage
            next=self.status.check_fold()
        self.status= next.copy()
        #update the other guy's status vector resulting from your act
        player2.status.vec_act[stage][1]=self.status.vec_act[stage][0]
        player2.status.vec_act[stage][2]=self.status.vec_act[stage][2]
        player2.status.stage= self.status.stage

if __name__== "__main__":
    import pickle
#    auto= pickle.load(open("player.p", "rb"))
    net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                               alpha=0.02, 
                               lamb=0.9, randomInit=False)
    auto= fw.Auto_player(net, name="superbot") 
    cs= Calling_station()
    auto.train(500000,cs, debug=0)
    pickle.dump(auto, open("player.p", "wb"))
    
    
