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
net2 = UnbiasedNet.NeuralNet(framework.n_in,
                            framework.n_hidden, framework.n_out,
                            alpha=0.001, lamb=0.9, randomInit=True)
auto = Auto_player(net, name= "nova")
#auto= pickle.load(open("nova.p", "rb"))
cs= calling_station.Calling_station()
auto.train(3000, cs)
pickle.dump(auto, open("nova.p", "wb"))
#auto = Auto_player(net, name= "Moon")
#auto2= Auto_player(net2, name= "noname")
#auto.train(4000,auto2)
#pickle.dump(auto, open("moon.p", "wb"))

#now test
#auto= pickle.load(open("moon.p", "rb"))
#wins=[]
#for i in range(40):
#    wins.append(auto.compete(auto2, 2000, debug=0))
#print np.mean(wins)
#print np.std(wins)
