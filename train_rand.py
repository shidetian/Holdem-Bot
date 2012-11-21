import pickle
import framework
from framework import Status
from framework import Auto_player
import UnbiasedNet
import numpy as np
import calling_station

net = UnbiasedNet.NeuralNet(framework.n_in,
                            framework.n_hidden, framework.n_out,
                            alpha=0.001, lamb=0.5, randomInit=True)
auto= Auto_player(net, "lion")
cs= calling_station.Calling_station()
distance=10
i=0
while distance > 0.0005:
    oldnet= auto.net.deepcopy()
    auto.net.alpha /=1.02
    auto.train(1000, cs, frenzy=1, debug=0)
    distance= UnbiasedNet.diff(auto.net, oldnet)
#    print i, UnbiasedNet.diff(auto.net, oldnet)
#    i= i+1
    pickle.dump(auto, open("lion.p","wb"))
wins= []
for i in range(50):
    wins.append(auto.compete(cs, 10000, debug=0))
    print "win ", wins[i]
print np.mean(wins)
print np.std(wins)

