import pickle
import framework
from framework import Status
from framework import Auto_player 
import UnbiasedNet
import numpy as np

auto=pickle.load(open("player.p", "rb"))
net2=UnbiasedNet.NeuralNet(framework.n_in ,framework.n_hidden, 
                           framework.n_out, False)
auto2=framework.Auto_player(net2)
wins= []
for i in range(10):
    wins.append(auto.compete(auto2,1000))
print wins
print sum(wins)
