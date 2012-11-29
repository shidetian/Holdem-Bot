import pickle
import UnbiasedNet
import anotherStatus as another
import calling_station
import betting_station
import time
import numpy as np
import framework
from tight_aggressive import Tight_aggressive

name = 'frenzy_vs_TA.p'
start=time.time()
ALPHA = 0.001
LAMBS = [0.9]
n_train = []

for LAMB in LAMBS:
    net = UnbiasedNet.NeuralNet(another.n_in, another.n_hidden, another.n_out,
                                alpha=ALPHA, lamb=LAMB, randomInit=True)
    auto = another.AnotherAutoPlayer(net, name="against_TA")
    auto2= Tight_aggressive()
    distance=10
    i=0
    while distance > 0.0002:
        oldnet=auto.net.deepcopy()
        auto.net.alpha/=1.01
        auto.train(1000, auto2, debug=0, frenzy=1)
        distance= UnbiasedNet.diff(auto.net, oldnet)
        i=i+1000
    print "number of training:", i    
    pickle.dump(auto, open(str(LAMB) + name, "wb"))
    n_train.append(i)
print "the training used time", time.time()-start

bsbot=betting_station.Betting_station()
j=0
for LAMB in LAMBS:  
    auto = pickle.load(open(str(LAMB)+name, 'rb'))
    result = []
    for i in range(20):
        result.append( 
            auto.compete(bsbot, 2000, debug=0))
    print 'Lambda:', LAMB
    print 'Number of training:', n_train[j]
    j+=1
    print 'Results: ', result
    print 'mean', np.mean(result)
    print 'std', np.std(result)
