import numpy as np
import holdem
import UnbiasedNet
import framework as fw
import calling_station
import pickle
import time

class Tight_aggressive(fw.Auto_player):
    def __init__(self):
        self.net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                                        randomInit=False)
        self.status= fw.Status()
        self.name="TightAggressive"
    def has_ace(self):
        if (self.status.vec_cards[0][0]==1
            or self.status.vec_cards[0][13]==1
            or self.status.vec_cards[0][26]==1
            or self.status.vec_cards[0][39]==1):
            return True
        else: 
            return False
    def has_king(self):
        if (self.status.vec_cards[0][12]==1
            or self.status.vec_cards[0][25]==1
            or self.status.vec_cards[0][38]==1
            or self.status.vec_cards[0][51]==1):
            return True
        else:
            return False
    def has_pair(self):
        i=0
        while (i<52):
            if self.status.vec_cards[0][i]==1:
                break
            else:
                i+=1
        j=i
        while (j+13<52):
            j+=13
            if (self.status.vec_cards[0][j]==1):
                return True
        return False
    def decision(self, player2, debug=0):
        #always call/check
        if debug:
            print "it's the defeater's turn!"
        stage= self.status.stage
        if self.has_ace() or self.has_king() or self.has_pair():
            if "Raise" in self.allowed_actions(player2):
                if debug:
                    print "Now defeater bet/raise at stage", stage
                next=self.status.praise()
                action= "Raise"
            elif "Call" in self.allowed_actions(player2):
                next=self.status.call()
                action= "Call"
        else:
            if debug:
                print "Now cs check_fold", stage
            if "CheckFold" in self.allowed_actions(player2):
                next=self.status.check_fold()
                action= "CheckFold"
            else: 
                next=self.status.check_first()
                action= "Check"
        self.status= next.copy()
        #update the other guy's status vector resulting from your act
        player2.status.vec_act[stage][1]=self.status.vec_act[stage][0]
        player2.status.vec_act[stage][2]=self.status.vec_act[stage][2]
        player2.status.stage= self.status.stage
        return action

if __name__== "__main__":
    import pickle
#    auto= pickle.load(open("player.p", "rb"))
#    net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
#                               alpha=0.001, 
#                               lamb=0.5, randomInit=False)
    auto= Tight_aggressive()
    cs= calling_station.Calling_station()
    win=[]
    for i in range(50):
        win.append(auto.compete(cs,2000, debug=1))
    print win
    print np.mean(win)
    print np.std(win)
