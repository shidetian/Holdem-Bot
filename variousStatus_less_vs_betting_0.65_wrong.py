import pickle
import UnbiasedNet
from calling_station import Calling_station
from betting_station import Betting_station 

ALPHA = 0.002
n_train = 200000
LAMB = 0.65
data = '\n Learning rate: ' + str(ALPHA)
data += '\n Lambda: ' + str(LAMB)
data += '\n Number of training: ' + str(n_train) + '\n'
data_name = 'variousStatus_less_vs_betting_0.65_w.txt'

for r in [0.1, 0.2, 0.3, 0.4]:
    for status in ['pairStatus', 'anotherStatus',
                   'realizedStatus', 'coarserStatus']:

        fw = __import__(status)

        stat_obj = fw.AnotherStatus()
        n_cards = sum( len(stat_obj.vec_cards[key]) for key in stat_obj.vec_cards )

        name = status + str(r)+ '_0.65_2e5_vs_betting_w.p'

        net = UnbiasedNet.NeuralNet(fw.n_in, n_cards, fw.n_out, randomInit=True,
                                    alpha=ALPHA, lamb=LAMB,
                                    subdiv=[(0,0), (n_cards,n_cards),
                                            (fw.n_in,n_cards)])
        auto = fw.AnotherAutoPlayer(net, name="'",check_prob=0.3,
                                    call_prob=0.3, raise_prob=r, checkfold_prob=0.1)
        ai = Betting_station()
        auto.train(n_train, ai, debug=0, frenzy=1)
        pickle.dump(auto, open(name, "wb"))
        result = []
        for i in range(10):
            result.append( auto.compete(ai, 5000, debug=0) )
        data += '\n raise_prob: ' + str(r)
        data += status + ' result: '
        data += str(result)
        with open(data_name, 'a') as f:
            f.write(data)
