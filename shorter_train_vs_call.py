import pickle
import UnbiasedNet
import calling_station
import betting_station
import time
import numpy as np
import shorter_framework as sfw

name = 'shorter_frenzy_vs_call.p'
start=time.time()
ALPHA = 0.005
LAMBS = [0.9]
n_train = []
n_in=208
n_hidden=150
n_out=1

for LAMB in LAMBS:
    net = UnbiasedNet.NeuralNet(n_in, n_hidden, n_out,
                                alpha=ALPHA, lamb=LAMB, randomInit=True)
    auto = sfw.shorter_Auto_player(net, name="shorter_against_call")
    csbot= calling_station.Calling_station()
    distance=10
    i=0
    while distance > 0.0001:
        oldnet=auto.net.deepcopy()
        auto.net.alpha/=1.005
        auto.train(1000, csbot, debug=0, frenzy=1, recover_rate=0)
        distance= UnbiasedNet.diff(auto.net, oldnet)
        i=i+1000
    print "number of training:", i    
    pickle.dump(auto, open(str(LAMB) + name, "wb"))
    n_train.append(i)
print "the training used time", time.time()-start

j=0
for LAMB in LAMBS:  
    auto = pickle.load(open(str(LAMB)+name, 'rb'))
    result = []
    for i in range(20):
        result.append( 
            auto.compete(csbot, 2000, debug=0))
    print 'Lambda:', LAMB
    print 'Number of training:', n_train[j]
    j+=1
    print 'Results: ', result
    print 'mean', np.mean(result)
    print 'std', np.std(result)
