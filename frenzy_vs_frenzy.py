import pickle
import UnbiasedNet
import anotherStatus as fw
from anotherStatusBots import CallingStation
name = 'momentum_vs_calling_.005_.95_2e6.p'

ALPHA = 0.002
LAMB = .95
n_train = 200000

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
ai = CallingStation()
auto.train(n_train, ai, debug=0, frenzy=0)
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

