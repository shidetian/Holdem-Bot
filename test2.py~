from HandStat import *
#from framework import *
import pickle
from UnbiasedNet import *
import call_defeater
import tight_aggressive
import framework
import numpy as np

net=UnbiasedNet.NeuralNet(1,1,1)
auto= MyAutoPlayer(net, "crazy_guy", frenzy=1)
#auto= Auto_player(net, "crazy_guy", frenzy=1)
#pickle.dump(auto, open("crazy_guy.p", "wb"))
net2=UnbiasedNet.NeuralNet(n_in, n_hidden, n_out, 0.004, 0.9, randomInit=True)
auto2= MyAutoPlayer(net2, "HandStat_trained_crazily")
#auto2= Auto_player(net2, "HandStat_trained_crazily")
#auto2.train(60000, auto, frenzy=1)
#pickle.dump(auto2, open("fw_trained_crazily.p", "wb"))
auto3=call_defeater.Call_defeater()
pickle.dump(auto3, open("call_defeater.p", "wb"))
ta= tight_aggressive.Tight_aggressive()
vs_ta=pickle.load(open("0.9frenzy_vs_TA.p", "rb"))
wins=[]
for i in range(20):
    wins.append(vs_ta.compete(ta, 2000, debug=0))
print wins
print 'mean', np.mean(wins)
print 'std', np.std(wins)
