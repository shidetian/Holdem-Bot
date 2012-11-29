import pickle
import framework
from framework import Status
from framework import Auto_player 
import UnbiasedNet
import numpy as np
import calling_station
from cheater_bot import Cheater_player

#auto=pickle.load(open("9th_gen_frenzy_vs_calling.p", "rb"))
auto=pickle.load(open("twinB.p", "rb"))
#net2=UnbiasedNet.NeuralNet(framework.n_in ,framework.n_hidden, 
#                           framework.n_out, True)
#auto2=framework.Auto_player(net2)
#cheater= Cheater_player()
cheater = calling_station.Calling_station()
wins= []
for i in range(40):
    wins.append(auto.compete(cheater, 100, debug=0))
    #print wins
print np.mean(wins)
print np.std(wins)
#print auto.net.n_in, auto.net.n_hidden, auto.net.n_hidden, auto.net.w_out
#print auto2.net.w_out
#print auto.net.w_in[1], auto2.net.w_in[1]
