import pickle
import UnbiasedNet
import realizedStatus as fw
from calling_station import Calling_station
from betting_station import Betting_station 

ALPHA = 0.002
n_train = 200000

for LAMB in [0.7, 0.65, 0.6, 0.55, 0.5]:
    name = 'realized_dealer_vs_betting_.002_' + str(LAMB) + '_2e6.p'
    stat_obj = fw.AnotherStatus()
    n_cards = sum( len(stat_obj.vec_cards[key]) for key in stat_obj.vec_cards )
    n_cards += 1
    print n_cards

    net = UnbiasedNet.NeuralNet(fw.n_in, n_cards, fw.n_out, randomInit=False,
                               alpha=ALPHA, lamb=LAMB, momentum=0.5,
                                subdiv=[(0,0), (n_cards,n_cards),
                                        (fw.n_in,n_cards)])
    auto = fw.AnotherAutoPlayer(net, name="superbot")
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
    
    name = 'result_' + name[:-2] +  '.txt'
    with open('name', 'w') as f:
        f.write(data)
