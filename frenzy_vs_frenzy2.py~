import pickle
import UnbiasedNet
import anotherStatus as fw
name = 'frenzy_vs_frenzy.p'

ALPHA = 0.005
LAMB = 0.9
n_train = 100000


net = UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                           alpha=ALPHA, lamb=LAMB, randomInit=True)
auto = fw.AnotherAutoPlayer(net, name="superbot")
ai = fw.AnotherAutoPlayer(net, name='cpu', frenzy=1)

auto.train(n_train, ai, debug=0, frenzy=1)
pickle.dump(auto, open(name, "wb"))

auto = pickle.load(open(name, 'rb'))
result = []
for i in range(10):
    result.append( auto.compete(Calling_station(), 5000, debug=0) )
print 'Learning rate:', ALPHA
print 'Lambda:', LAMB
print 'Number of training:', n_train
print 'Results: ', result
name = 'result_' + name
pickle.dump(result, open(name, "wb"))

