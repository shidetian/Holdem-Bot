import pickle
import UnbiasedNet

import onlyCardStatus as oc
from calling_station import Calling_station
from betting_station import Betting_station

result_name = 'result_coarser_onlyCard_vs_betting.txt'
ALPHA = 0.005
n_train = 100000

for LAMB in [0.7, 0.65]:
    
    name = 'coarser_onlyCard_vs_betting_.005_' + str(LAMB) + '_1e5.p'

    net1 = UnbiasedNet.NeuralNet(oc.n_in, oc.n_in, oc.n_out, randomInit=True,
                               alpha=ALPHA, lamb=LAMB)
    auto = oc.OnlyCardAutoPlayer(net1, name="auto1", check_prob=0.3,
                                call_prob=0.3, raise_prob=0.3, checkfold_prob=0.1)
    ai = Betting_station()
    auto.train(n_train, ai, debug=0, frenzy=1)
    pickle.dump(auto, open(name, "wb"))

    result = []
    for i in range(10):
        result.append( auto.compete(ai, 5000, debug=0) )
    data = '\n Learning rate: ' + str(ALPHA)
    data += '\n Lambda: ' + str(LAMB)
    data += '\n Number of training: ' + str(n_train)
    data += '\n Results: ' + str(result)
    print data
    
    
    with open(result_name, 'a') as f:
        f.write(data)
