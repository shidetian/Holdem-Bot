import pickle
import UnbiasedNet
import anotherStatus as fw
import calling_station
import betting_station
import time
import numpy as np
name = 'frenzy_vs_betting.p'
start=time.time()
ALPHA = 0.001
LAMBS = [0.75]
n_train = []

callBot = calling_station.Calling_station()
bsbot=betting_station.Betting_station()
for LAMB in LAMBS:
    net = UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                                alpha=ALPHA, lamb=LAMB, randomInit=True)
    auto = fw.AnotherAutoPlayer(net, name="superbot")
    
    distance=10
    i=0
    while distance > 0.0002:
        oldnet=auto.net.deepcopy()
        auto.net.alpha/=1.01
        auto.train(1000, bsbot, debug=0, frenzy=1)
        distance= UnbiasedNet.diff(auto.net, oldnet)
        i=i+1000
        pickle.dump(auto, open(str(LAMB) + name, "wb"))
    print "number of training:", i    
    n_train.append(i)
print "the training used", time.time()-start

opp_name = str(LAMB) + name
for k in range(10):
    net = UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                                alpha=ALPHA, lamb=LAMB, randomInit=True)
    child = fw.AnotherAutoPlayer(net, name="superbot")

    distance=10
    i=0
    while distance > 0.0002:
        oldnet=auto.net.deepcopy()
        auto.net.alpha/=1.01
        child.train(1000, auto, debug=0, frenzy=1)
        distance= UnbiasedNet.diff(auto.net, oldnet)
        i=i+1000
        pickle.dump(child, open(str(k) + 'th_gen_' + name, "wb"))
    auto = child
    print "number of training:", i
    
j=0
for LAMB in LAMBS:  
    auto = pickle.load(open(str(LAMB)+name, 'rb'))
    result = []
    for i in range(20):
        result.append( 
            auto.compete(ai, 2000, debug=0))
    print 'Against calling station'
    print 'Lambda:', LAMB
    print 'Number of training:', n_train[j]
    j+=1
    print 'Results: ', result
    print 'mean', np.mean(result)
    print 'std', np.std(result)
    
for LAMB in LAMBS:  
    auto = pickle.load(open(str(LAMB)+name, 'rb'))
    result = []
    for i in range(20):
        result.append( 
            auto.compete(bsbot, 2000, debug=0))
    print 'Against betting bot'
    print 'Lambda:', LAMB
    print 'Number of training:', n_train[j]
    j+=1
    print 'Results: ', result
    print 'mean', np.mean(result)
    print 'std', np.std(result)
