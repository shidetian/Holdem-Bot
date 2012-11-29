import pickle
from biasedPerceptron import BiasedPerceptron, diff
import anotherStatus as fw
import calling_station
import betting_station
import time
import numpy as np
name = 'frenzy_perceptron_vs_frenzy.p'
start=time.time()
ALPHA = 0.001
LAMBS = [0.8, 0.85, 0.9, 0.95, 1]
n_train = 500000

csBot = calling_station.Calling_station()
bsBot=betting_station.Betting_station()
for LAMB in LAMBS:
    net = BiasedPerceptron(fw.n_in, fw.n_hidden, fw.n_out,
                                alpha=ALPHA, lamb=LAMB, randomInit=True)
    net2 = BiasedPerceptron(fw.n_in, fw.n_hidden, fw.n_out,
                                alpha=ALPHA, lamb=LAMB, randomInit=True)
    auto = fw.AnotherAutoPlayer(net, name="superbot")
    ai = fw.AnotherAutoPlayer(net2, name='cpu', frenzy=1)

    auto.train(n_train, bsBot, debug=0, frenzy=1)
    
    pickle.dump(auto, open(str(LAMB) + name, "wb"))
    
print "the training used time", time.time()-start


j=0
for LAMB in LAMBS:  
    auto = pickle.load(open(str(LAMB)+name, 'rb'))
    result = []
    for i in range(5):
        result.append( 
            auto.compete(bsBot, 2000, debug=0))
    print 'Lambda:', LAMB
    print 'Results against betting bot: ', result
    print 'mean', np.mean(result)
    print 'std', np.std(result)
