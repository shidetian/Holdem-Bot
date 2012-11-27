import pickle
import framework
from framework import Status
from framework import Auto_player
import UnbiasedNet
import numpy as np
import calling_station
import betting_station
import time
start= time.time()
net = UnbiasedNet.NeuralNet(framework.n_in,
                            150, framework.n_out,
                            alpha=0.005, lamb=0.9, randomInit=True)
net2= UnbiasedNet.NeuralNet(framework.n_in, 150, framework.n_out, 
                            alpha=0.005, lamb=0.95, randomInit=True)
auto=pickle.load(open("lion150_2.p", "rb"))
auto2=pickle.load(open("lion150_3.p", "rb"))
#cs= calling_station.Calling_station()
#bs= betting_station.Betting_station()
distance=10
i=0
auto.net.alpha=0.001
while distance > 0.0003:
    oldnet= auto.net.deepcopy()
    auto.net.alpha /=1.01
    auto.train(1000, auto2, frenzy=1, debug=0)
    distance= UnbiasedNet.diff(auto.net, oldnet)
#    print i, UnbiasedNet.diff(auto.net, oldnet)
    i= i+1000
    pickle.dump(auto, open("lion150_2_against_lion3.p","wb"))
wins= []
for j in range(20):
    wins.append(auto.compete(auto2, 2000, debug=0))
print wins
print "mean", np.mean(wins)
print "std",  np.std(wins)
print "trained", i 
print "newest_alpha", auto.net.alpha
print "used, ", time.time()-start
