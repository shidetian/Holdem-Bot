import pickle
import framework
from framework import Status
from framework import Auto_player 
import UnbiasedNet
import numpy as np
import calling_station


auto=pickle.load(open("nova.p", "rb"))
#net2=UnbiasedNet.NeuralNet(framework.n_in ,framework.n_hidden, 
#                           framework.n_out, True)
#auto2=framework.Auto_player(net2)
cs= calling_station.Calling_station()
wins= []
for i in range(20):
    wins.append(auto.compete(cs, 5000, debug=0))
print wins
print np.mean(wins)
print np.std(wins)
#print auto.net.n_in, auto.net.n_hidden, auto.net.n_hidden, auto.net.w_out
#print auto2.net.w_out
#print auto.net.w_in[1], auto2.net.w_in[1]
