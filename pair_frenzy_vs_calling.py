import pickle
import UnbiasedNet
import pairStatus as fw

from calling_station import Calling_station 
name = 'pair_frenzy_vs_calling_.005_.95_2e6.p'

ALPHA = 0.002
LAMB = .95
n_train = 200000
for LAMB in [0.7, 0.75, 0.8, 0.85, 0.9]:
    name = 'pair_vs_calling_.002_' + str(LAMB) + '_2e6.p'
    stat_obj = fw.AnotherStatus()
    n_cards = sum( len(stat_obj.vec_cards[key]) for key in stat_obj.vec_cards )
    print n_cards

    net = UnbiasedNet.NeuralNet(fw.n_in, n_cards, fw.n_out,
                               alpha=ALPHA, lamb=LAMB, momentum=0.5,
                                subdiv=[(0,0), (n_cards,n_cards),
                                        (fw.n_in,n_cards)])
    net2 = UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                                    alpha=ALPHA, lamb=LAMB, randomInit=True)
    auto = fw.AnotherAutoPlayer(net, name="superbot")
    ai = Calling_station()
    auto.train(n_train, ai, debug=0, frenzy=1)
    pickle.dump(auto, open(name, "wb"))

    auto = pickle.load(open(name, 'rb'))
    result = []
    for i in range(10):
        result.append( auto.compete(ai, 5000, debug=0) )
    print 'Learning rate:', ALPHA
    print 'Lambda:', LAMB
    print 'Number of training:', n_train
    print 'Results: ', result
    name = 'result_' + name
    pickle.dump(result, open(name, "wb"))

