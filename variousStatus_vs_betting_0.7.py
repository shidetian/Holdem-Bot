import pickle
import UnbiasedNet
import coarserStatus as fw
from calling_station import Calling_station
from betting_station import Betting_station 

ALPHA = 0.002
n_train = 200000
LAMB = 0.7
data = '\n Learning rate: ' + str(ALPHA)
data += '\n Lambda: ' + str(LAMB)
data += '\n Number of training: ' + str(n_train) + '\n'
data_name = 'variousStatus_vs_betting_0.7.txt'

for status in ['pairStatus', 'anotherStatus',
               'realizedStatus', 'coarserStatus']:

    fw = __import__(status)

    stat_obj = fw.AnotherStatus()
    n_cards = sum( len(stat_obj.vec_cards[key]) for key in stat_obj.vec_cards )

    name = status + '_0.7_2e5_vs_betting.p'

    net = UnbiasedNet.NeuralNet(fw.n_in, n_cards, fw.n_out,
                                alpha=ALPHA, lamb=LAMB,
                                subdiv=[(0,0), (n_cards,n_cards),
                                        (fw.n_in,n_cards)])
    auto = fw.AnotherAutoPlayer(net, name="'")
    ai = Betting_station()
    auto.train(n_train, ai, debug=0, frenzy=1)
    pickle.dump(auto, open(name, "wb"))
    result = []
    for i in range(10):
        result.append( auto.compete(ai, 5000, debug=0) )
    data += status + 'result'
    data += str(result)
    with open(data_name, 'a') as f:
        f.write(data)
