import pickle
import framework
from framework import Status
from framework import Auto_player 
import UnbiasedNet
import numpy as np
import calling_station

net = UnbiasedNet.NeuralNet(framework.n_in, 
                            framework.n_hidden, framework.n_out, 
                            alpha=0.001, lamb=0.9, randomInit=True)
auto = Auto_player(net, name= "nova")
#auto= pickle.load(open("nova.p", "rb"))
cs= calling_station.Calling_station()
auto.train(7000, cs)
pickle.dump(auto, open("nova.p", "wb"))
